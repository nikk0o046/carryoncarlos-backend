import logging
logger = logging.getLogger(__name__)

def create_other_params():
    logger.info("Creating other parameters...")

    other_params = {
        "limit" : "200",
        "fly_from" : "HEL",
        "max_stopovers" : "1",
        "stopover_to" : "4:00",
        "conn_on_diff_airport" : "0",
        "ret_from_diff_city" : "false",
        "ret_from_to_city" : "false",
    }
    logger.info("Other parameters created: %s", other_params)
    return other_params