from fastapi import FastAPI
from dotenv import dotenv_values
from motor import MotorClient
from routes.run_route import router

config = dotenv_values(".env")
app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MotorClient(config["DB_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
