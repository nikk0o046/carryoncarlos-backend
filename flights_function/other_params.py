import logging
logger = logging.getLogger(__name__)

def create_other_params(selectedCityID, cabinClass, travelers):
    logger.info("Creating other parameters...")

     # Map the cabinClass to the expected API value
    cabin_mapping = {
        "Economy": "M",
        "Economy Premium": "W",
        "Business": "C",
        "First Class": "F"
    }
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
        "stopover_from" : "1:00",
        "limit" : "1000",
        "conn_on_diff_airport" : "0",
        "ret_from_diff_city" : "false",
        "ret_from_to_city" : "false",
    }
    logger.info("Other parameters created: %s", other_params)
    return other_params