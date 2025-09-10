import streamlit as st
import uuid
from weather_service import WeatherService

# Initialize backend service
try:
    weather_service = WeatherService()
except ValueError as e:
    st.error(str(e))
    st.stop()

# UI
st.title("Weather App")

city = st.text_input("Enter city name (e.g., 'New York')")

if st.button("Get Weather"):
    if city:
        correlation_id = str(uuid.uuid4())  # Unique ID for this request
        try:
            weather_data = weather_service.get_weather_data(city, correlation_id)
            st.success(f"Weather in {city}:")
            st.write(f"Temperature: {weather_data['temperature']} °C")
            st.write(f"Wind Speed: {weather_data['wind_speed']} m/s")
            st.write(f"Humidity: {weather_data['humidity']} %")

            weather_service.save_to_influxdb(weather_data, city, correlation_id)
        except ValueError as e:
            st.error(str(e))
    else:
        st.warning("Please enter a city name.")
