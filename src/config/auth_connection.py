import os
#from dotenv import load_dotenv
#load_dotenv(".env") # removed for deploying

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
MONGODB_URL = os.getenv('MONGODB_URL')
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
