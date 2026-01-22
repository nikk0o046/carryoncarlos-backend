import logging
from opentelemetry import trace


logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


@tracer.chain
def create_other_params(
    selectedCityID: str, cabinClass: str, travelers: dict, user_id: str
) -> dict:
    """
    This function takes the selected city ID, the cabin class, the travelers and the user ID and returns them and some default parameters as a dictionary.

    Args:
        selectedCityID (str): The selected city ID.
        cabinClass (str): The cabin class.
        travelers (dict): The travelers.
        user_id (str): The user ID.

    Returns:
        dict: The other parameters.
    """

    logger.debug("[UserID: %s] Creating other parameters...", user_id)

    # Map the cabinClass to the expected API value
    cabin_mapping = {"Economy": "M", "Economy Premium": "W", "Business": "C", "First Class": "F"}
    selected_cabin = cabin_mapping.get(cabinClass, "M")  # Default to Economy if not found

    adults = travelers.get("adults", 1)
    children = travelers.get("children", 0)
    infants = travelers.get("infants", 0)

    other_params = {
        "adults": str(adults),
        "children": str(children),
        "infants": str(infants),
        "selected_cabins": selected_cabin,
        "fly_from": selectedCityID,
        "stopover_from": "1:00",
        "limit": "1000",
        "conn_on_diff_airport": "0",
        "ret_from_diff_city": "false",
        "ret_from_to_city": "false",
    }
    logger.debug("[UserID: %s] Other parameters created: %s", user_id, other_params)
    return other_params
