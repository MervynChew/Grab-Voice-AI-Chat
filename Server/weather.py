import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> str:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            return f"The current weather in {city} is {weather} with a temperature of {temperature}°C (feels like {feels_like}°C)."
        else:
            return f"Could not retrieve weather for '{city}'. Please make sure the city name is correct."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
