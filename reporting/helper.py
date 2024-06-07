import requests
import logging
from time import sleep
from django.conf import settings

logger = logging.getLogger(__name__)


def get_geocode(address):
    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': address,
        'key': settings.OPEN_CAGE_API,
        'limit': 1,
        'no_annotations': 1
    }
    MAX_RETRIES = 3
    retries = 0
    data = None  # Initialize data with None

    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error occurred while geocoding address '{address}': {e}")
            retries += 1
            sleep(5)
        else:
            data = response.json()
            break

    if retries == MAX_RETRIES:
        logger.error(f"Failed to geocode address '{address}' after {MAX_RETRIES} retries")
        return None

    if data is None or not data['results']:
        logger.warning(f"No geocoding results found for address '{address}'")
        return None

    location = data['results'][0]['geometry']
    return location['lat'], location['lng']
