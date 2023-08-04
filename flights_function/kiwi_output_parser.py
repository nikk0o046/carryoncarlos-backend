import logging
logger = logging.getLogger(__name__)
import time

def extract_info(api_response):
    start_time = time.time() #start timer to log it later
    logger.info("Extracting information from response data...")

    if api_response is None or 'data' not in api_response:  # Check that the response is not None and contains 'data'
        logger.warning("Invalid API response")
        return []

    output = []
    seen_cities = set()
    try:  # Try to extract the information from the response
        for index, flight in enumerate(api_response['data']):
            if flight['cityTo'] not in seen_cities:
                average_duration = flight['duration']['total'] / 2  # Since we have both the outbound and return flights
                stop_overs = len(flight['route']) - 2  # Subtracting 2 because there's one flight out and one flight back

                flight_info = {
                    "flight_number": index + 1,
                    "from": flight['cityFrom'],
                    "to": flight['cityTo'],
                    "average_duration": {
                        "hours": average_duration // 3600,
                        "minutes": (average_duration // 60) % 60
                    },
                    "stop_overs": stop_overs,
                    "price": {
                        "value": flight['price'],
                        "currency": api_response['currency']
                    },
                    "booking_link": flight['deep_link']
                }
                output.append(flight_info)
                seen_cities.add(flight['cityTo'])
                
    except KeyError as e:  # This will catch any missing keys in the response
        logger.exception("Failed to extract info from API response: %s", e)
        return []

    logger.info("Information extraction completed. %s flights left after processing.", len(output))
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Function execution time: {elapsed_time} seconds")
    
    return output


