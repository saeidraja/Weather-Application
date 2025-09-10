import os
import logging
import requests
import uuid
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom JSON formatter with correlation ID
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['correlation_id'] = getattr(record, 'correlation_id', 'N/A')

# Set up logging
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
formatter = CustomJsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s %(correlation_id)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.influx_url = os.getenv("INFLUXDB_URL", "http://localhost:8086")
        self.influx_token = os.getenv("INFLUXDB_TOKEN")
        self.influx_org = os.getenv("INFLUXDB_ORG")
        self.influx_bucket = os.getenv("INFLUXDB_BUCKET")

        if not self.api_key:
            logger.critical("OPENWEATHER_API_KEY environment variable not set")
            raise ValueError("OPENWEATHER_API_KEY environment variable not set")
        if not self.influx_token:
            logger.critical("INFLUXDB_TOKEN environment variable not set")
            raise ValueError("INFLUXDB_TOKEN environment variable not set")
        if not self.influx_org:
            logger.critical("INFLUXDB_ORG environment variable not set")
            raise ValueError("INFLUXDB_ORG environment variable not set")
        if not self.influx_bucket:
            logger.critical("INFLUXDB_BUCKET environment variable not set")
            raise ValueError("INFLUXDB_BUCKET environment variable not set")

        # Initialize InfluxDB client
        try:
            self.client = InfluxDBClient(url=self.influx_url, token=self.influx_token, org=self.influx_org)
            buckets_api = self.client.buckets_api()
            if not buckets_api.find_bucket_by_name(self.influx_bucket):
                logger.info("Creating InfluxDB bucket", extra={"bucket": self.influx_bucket})
                buckets_api.create_bucket(bucket_name=self.influx_bucket)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            logger.info("Connected to InfluxDB", extra={"bucket": self.influx_bucket})
        except Exception as e:
            logger.critical("Failed to connect to InfluxDB", extra={"error": str(e)})
            raise ValueError(f"Failed to connect to InfluxDB: {e}")

    def get_weather_data(self, city: str, correlation_id: str = None) -> dict:
        """
        Fetch weather data from OpenWeatherMap API.
        """
        correlation_id = correlation_id or str(uuid.uuid4())
        logger.debug("Starting weather data fetch", extra={"city": city, "correlation_id": correlation_id})
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            weather_info = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            logger.info("Successfully fetched weather data", extra={"city": city, "data": weather_info, "correlation_id": correlation_id})
            return weather_info
        except requests.RequestException as e:
            logger.error("Failed to fetch weather data", extra={"city": city, "error": str(e), "correlation_id": correlation_id})
            raise ValueError(f"Error fetching weather data: {e}")

    def save_to_influxdb(self, data: dict, city: str, correlation_id: str = None):
        """
        Save weather data to InfluxDB v2.
        """
        correlation_id = correlation_id or str(uuid.uuid4())
        logger.debug("Saving data to InfluxDB", extra={"city": city, "correlation_id": correlation_id})
        try:
            point = Point("weather") \
                .tag("city", city) \
                .field("temperature", float(data["temperature"])) \
                .field("humidity", float(data["humidity"])) \
                .field("wind_speed", float(data["wind_speed"])) \
                .time(datetime.utcnow(), WritePrecision.NS)
            self.write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=point)
            logger.info("Successfully saved data to InfluxDB", extra={"city": city, "data": data, "correlation_id": correlation_id})
        except Exception as e:
            logger.error("Failed to save data to InfluxDB", extra={"city": city, "error": str(e), "correlation_id": correlation_id})
            raise ValueError(f"Failed to save data to InfluxDB: {e}")
