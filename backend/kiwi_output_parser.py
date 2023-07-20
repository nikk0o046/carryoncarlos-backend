import logging
logger = logging.getLogger(__name__)

def extract_info(api_response):
    logger.info("Extracting information from response data...")

    if api_response is None or 'data' not in api_response:  # Check that the response is not None and contains 'data'
        logger.warning("Invalid API response")
        return []

    output = []
    seen_cities = set()
    try:  # Try to extract the information from the response
        for index, flight in enumerate(api_response['data']):
            if flight['cityTo'] not in seen_cities:
                flight_info = (
                    f"Flight {index + 1}:\n"
                    f"From: {flight['cityFrom']}\n"
                    f"To: {flight['cityTo']}\n"
                    f"Flight Duration: {flight['duration']['total'] // 3600} hours {flight['duration']['total'] % 3600 // 60} minutes\n"
                    f"Price: {flight['price']} {api_response['currency']}\n"
                    f"Booking Link: {flight['deep_link']}\n"
                    "-----------------------------------\n"
                )
                output.append(flight_info)
                seen_cities.add(flight['cityTo'])
    except KeyError as e:  # This will catch any missing keys in the response
        logger.exception("Failed to extract info from API response: %s", e)
        return []

    logger.info("Information extraction completed.")
    return output


