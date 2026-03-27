import plotly.express as px
import streamlit as st
import requests
import time

# Page settings
st.set_page_config(page_title="System Monitor", layout="wide")

st.title("💻 System Monitoring Dashboard")

# Backend URL
BASE_URL = "http://127.0.0.1:8000"

# Create columns
col1, col2, col3 = st.columns(3)

try:
    # Fetch data from backend
    response = requests.get(f"{BASE_URL}/metrics")
    data = response.json()

    cpu = data["cpu"]
    memory = data["memory"]
    disk = data["disk"]

    # Display metrics
    col1.metric("CPU Usage", f"{cpu}%")
    col2.metric("Memory Usage", f"{memory}%")
    col3.metric("Disk Usage", f"{disk}%")

except:
    st.error("⚠️ Backend not running!")
# Store history
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []

st.session_state.cpu_history.append(cpu)

# Keep last 20 values
st.session_state.cpu_history = st.session_state.cpu_history[-20:]

# Create graph
fig = px.line(st.session_state.cpu_history, title="CPU Usage Trend")
st.plotly_chart(fig)
# Auto refresh every 2 seconds
time.sleep(2)
st.rerun()