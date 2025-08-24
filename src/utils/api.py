"""
API utilities for the Azeroth Herald bot.
Contains functions to interact with external APIs like Raider.IO.
"""

import os
import requests


async def fetch_affixes(region='us'):
    """Fetches current Mythic+ affixes from Raider.IO API."""
    try:
        raider_io_api_key = os.getenv('RAIDER_IO_API_KEY')
        if not raider_io_api_key:
            return None, "API key not configured"
        
        url = f"https://raider.io/api/v1/mythic-plus/affixes"
        params = {
            'access_key': raider_io_api_key,
            'region': region,
            'locale': 'en'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data, None
        
    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


async def fetch_season_cutoffs(region='us'):
    """Fetches current season cutoffs from Raider.IO API."""
    try:
        raider_io_api_key = os.getenv('RAIDER_IO_API_KEY')
        if not raider_io_api_key:
            return None, "API key not configured"
        
        url = f"https://raider.io/api/v1/mythic-plus/season-cutoffs"
        params = {
            'access_key': raider_io_api_key,
            'region': region
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data, None
        
    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
