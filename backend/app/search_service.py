import requests

ALPHA_VANTAGE_API_KEY = "3PDWBSV8VU44ZC0J"  

def search_stocks_alpha_vantage(query: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": query,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        matches = data.get("bestMatches", [])

        results = []
        for match in matches:
            symbol = match.get("1. symbol", "")
            name = match.get("2. name", "")
            if symbol and name:
                results.append({
                    "symbol": symbol,
                    "name": name,
                })

        return results

    except requests.RequestException as e:
        print("Error contacting Alpha Vantage:", e)
        return []
