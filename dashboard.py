import streamlit as st
import psutil
import time
import pandas as pd
import platform
import os

# Page config
st.set_page_config(page_title="System Monitor", layout="wide")

st.title("💻 Advanced System Monitoring Dashboard")

# Sidebar
st.sidebar.header("⚙️ Settings")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 5, 2)

# System Info
st.sidebar.markdown("### 💻 System Info")
st.sidebar.write(f"OS: {platform.system()}")
st.sidebar.write(f"Processor: {platform.processor()}")

# Placeholder
placeholder = st.empty()

# Data storage
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["CPU", "Memory", "Disk"])

while True:
    # System stats
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    # Cross-platform disk usage (BEST WAY)
    disk = psutil.disk_usage(os.path.abspath(os.sep)).percent

    # Store data
    new_row = {"CPU": cpu, "Memory": memory, "Disk": disk}
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )

    # Keep last 20 records
    if len(st.session_state.data) > 20:
        st.session_state.data = st.session_state.data.iloc[-20:]

    with placeholder.container():
        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("🧠 CPU Usage", f"{cpu}%")
        col2.metric("💾 Memory Usage", f"{memory}%")
        col3.metric("🗄️ Disk Usage", f"{disk}%")

        # Alerts
        if cpu > 80:
            st.error("🚨 High CPU Usage!")
        elif cpu > 50:
            st.warning("⚠️ Moderate CPU Usage")
        else:
            st.success("✅ CPU Normal")

        if memory > 80:
            st.warning("⚠️ High Memory Usage!")

        if disk > 80:
            st.warning("⚠️ Disk Almost Full!")

        # Chart
        st.subheader("📊 Usage Trends")
        st.line_chart(st.session_state.data)

        # Top Processes (FIXED VERSION 🔥)
        st.subheader("🔥 Top Processes (by CPU usage)")

        processes = []

        for p in psutil.process_iter(['name']):
            try:
                cpu_usage = p.cpu_percent(interval=0.1)
                processes.append({
                    "name": p.info['name'],
                    "cpu_percent": cpu_usage
                })
            except:
                pass

        top_processes = sorted(
            processes,
            key=lambda x: x['cpu_percent'],
            reverse=True
        )[:5]

        st.table(top_processes)

    time.sleep(refresh_rate)