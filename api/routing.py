ROUTING_MAP = {
    # Cards Operations
    "card_payment_fee_charged": "Cards Operations",
    "visa_or_mastercard": "Cards Operations",
    "getting_spare_card": "Cards Operations",
    "change_pin": "Cards Operations",
    "card_about_to_expire": "Cards Operations",
    "supported_cards_and_currencies": "Cards Operations",

    # Payments / Transfers Operations
    "cancel_transfer": "Payments / Transfers Operations",
    "beneficiary_not_allowed": "Payments / Transfers Operations",

    # Digital Banking / Security
    "apple_pay_or_google_pay": "Digital Banking / Security",
    "lost_or_stolen_phone": "Digital Banking / Security",
}


# Replace this with the threshold agreed by your team.
CONFIDENCE_THRESHOLD = 0.30


def get_route(intent: str) -> str:
    return ROUTING_MAP.get(intent, "Manual Review")


def requires_human_review(confidence: float) -> bool:
    return confidence < CONFIDENCE_THRESHOLD
