from rest_framework.exceptions import APIException
from rest_framework.settings import api_settings


class InvalidNonceException(APIException):
    status_code = 400
    default_detail = {api_settings.NON_FIELD_ERRORS_KEY: ["ERROR_NONCE_EXPIRED"]}
    default_code = 'invalid'


class UnsettledCardException(APIException):
    status_code = 400
    default_detail = {api_settings.NON_FIELD_ERRORS_KEY: ["ERROR_CARD_USED_IN_UNSETTLED_TRANSACTION"]}
    default_code = 'invalid'


class DuplicateCardException(APIException):
    status_code = 400
    default_detail = {api_settings.NON_FIELD_ERRORS_KEY: ["ERROR_DUPLICATE_CARD"]}
    default_code = 'invalid'


class GatewayDeclinedErorr(APIException):
    status_code = 400
    default_detail = {api_settings.NON_FIELD_ERRORS_KEY: ["ERROR_GATEWAY_DECLINED"]}
    default_code = 'invalid'


class GatewayNetworkUnavailableError(APIException):
    status_code = 400
    default_detail = {api_settings.NON_FIELD_ERRORS_KEY: ["ERROR_NETWORK_UNAVAILABLE"]}
    default_code = 'invalid'
