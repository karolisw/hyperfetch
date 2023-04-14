import logging
from time import time
from typing import Union
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorClient
from config.auth_connection import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from config.mongodb import db
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))

async def connect_to_motor() -> None:
    logger.info("Connecting to mongoDB...")
    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   username='myUserAdmin',
                                   password='SkoleBole69',
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logging.info("Connected！")


async def close_motor_connection() -> None:
    logging.info("Disconnecting from mongoDB...")
    db.client.close()
    logging.info("Disconnected.")


def get_time(seconds_precision=True) -> Union[int, float]:
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())