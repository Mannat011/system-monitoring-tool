import streamlit as st
import requests
import time
import plotly.express as px

# Page settings
st.set_page_config(page_title="System Monitor", layout="wide")

st.title("💻 System Monitoring Dashboard")

# Sidebar controls
st.sidebar.title("⚙️ Controls")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 5, 2)

# Backend URL
BASE_URL = "https://system-monitoring-tool.onrender.com"
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

    # 🚨 Alerts
    if cpu > 80:
        st.warning("⚠️ High CPU Usage!")

    if memory > 80:
        st.warning("⚠️ High Memory Usage!")

    if disk > 80:
        st.warning("⚠️ Disk Almost Full!")

    # 📊 Store history for graph
    if "cpu_history" not in st.session_state:
        st.session_state.cpu_history = []

    st.session_state.cpu_history.append(cpu)

    # Keep only last 20 values
    st.session_state.cpu_history = st.session_state.cpu_history[-20:]

    # 📈 Create graph
    fig = px.line(st.session_state.cpu_history, title="CPU Usage Trend")
    st.plotly_chart(fig)

    # 🕒 Timestamp
    st.write("Last Updated:", data["timestamp"])

except:
    st.error("⚠️ Backend not running!")

# Auto refresh
time.sleep(refresh_rate)
st.rerun()