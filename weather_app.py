import tkinter as tk
from tkinter import messagebox
import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        geo_response = requests.get(GEOCODE_URL, params={"name": city, "count": 1}, timeout=5)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            messagebox.showerror("Error", "City not found.")
            return

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        name = location["name"]
        country = location.get("country", "")

        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
            "wind_speed_unit": "ms"
        }
        weather_response = requests.get(WEATHER_URL, params=weather_params, timeout=5)
        weather_data = weather_response.json()

        current = weather_data["current"]
        temp = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        code = current["weather_code"]

        def describe(code):
            if code == 0: return "Clear sky ☀️"
            elif code <= 3: return "Partly cloudy ⛅"
            elif code <= 48: return "Foggy 🌫️"
            elif code <= 67: return "Rainy 🌧️"
            elif code <= 77: return "Snowy ❄️"
            elif code <= 82: return "Rain showers 🌦️"
            elif code <= 99: return "Thunderstorm ⛈️"
            return "Unknown"

        result = (
            f"📍 {name}, {country}\n"
            f"Temp: {temp}°C (Feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind} m/s\n"
            f"Weather: {describe(code)}"
        )
        result_label.config(text=result)

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Network Error", "No internet connection.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Weather App")
root.geometry("360x300")
root.resizable(False, False)

tk.Label(root, text="🌤 Weather App", font=("Helvetica", 16, "bold")).pack(pady=10)

city_entry = tk.Entry(root, font=("Helvetica", 13), width=22)
city_entry.pack(pady=5)
city_entry.bind("<Return>", lambda e: get_weather())

tk.Button(root, text="Get Weather", command=get_weather,
          font=("Helvetica", 11), bg="#4A90D9", fg="white", padx=10).pack(pady=8)

result_label = tk.Label(root, text="", font=("Helvetica", 12),
                        justify="left", wraplength=320)
result_label.pack(pady=10)

root.mainloop()