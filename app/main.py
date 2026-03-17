import logging
import os
import socket
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("devops-platform")

APP_NAME = os.getenv("APP_NAME", "devops-platform")
APP_ENV = os.getenv("APP_ENV", "dev")
APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(
    title="DevOps Platform",
    version=APP_VERSION,
)


@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {
        "message": "DevOps Platform Running",
        "app": APP_NAME,
        "env": APP_ENV,
        "version": APP_VERSION,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/version")
def version():
    return {"version": APP_VERSION}


@app.get("/info")
def info():
    return {
        "app": APP_NAME,
        "env": APP_ENV,
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
    }