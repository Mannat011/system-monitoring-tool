# System Monitoring Tool

A real-time system monitoring tool built using FastAPI and Python.

## Features
- CPU, Memory, Disk monitoring
- Alert detection system
- Health status (Healthy, Warning, Critical)
- REST API endpoints

## Tech Stack
- Python
- FastAPI
- psutil

## Run Locally
pip install fastapi uvicorn psutil
python -m uvicorn main:app --reload

## API Endpoints
- `/` → Health check
- `/metrics` → System metrics

## Sample Output
{
  "status": "Healthy",
  "alerts": [],
  "cpu": 10,
  "memory": 40,
  "disk": 50
}