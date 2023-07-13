def extract_info(api_response):
    output = []
    seen_cities = set()
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
    return output

