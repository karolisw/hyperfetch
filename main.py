from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routes.run_route import router
from src.config.auth_connection import ALLOWED_HOSTS
from src.utils.db_utils import connect_to_motor, close_motor_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_motor)
app.add_event_handler("shutdown", close_motor_connection)


app.include_router(router)