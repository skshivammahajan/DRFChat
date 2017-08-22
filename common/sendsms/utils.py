from django.conf import settings
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient


class SMSHelper:
    """
    Sends the Verification code through sms to user's registered phone .
    """
    client = None

    def __init__(self):
        self.client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

    def send_sms(self, to, body):
        try:
            self.client.messages.create(to=to, from_=settings.PHONE, body=body)
        except TwilioRestException:
            pass
