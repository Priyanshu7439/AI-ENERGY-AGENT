import requests

API_KEY = "5a3bad839da0e5d24423fec732f622d1"

def get_temperature(city="kolkata"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        return data["main"]["temp"]

    except:
        return None