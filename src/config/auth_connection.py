import os

# Used in dev and for tests
from dotenv import load_dotenv
load_dotenv()

# Will find environment variables from Azure when in prod
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
MONGODB_URL = os.environ.get("MONGODB_URL")
MONGO_DB = os.environ.get("MONGO_DB")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")
