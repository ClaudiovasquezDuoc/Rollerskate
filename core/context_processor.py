import requests

def temperatura_clima(request):
    try:
        # Puedes cambiar las coordenadas por las de tu ciudad (ej: Santiago)
        lat = -33.45694
        lon = -70.64827

        url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'

        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            valor = float(data['current_weather']['temperature'])
            return {'temperatura_clima': round(valor, 2)}
    except Exception as e:
        print(f"Error: {e}")
    
    return {'temperatura_clima': 'No disponible'}