def extract_info(api_response):
    output = []
    for index, flight in enumerate(api_response['data']):
        flight_info = (
            f"Flight {index + 1}:\n"
            f"From: {flight['cityFrom']}\n"
            f"To: {flight['cityTo']}\n"
            f"Flight Duration: {flight['duration']['total'] // 3600} hours {flight['duration']['total'] % 3600 // 60} minutes\n"
            f"Price: {flight['price']} {api_response['currency']}\n"
            "-----------------------------------\n"
        )
        output.append(flight_info)
    return output

