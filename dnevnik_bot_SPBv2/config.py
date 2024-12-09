import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG")

TOKEN = os.getenv("TEST_TOKEN") if DEBUG == "True" else os.getenv("TOKEN")
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
API_URL = f"{API_HOST}:{API_PORT}"

REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_USER = os.getenv("REDIS_USER")
DATA_FILE = os.getenv("DATA_FILE")


REDIS_URL = (
	f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)
