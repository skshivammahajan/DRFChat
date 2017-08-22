from rest_framework import serializers

from payments.models import Card


class CardSerializer(serializers.ModelSerializer):
    """
    Serializes card.
    """
    class Meta:
        model = Card
        fields = ('id', 'last_4', 'card_type', 'expiration_date', 'is_default', )


class NonceSerializer(serializers.Serializer):
    """
    Serializer to validate payment method nonce.
    """
    payment_method_nonce = serializers.CharField(max_length=100)
