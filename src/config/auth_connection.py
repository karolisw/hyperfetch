import os
#from dotenv import load_dotenv
#load_dotenv(".env") # removed for deploying

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
MONGODB_URL = os.environ.get("MONGODB_URL")
MONGO_DB = os.environ.get("MONGO_DB")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")
