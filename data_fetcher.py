import requests

def fetch_data():
    url = "TU_URL_API_AQUI"  # Cambia por la URL de tu API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "best_bid": data['bids'][0][0],
            "best_ask": data['asks'][0][0]
        }
    else:
        return {"error": "No se pudo obtener la data"}
