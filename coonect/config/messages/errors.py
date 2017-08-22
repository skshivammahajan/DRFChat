ERROR_INVALID_DEVICE_ID = {"code": 5001, "message": "Device does not exist."}
ERROR_INVALID_USER_DEVICE = {"code": 5002, "message": "User device does not exist."}
ERROR_INVALID_EXPERT_DEVICE = {"code": 5003, "message": "Expert device does not exist."}
ERROR_INVALID_EXPERT_PROFILE = {"code": 5004, "message": "Expert profile does not exist."}

ERROR_REVIEW_ALREADY_SUBMITTED = {"code": 5011, "message": "You have already reviewed this session."}

ERROR_INVALID_SCHEDULED_DATETIME = {"code": 5012, "message": "Scheduled date time should be in future."}
ERROR_INVALID_SCHEDULED_DURATION = {"code": 5013, "message": "Scheduled duration not a valid choice."}
ERROR_INVALID_SCHEDULED_SLOT = {"code": 5014, "message": "Scheduled slot does not exist or it has been already booked."}

ERROR_CARD_USED_IN_UNSETTLED_TRANSACTION = {
    "code": 5021,
    "message": "This Card can not be removed as it is used in unsettled transactions."
}
ERROR_INVALID_CARD = {"code": 5022, "message": "Card does not exist."}
ERROR_CARD_PRE_AUTHORIZATION = {
    "code": 5023, "message": "The card has insufficient funds to cover the cost of the session."
}
ERROR_DUPLICATE_CARD = {"code": 5024, "message": "Duplicate card exists in the vault."}
ERROR_GATEWAY_DECLINED = {"code": 5025, "message": "This card is invalid or as been Expired."}
ERROR_NETWORK_UNAVAILABLE = {"code": 5026, "message": "Processor Network Unavailable - Try Again."}
ERROR_NONCE_EXPIRED = {"code": 5029, "message": "This nonce is invalid or has been expired."}


ERROR_PROMO_CODE_INVALID = {"code": 5031, "message": "Promo code is not valid."}
ERROR_ALREADY_APPLIED_COUPON_CODE = {"code": 5032, "message": "You have already applied the promo code ."}
