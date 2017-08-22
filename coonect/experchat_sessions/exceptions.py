from rest_framework.exceptions import APIException
from rest_framework.settings import api_settings


class InvalidPreAuthException(APIException):
    status_code = 400
    default_detail = {api_settings.NON_FIELD_ERRORS_KEY: ["ERROR_CARD_PRE_AUTHORIZATION"]}
    default_code = 'invalid'
