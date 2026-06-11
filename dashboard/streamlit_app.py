"""
streamlit_app.py
Main dashboard for Air Quality Monitoring
Run with: streamlit run dashboard/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.sensor_simulator import AirQualitySensorSimulator
from processing.aqi_calculator import AQICalculator
from processing.alert_generator import AlertGenerator

# Page configuration
st.set_page_config(
    page_title="Air Quality Monitoring Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stAlert {
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Temperature Box - Change this color */
    .temp-box {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 10px;
    }
    
    /* Humidity Box - Change this color */
    .humidity-box {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 10px;
    }
    
    /* Smoke Box - Change this color */
    .smoke-box {
        background: linear-gradient(135deg, #95E77E 0%, #49B82D 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 10px;
    }
    
    /* Air Quality Box - Dynamic colors based on AQI */
    .good-box {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .moderate-box {
        background: linear-gradient(135deg, #FFC107 0%, #FFB300 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .poor-box {
        background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .unhealthy-box {
        background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .hazardous-box {
        background: linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_history' not in st.session_state:
    st.session_state.data_history = []
if 'alert_history' not in st.session_state:
    st.session_state.alert_history = []
if 'simulator' not in st.session_state:
    st.session_state.simulator = AirQualitySensorSimulator()
if 'alert_gen' not in st.session_state:
    st.session_state.alert_gen = AlertGenerator()
if 'running' not in st.session_state:
    st.session_state.running = False

# Title and description
st.title("🌍 IoT-Based Air Quality & Pollution Monitoring Dashboard")
st.markdown("---")

# Sidebar controls
with st.sidebar:
    st.header("🎮 Control Panel")
    
    # Simulation mode selection
    simulation_mode = st.radio(
        "Select Simulation Mode",
        ["📈 Live Simulation", "📊 Test Scenarios"]
    )
    
    if simulation_mode == "📈 Live Simulation":
        update_interval = st.slider(
            "Update Interval (seconds)",
            min_value=1,
            max_value=10,
            value=2
        )
        
        if st.button("▶️ Start Monitoring", type="primary"):
            st.session_state.running = True
        if st.button("⏹️ Stop Monitoring"):
            st.session_state.running = False
        if st.button("🗑️ Clear Data"):
            st.session_state.data_history = []
            st.session_state.alert_history = []
            st.success("Data cleared!")
    
    else:  # Test Scenarios
        st.markdown("### Test Different Pollution Levels")
        scenario = st.selectbox(
            "Select Scenario",
            ["Normal (Good)", "Moderate Pollution", "Poor Air Quality", "Hazardous Conditions"]
        )
        
        if st.button("🔬 Generate Test Reading"):
            scenario_map = {
                "Normal (Good)": "normal",
                "Moderate Pollution": "moderate",
                "Poor Air Quality": "poor",
                "Hazardous Conditions": "hazardous"
            }
            reading = st.session_state.simulator.get_specific_scenario(scenario_map[scenario])
            st.session_state.data_history.append(reading)
            
            # Process and check alerts
            aqi_result = AQICalculator.calculate_aqi(reading["air_quality"])
            alert = st.session_state.alert_gen.check_and_alert(reading, aqi_result)
            if alert:
                st.session_state.alert_history.append(alert)
            
            st.success(f"✅ Generated {scenario} reading!")
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Info")
    st.metric("Total Readings", len(st.session_state.data_history))
    st.metric("Alerts Triggered", len(st.session_state.alert_history))

# Main content area
col1, col2, col3, col4 = st.columns(4)

# Display current readings if data exists
if st.session_state.data_history:
    latest_data = st.session_state.data_history[-1]
    aqi = AQICalculator.calculate_aqi(latest_data["air_quality"])
    
    # Color-coded AQI display
    aqi_color = aqi["category"].lower()
    with col1:
        box_class = f"{aqi_color.lower()}-box" if aqi_color in ["good", "moderate", "poor", "unhealthy", "hazardous"] else "metric-card"
        st.markdown(f"""
        <div class="{box_class}">
            <h3>🌬️ Air Quality</h3>
            <h1>{latest_data['air_quality']}</h1>
            <h3>{aqi['color']} {aqi['category']}</h3>
            <p>{aqi['message'][:50]}...</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌡️ Temperature</h3>
            <h1>{latest_data['temperature_c']}°C</h1>
            <p>{'Normal' if latest_data['temperature_c'] < 30 else 'High'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💧 Humidity</h3>
            <h1>{latest_data['humidity_percent']}%</h1>
            <p>{'Comfortable' if 40 <= latest_data['humidity_percent'] <= 70 else 'Uncomfortable'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💨 Smoke Level</h3>
            <h1>{latest_data['smoke_ppm']} ppm</h1>
            <p>{'Normal' if latest_data['smoke_ppm'] < 50 else 'Elevated'}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("👈 Click 'Start Monitoring' in the sidebar to begin collecting data!")

# Live simulation auto-update
if simulation_mode == "📈 Live Simulation" and st.session_state.running:
    placeholder = st.empty()
    for i in range(10):  # Run for 10 iterations or until stopped
        if not st.session_state.running:
            break
        
        # Generate new reading
        reading = st.session_state.simulator.get_all_readings()
        st.session_state.data_history.append(reading)
        
        # Calculate AQI and check alerts
        aqi_result = AQICalculator.calculate_aqi(reading["air_quality"])
        alert = st.session_state.alert_gen.check_and_alert(reading, aqi_result)
        if alert:
            st.session_state.alert_history.append(alert)
        
        # Update placeholder with rerun
        placeholder.empty()
        time.sleep(update_interval)
        st.rerun()

# Charts Section
st.markdown("---")
st.header("📈 Real-Time Data Visualization")

if len(st.session_state.data_history) > 1:
    # Create DataFrame from history
    df = pd.DataFrame(st.session_state.data_history)
    
    # Chart 1: Air Quality Trend
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['air_quality'],
            mode='lines+markers',
            name='Air Quality',
            line=dict(color='red', width=2),
            marker=dict(size=6)
        ))
        
        # Add threshold lines
        fig1.add_hline(y=50, line_dash="dash", line_color="green", 
                       annotation_text="Good Limit")
        fig1.add_hline(y=100, line_dash="dash", line_color="yellow",
                       annotation_text="Moderate Limit")
        fig1.add_hline(y=200, line_dash="dash", line_color="orange",
                       annotation_text="Poor Limit")
        
        fig1.update_layout(
            title="Air Quality Trend",
            xaxis_title="Time",
            yaxis_title="Air Quality Value (0-500)",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['temperature_c'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='orange', width=2)
        ))
        fig2.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['humidity_percent'],
            mode='lines+markers',
            name='Humidity',
            line=dict(color='blue', width=2)
        ))
        fig2.update_layout(
            title="Temperature & Humidity Trend",
            xaxis_title="Time",
            yaxis_title="Value",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 2: Smoke and CO2 Levels
    col3, col4 = st.columns(2)
    
    with col3:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df['timestamp'][-10:],
            y=df['smoke_ppm'][-10:],
            name='Smoke (ppm)',
            marker_color='red'
        ))
        fig3.update_layout(
            title="Smoke Levels (Last 10 readings)",
            xaxis_title="Time",
            yaxis_title="Smoke (ppm)",
            height=350
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        fig4 = px.line(df, x='timestamp', y='co2_ppm', 
                       title="CO2 Levels Trend",
                       labels={'timestamp': 'Time', 'co2_ppm': 'CO2 (ppm)'})
        fig4.add_hline(y=800, line_dash="dash", line_color="orange",
                       annotation_text="Poor Ventilation Threshold")
        fig4.update_layout(height=350)
        st.plotly_chart(fig4, use_container_width=True)

# Alerts Section
st.markdown("---")
st.header("🚨 Alert Log")

if st.session_state.alert_history:
    alert_df = pd.DataFrame(st.session_state.alert_history)
    alert_df = alert_df[['timestamp', 'alert_level', 'category', 'air_quality_value', 'message']]
    st.dataframe(alert_df, use_container_width=True)
else:
    st.info("✅ No alerts triggered. Air quality is within safe limits!")

# Health Recommendations
st.markdown("---")
st.header("💡 Health Recommendations")

if st.session_state.data_history:
    latest_aqi = st.session_state.data_history[-1]["air_quality"]
    recommendation = AQICalculator.get_health_recommendation(latest_aqi)
    
    aqi_category = AQICalculator.calculate_aqi(latest_aqi)["category"]
    
    if aqi_category == "Good":
        st.success(f"🟢 {recommendation}")
    elif aqi_category == "Moderate":
        st.info(f"🟡 {recommendation}")
    elif aqi_category == "Poor":
        st.warning(f"🟠 {recommendation}")
    else:
        st.error(f"🔴 {recommendation}")

# Data Export Section
st.markdown("---")
st.header("💾 Data Export")

if st.button("📥 Export Data to CSV"):
    if st.session_state.data_history:
        df_export = pd.DataFrame(st.session_state.data_history)
        csv = df_export.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"air_quality_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data to export!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
    <p>IoT-Based Air Quality Monitoring Dashboard | Real-time Pollution Tracking | Environmental Monitoring System</p>
    <p>Data is simulated for demonstration purposes</p>
</div>
""", unsafe_allow_html=True)