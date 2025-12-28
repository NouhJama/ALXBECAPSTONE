import requests
from django.conf import settings
from django.core.cache import cache


COIN_GECKO_URL = "https://api.coingecko.com/api/v3"

def get_coin_price(coin_id: str, currency: str = "usd"):
    """
    - First look the price in cache. If found, return it.
    - If not found in cache, fetch from CoinGecko API.
    - Cache the fetched price for future requests.
    Args:
        coin_id (str): The CoinGecko coin ID (e.g., 'bitcoin').
        currency (str): The target currency (e.g., 'usd').
    """
    cache_key = f"coin_price_{coin_id}_{currency}"
    # Try to get  price from cache
    cached_price = cache.get(cache_key)
    if cached_price is not None:
        print("Price fetched from cache.")
        return {"success": True, "price": cached_price, "message": None}
    # If not in cache, fetch from CoinGecko API
    print("Fetching price from CoinGecko API.")

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

        # Cache the price for 5 minutes (300 seconds)
        price = data[coin_id.lower()][currency.lower()]
        cache.set(cache_key, price, timeout=300)

        return {
            "success": True, "price": price, "message": None
        }
    
    # Timeout exception
    except requests.Timeout:
        err_message = 'Request to CoinGecko timed out.'
        return {"success": False, "message": err_message}
    
    # Catch network-related errors
    except requests.RequestException as e:
        message = 'Network error occurred while fetching data from CoinGecko.'
        return {"success": False, "price": None, "message": str(e)}
     
    # Catch coin_id not found
    except KeyError:
        err_message = f"Coin ID {coin_id} not found in CoinGecko response."
        return {"success": False, "price": None, "message": err_message}
   