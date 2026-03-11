import logging
import os
import time

from httpx import AsyncClient, HTTPStatusError, RequestError
from dotenv import load_dotenv

from app.constants import KIWI_BASE_URL

load_dotenv()
logger = logging.getLogger(__name__)

KIWI_API_KEY = os.environ.get("KIWI_API_KEY")


async def make_api_request(params1: dict, params2: dict, params3: dict, params4: dict, user_id: str) -> dict:
    """
    This function takes the destination, time, duration and other parameters and user ID and returns Kiwi API response.

    Args:
        params1 (dict): The destination parameters.
        params2 (dict): The time parameters.
        params3 (dict): The duration parameters.
        params4 (dict): The other parameters.
        user_id (str): The user ID.

    Returns:
        dict: The API response.
    """

    start_time = time.time()  # start timer to log it later
    logger.debug("[UserID: %s] Making API request...", user_id)

    url = f"{KIWI_BASE_URL}/v2/search"

    # Combine queries from parts 2, 3, and 4
    # Combine all dictionaries into a single payload dictionary
    payload = {**params1, **params2, **params3, **params4}
    logger.info("[UserID: %s] Payload for kiwi API: %s", user_id, payload)

    # API headers
    headers = {
        "apikey": KIWI_API_KEY,
    }

    try:
        async with AsyncClient() as client:
            response = await client.get(url, headers=headers, params=payload)
            response.raise_for_status()
    except HTTPStatusError as e:
        logger.exception("[UserID: %s] Request failed: %s", user_id, e)
        return None
    except RequestError as e:
        logger.exception("[UserID: %s] Request failed: %s", user_id, e)
        return None

    try:
        data = response.json()
    except ValueError as e:
        logger.exception("[UserID: %s] Failed to parse response as JSON: %s", user_id, e)
        return None

    logger.debug("[UserID: %s] API request completed.", user_id)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug("[UserID: %s] Function execution time: %s seconds", user_id, elapsed_time)

    # Check if flights were found and log the amounts
    try:
        if len(data["data"]) > 0:
            logger.info(
                "[UserID: %s] Number of flights: %s, Total search results: %s",
                user_id,
                len(data["data"]),
                data["_results"],
            )
        else:
            logger.info("[UserID: %s] No flights found. Total search results: %s", user_id, data["_results"])
    except KeyError:
        logger.error("[UserID: %s] Key 'data' not found in the response.", user_id)

    if "error" in data:
        logger.error("[UserID: %s] Error in response data: %s", user_id, data["error"])
        return None

    return data
