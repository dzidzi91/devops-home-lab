import logging
import os
import socket
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

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

# 📊 METRICS

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "app_request_duration_seconds",
    "Request latency",
    ["endpoint"],
)

APP_INFO = Counter(
    "app_info",
    "Application info",
    ["app_name", "env", "version"],
)

# inicijalni info metric
APP_INFO.labels(APP_NAME, APP_ENV, APP_VERSION).inc()


# 📈 MIDDLEWARE za automatsko praćenje svih requesta

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    REQUEST_COUNT.labels(
        request.method,
        request.url.path,
        response.status_code
    ).inc()

    REQUEST_LATENCY.labels(request.url.path).observe(process_time)

    return response


# 📌 METRICS endpoint

@app.get("/metrics")
def metrics():
    return generate_latest()


# ================== EXISTING ENDPOINTS ==================

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