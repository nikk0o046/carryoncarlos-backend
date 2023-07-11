import requests
from secret_keys import KIWI_API_KEY

def make_API_request(params1, params2, params3):

    url = "https://api.tequila.kiwi.com/v2/search"

    # Combine queries from parts 2, 3, and 4
    # Combine all dictionaries into a single payload dictionary
    payload = {**params1, **params2, **params3}
        
    # API headers
    headers = {
        'apikey': KIWI_API_KEY,
    }

    # Make the API call
    response = requests.request("GET", url, headers=headers, params=payload)

    # This will give the JSON response
    data = response.json()

    return data