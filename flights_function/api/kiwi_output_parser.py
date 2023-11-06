import logging
logger = logging.getLogger(__name__)
import time

def extract_info(api_response, user_id):
    start_time = time.time() #start timer to log it later
    logger.debug("[UserID: %s] Extracting information from response data...", user_id)


    if api_response is None or 'data' not in api_response:  # Check that the response is not None and contains 'data'
        logger.warning("[UserID: %s] Invalid API response", user_id)
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

        for flight in output:
            logger.info(
                "[UserID: %s] Flight details - From: %s, To: %s, Duration: %sh %sm, Stopovers: %s, Price: %s %s",
                user_id,
                flight['from'],
                flight['to'],
                flight['average_duration']['hours'],
                flight['average_duration']['minutes'],
                flight['stop_overs'],
                flight['price']['value'],
                flight['price']['currency'],
                extra={'booking_link': flight['booking_link']}
            )
                
    except KeyError as e:  # This will catch any missing keys in the response
        logger.exception("[UserID: %s] Failed to extract info from API response: %s", user_id, e)
        return []
    
    #logger.info("[UserID: %s] Information extraction completed. %s flights left after processing.", user_id, len(output))
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)
    
    return output


