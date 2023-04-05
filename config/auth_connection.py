import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings

API_V1_STR = "/api"
load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", "http://localhost:5173"))

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/runs?authSource=admin")
MONGO_DB = os.getenv("MONGO_DB", "runs")

database_name = MONGO_DB
# database_name = "runs"
run_collection_name = "run"
user_collection_name = "user"