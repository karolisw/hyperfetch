import os
import uvicorn as uvicorn
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.routes.run_route import router
from src.config.auth_connection import ALLOWED_HOSTS
from src.utils.db_utils import connect_to_motor, close_motor_connection

app = FastAPI()


class CheckOriginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        allowed_origins = ALLOWED_HOSTS
        origin = request.headers.get("Origin")
        if origin not in allowed_origins:
            return Response("Not allowed origin", status_code=403)
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["hyperfetch-backend.azurewebsites.net"]
)
app.add_middleware(
    CheckOriginMiddleware
)

app.add_event_handler("startup", connect_to_motor)
app.add_event_handler("shutdown", close_motor_connection)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 443)))
