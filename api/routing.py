#ROUTING_MAP = {
    # "intent_name": "Department"
#}


def get_destination(intent: str) -> str:

    return ROUTING_MAP.get(
        intent,
        "Manual Review"
    )
