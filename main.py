from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.run_route import router
from config.auth_connection import ALLOWED_HOSTS
from utils.db_utils import connect_to_motor, close_motor_connection


app = FastAPI()

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["http://localhost:5173"]  # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("ALLOWED HOSTS: ", ALLOWED_HOSTS)
app.add_event_handler("startup", connect_to_motor)
app.add_event_handler("shutdown", close_motor_connection)


app.include_router(router)
