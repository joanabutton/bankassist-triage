ROUTING_MAP = {
    # Add team-approved intent → route mappings here
}


CONFIDENCE_THRESHOLD = None


def get_route(intent: str) -> str:
    return ROUTING_MAP.get(intent, "Manual Review")


def requires_human_review(confidence: float) -> bool:

    if CONFIDENCE_THRESHOLD is None:
        return True

    return confidence < CONFIDENCE_THRESHOLD
