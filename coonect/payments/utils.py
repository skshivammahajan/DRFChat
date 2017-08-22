import braintree
from django.conf import settings

from experchat.patterns import Singleton
from payments.exceptions import (
    DuplicateCardException, GatewayDeclinedErorr, GatewayNetworkUnavailableError, InvalidNonceException,
    UnsettledCardException
)
from payments.models import Card, Customer, Transaction


class ExperchatPayment(metaclass=Singleton):
    """
    This class provides all payment options by using braintree SDK.
    """

    def __init__(self):
        braintree.Configuration.configure(
            settings.BRAINTREE_ENVIRONMENT,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY
        )

    def generate_client_token(self):
        return braintree.ClientToken.generate()

    def create_or_update_customer(self, user, payment_method_nonce):
        customer = Customer.objects.filter(user=user).first()
        is_masterpass_card = False
        if payment_method_nonce.split('-')[0].upper() == 'fake'.upper():
            is_masterpass_card = True

        if customer is not None:
            result = braintree.Customer.update(customer.customer_uid, {
                "credit_card": {
                    "payment_method_nonce": payment_method_nonce,
                    "options": {
                        "verify_card": True,
                        "make_default": True,
                        "fail_on_duplicate_payment_method": False
                    }
                }
            })

        else:
            result = braintree.Customer.create({
                "first_name": user.get_full_name(),
                "credit_card": {
                    "payment_method_nonce": payment_method_nonce,
                    "options": {
                        "verify_card": True
                    }
                }
            })

            if result.is_success:
                customer = Customer.objects.create(
                    user=user,
                    customer_uid=result.customer.id,
                )

        if result.is_success:
            try:
                if is_masterpass_card:
                    new_payment_method = result.customer.masterpass_cards[0]
                else:
                    new_payment_method = result.customer.payment_methods[0]
            except IndexError:
                raise InvalidNonceException

            is_duplicate = self.compare_and_delete_exiting_card(result.customer, new_payment_method, is_masterpass_card)
            if is_duplicate:
                # Delete the newly added card and raise exception
                if is_masterpass_card:
                    braintree.PaymentMethod.delete(new_payment_method['token'])
                else:
                    braintree.PaymentMethod.delete(new_payment_method.token)

                raise DuplicateCardException

            card = Card.objects.create(
                customer=customer,
                last_4=new_payment_method.last_4 if not is_masterpass_card else new_payment_method['last_4'],
                payment_method_token=new_payment_method.token if not is_masterpass_card else
                new_payment_method['token'],
                card_type=new_payment_method.card_type if not is_masterpass_card else new_payment_method['card_type'],
                expiration_date=new_payment_method.expiration_date if not is_masterpass_card else
                '{}/{}'.format(new_payment_method['expiration_month'], new_payment_method['expiration_year']),
                is_default=new_payment_method.default if not is_masterpass_card else new_payment_method['default'],
            )
            self.update_exisiting_cards_payment_method(customer, card)

            return card

        verification = result.credit_card_verification
        try:
            if verification.processor_response_code == '2000':
                raise GatewayDeclinedErorr
            elif verification.processor_response_code == '3000':
                raise GatewayNetworkUnavailableError
            else:
                raise InvalidNonceException
        except AttributeError:
            if result.message == 'Duplicate card exists in the vault.':
                raise DuplicateCardException
            else:
                raise InvalidNonceException

    def compare_and_delete_exiting_card(self, customer, new_payment_method, is_masterpass_card):
        """
        This will compare and raise duplicate card Error exception if alreday any card is existing
        Args:
            customer (object): Braintree customer
            current_payment_method (obj): Newly added card
            is_masterpass_card (boolean): if nonce used is a masterpass card
        Raise:
            Exception if same card is existing for the same user
        """
        if is_masterpass_card:
            existing_payment_methods = customer.masterpass_cards[1:]
        else:
            existing_payment_methods = customer.payment_methods[1:]

        is_duplicate = False
        if is_masterpass_card:
            for payment_method in existing_payment_methods:
                if payment_method['unique_number_identifier'] == new_payment_method['unique_number_identifier']:
                    is_duplicate = True
                    break
        else:
            for payment_method in existing_payment_methods:
                if payment_method.unique_number_identifier == new_payment_method.unique_number_identifier:
                    is_duplicate = True
                    break

        return is_duplicate

    def update_exisiting_cards_payment_method(self, customer, card):
        """
        Update the exisiting card payment methods to False
        Because curent card payment method is set to True
        Args:
            customer (obj): current customer
            card (obj): new created card
        return:
            None
        """
        Card.objects.filter(customer=customer).exclude(id=card.id).update(is_default=False)

    def make_card_as_default(self, card):
        """
        Util method to make a card as default
        Args:
            card (obj): card objects
        :return:
        """
        braintree.Customer.update(card.customer.customer_uid, {
            "credit_card": {
                "options": {
                    "make_default": True,
                    "update_existing_token": card.payment_method_token
                }
            }
        })
        # update the card to defualt as true
        card.is_default = True
        card.save()
        self.update_exisiting_cards_payment_method(card.customer, card)
        return card

    def delete_card(self, card):
        if Transaction.objects.filter(card=card, status__in=[Transaction.UNSETTLED, Transaction.FAILED]).exists():
            raise UnsettledCardException

        braintree.PaymentMethod.delete(card.payment_method_token)
        card.delete()

    def create_pre_auth_transaction_from_card(self, user, amount, card):
        transaction_uid = self.create_pre_auth_transaction(card.payment_method_token, amount)
        if transaction_uid is None:
            return

        return Transaction.objects.create(
            user=user,
            transaction_uid=transaction_uid,
            amount=amount,
            card=card,
        )

    def settle_user_transactions(self, user):
        unsettled_transactions = Transaction.objects.filter(user=user, status=Transaction.UNSETTLED)
        for transaction in unsettled_transactions:
            self.settle_transaction(transaction, transaction.amount)

    def cancel_user_transactions(self, user):
        unsetteled_transactions = Transaction.objects.filter(user=user, status=Transaction.UNSETTLED)
        for transaction in unsetteled_transactions:
            self.cancel_transaction(transaction)

    def create_pre_auth_transaction(self, payment_method_token, amount):
        result = braintree.Transaction.sale({
            'amount': amount,
            'payment_method_token': payment_method_token,
            'options': {
                "submit_for_settlement": False
            }
        })
        if result.is_success:
            return result.transaction.id

        return

    def settle_transaction(self, transaction, amount):
        result = braintree.Transaction.submit_for_settlement(transaction.transaction_uid, amount)

        transaction.status = Transaction.SETTLED if result.is_success else Transaction.FAILED
        transaction.save()

        return result.is_success

    def cancel_transaction(self, transaction):
        result = braintree.Transaction.void(transaction.transaction_uid)

        transaction.status = Transaction.CANCELLED if result.is_success else Transaction.FAILED
        transaction.save()

        return result.is_success
