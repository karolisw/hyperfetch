import os

# Uncomment to run tests
ALLOWED_HOSTS = "https://hyperfetch.online"
MONGODB_URL="mongodb+srv://admin:adminKaroline12@hyperfetch.zxjvuqd.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB="hyperfetch"
MONGO_COLLECTION="runs"

'''ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
MONGODB_URL = os.environ.get("MONGODB_URL")
MONGO_DB = os.environ.get("MONGO_DB")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")'''
