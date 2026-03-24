
from fastapi import FastAPI
import psutil
from datetime import datetime

app = FastAPI(title="System Monitoring Tool")

@app.get("/")
def home():
    return {
        "message": "System Monitoring Tool Running",
        "status": "OK"
    }

@app.get("/metrics")
def metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    alerts = []
    status = "Healthy"

    # Alert logic
    if cpu > 80:
        alerts.append("High CPU usage")
    if memory > 80:
        alerts.append("High Memory usage")
    if disk > 80:
        alerts.append("High Disk usage")

    # Status logic
    if len(alerts) == 1:
        status = "Warning"
    elif len(alerts) >= 2:
        status = "Critical"

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "metrics": {
            "cpu": cpu,
            "memory": memory,
            "disk": disk
        },
        "alerts": alerts
    }