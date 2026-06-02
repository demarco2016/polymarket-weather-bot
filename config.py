import os
from dotenv import load_dotenv

load_dotenv()

# Forecast
CITIES = [
    "New York", "London", "Tokyo", "Sydney",
    "Dubai", "Paris", "Berlin", "Mumbai",
    "Shanghai", "São Paulo", "Cairo", "Moscow",
    "Toronto", "Mexico City", "Istanbul", "Seoul",
    "Bangkok", "Lagos", "Buenos Aires", "Jakarta"
]
FORECAST_SOURCES = ["ECMWF", "HRRR", "METAR"]
CALIBRATION_INTERVAL = 30

# Polymarket
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CLOB_API_KEY = os.getenv("CLOB_API_KEY")
CLOB_API_SECRET = os.getenv("CLOB_API_SECRET")
CLOB_API_PASSPHRASE = os.getenv("CLOB_API_PASSPHRASE")
FUNDER_ADDRESS = os.getenv("FUNDER_ADDRESS")
SIGNATURE_TYPE = int(os.getenv("SIGNATURE_TYPE", "0"))
BUILDER_CODE = os.getenv("BUILDER_CODE")

CLOB_HOST = "https://clob.polymarket.com"
CHAIN_ID = 137

# Trading
MIN_EV = float(os.getenv("MIN_EV", "0.05"))
KELLY_FRACTION = float(os.getenv("KELLY_FRACTION", "0.25"))
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "100"))
