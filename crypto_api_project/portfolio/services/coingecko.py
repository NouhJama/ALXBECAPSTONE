import requests
from django.conf import settings

COIN_GECKO_URL = "https://api.coingecko.com/api/v3"

def get_coin_price(coin_id: str, currency: str = "usd"):
    """
    Fetch the current price of a cryptocurrency from CoinGecko.

    :param coin_id: The CoinGecko ID of the cryptocurrency (e.g., 'bitcoin').
    :param currency: The fiat currency to get the price in (default is 'usd').
    :return: The current price or None if not found.
    """
    endpoint = f"{COIN_GECKO_URL}/simple/price"
    headers = {
        "api_key": settings.COIN_GECKO_API_KEY
    }
    params = {
        "ids": coin_id.lower(),
        "vs_currencies": currency
    }
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get(coin_id, {}).get(currency)
    except requests.RequestException as e:
        print(f"Error fetching price from CoinGecko: {e}")
        return None
    # Catch coin_id not found
    except KeyError:
        err_message = f"Coin ID {coin_id} not found in CoinGecko response."
        print(err_message)
        return {"Success": False, "price": None, "message": err_message}
    # Timeout exception
    except requests.Timeout:
        err_message = 'Request to CoinGecko timed out.'
        print(err_message)
        return {"Success": False, "message": err_message}