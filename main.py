from fastapi import FastAPI
from utils.common import *
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from routes.run_route import router
from config.core import ALLOWED_HOSTS
from utils.db_utils import connect_to_motor, close_motor_connection
from settings import api_settings as settings
from middleware import request_handler

#config = dotenv_values(".env")
app = FastAPI(title=settings.title)
#storage = get_yaml_val("config/db_config.yml", "storage")


if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]  # type: ignore
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_event_handler("startup", connect_to_motor)
app.add_event_handler("shutdown", close_motor_connection)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

'''
@app.on_event("startup")
def startup_db_client() -> None:
    #app.mongodb_client = MotorClient(config["DB_URI"])
    app.mongodb_client = motor.AsyncIOMotorClient(storage)
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client() -> None:
    app.mongodb_client.close()
'''

app.include_router(router)
