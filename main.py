from fastapi import FastAPI
import psutil
from datetime import datetime

app = FastAPI(title="System Monitoring Tool")


# Root endpoint (for testing)
@app.get("/")
def home():
    return {
        "message": "System Monitoring Tool Running",
        "status": "OK"
    }


# Metrics endpoint (MAIN API)
@app.get("/metrics")
def get_metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }