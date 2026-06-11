# 🌍 IoT-Based Air Quality & Pollution Monitoring Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![IoT](https://img.shields.io/badge/IoT-Enabled-orange.svg)](https://en.wikipedia.org/wiki/Internet_of_things)

## 📌 Overview

An **industry-oriented IoT project** that simulates real-time air quality monitoring, pollution detection, and environmental data analysis. This system collects air quality parameters (CO₂, smoke, temperature, humidity), calculates Air Quality Index (AQI), generates alerts for unsafe conditions, and visualizes data through an interactive dashboard.

### 🎯 Key Features

- ✅ **Real-time Air Quality Monitoring** (Simulated sensor data)
- ✅ **AQI Calculation & Classification** (Good/Moderate/Poor/Unhealthy/Hazardous)
- ✅ **Interactive Web Dashboard** (Streamlit-based)
- ✅ **Automated Alert Generation** (Console & visual alerts)
- ✅ **Data Logging & Export** (CSV format)
- ✅ **Report Generation** (HTML & Text reports)
- ✅ **Chart Visualization** (Trends, distributions, comparisons)
- ✅ **Virtual Simulation** (No hardware required)

### 📊 Monitored Parameters

| Parameter | Range | Description |
|-----------|-------|-------------|
| Air Quality | 0-500 | Overall pollution level |
| Temperature | 15-45°C | Ambient temperature |
| Humidity | 20-90% | Relative humidity |
| Smoke Level | 0-500 ppm | Smoke/gas concentration |
| CO₂ Level | 350-2000 ppm | Carbon dioxide concentration |

---

## ❓ Problem Statement

Air pollution is a critical global health issue. According to the WHO, **7 million premature deaths** occur annually due to air pollution. Traditional monitoring stations are expensive and sparse. This project provides a **low-cost, real-time air quality monitoring solution** that can be deployed in:

- 🏙️ **Smart Cities** - Urban pollution mapping
- 🏭 **Industrial Areas** - Emission monitoring
- 🏫 **Schools & Colleges** - Student health protection
- 🏥 **Hospitals** - Sensitive patient care
- 🏠 **Smart Homes** - Indoor air quality

---

## 🏗️ System Architecture
```
┌─────────────────┐
│ Sensor Data │ (Simulated MQ135, DHT22)
│ Generation │
└────────┬────────┘
│
▼
┌─────────────────┐
│ AQI & Alert │ (Classification & threshold check)
│ Processing │
└────────┬────────┘
│
▼
┌─────────────────┐
│ Data Storage │ (CSV Logging)
│ & Export │
└────────┬────────┘
│
▼
┌─────────────────┐
│ Dashboard & │ (Streamlit Web Interface)
│ Visualization │
└─────────────────┘
```

### Data Flow

1. **Sensor Simulator** generates realistic air quality readings
2. **AQI Calculator** classifies pollution levels (0-500 scale)
3. **Alert Generator** triggers warnings for unsafe conditions
4. **Dashboard** displays real-time data and charts
5. **CSV Logger** saves all readings for analysis
6. **Report Generator** creates summary reports

---

## 🛠️ Tech Stack

### Languages & Frameworks
- **Python 3.8+** - Core programming language
- **Streamlit** - Web dashboard framework
- **Pandas** - Data manipulation & analysis
- **NumPy** - Numerical computations
- **Matplotlib** - Chart generation

### Libraries Used

- streamlit==1.28.0  # Web dashboard
- pandas==2.1.0      # Data processing
- numpy==1.24.3      # Numerical operations
- plotly==5.17.0     # Interactive charts
- altair==5.1.0      # Statistical visualizations
- matplotlib==3.7.2  # Static chart generation

## 📁 Project Structure
```
IoT-Air-Quality-Pollution-Monitoring-Dashboard/
│
├── app.py                          # Main console application
├── generate_outputs.py             # One-click output generator
├── run_simulation.py               # Quick start script
├── requirements.txt                # Python dependencies
│
├── simulation/
│   ├── sensor_simulator.py         # Fake sensor data generator
│
├── processing/
│   ├── aqi_calculator.py           # AQI calculation logic
│   ├── alert_generator.py          # Alert system
│
├── dashboard/
│   ├── streamlit_app.py            # Web dashboard
│
├── data/                           # Auto-generated CSV logs
│   ├── sensor_logs.csv
│   └── alerts_log.csv
│
├── outputs/                        # Generated outputs
│   ├── charts/                     # PNG chart files
│   ├── exports/                    # Exported CSV files
│   └── reports/                    # HTML/TXT reports
│
├── images/                         # Screenshots for README
│
└── README.md                       # Documentation
```

## 🚀 Installation & Setup

Prerequisites
Python 3.8 or higher installed
Git (optional, for version control)
VS Code or any Python IDE

Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/IoT-Air-Quality-Pollution-Monitoring-Dashboard.git
cd IoT-Air-Quality-Pollution-Monitoring-Dashboard

Step 2: Create Virtual Environment (Recommended)
# Windows
python -m venv venv
venv\Scripts\activate
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Run the Application
Choose your preferred mode:

# Option 1: Streamlit Dashboard (Recommended)
streamlit run dashboard/streamlit_app.py

# Option 2: Console Mode
python app.py

# Option 3: Quick Start (Menu driven)
python run_simulation.py

# Option 4: Generate all reports & charts
python generate_outputs.py

## 🖥️ How to Use
Dashboard Mode (Streamlit)
Run streamlit run dashboard/streamlit_app.py
Open browser at http://localhost:8501
```

# Use sidebar controls:
- Select Live Simulation for real-time data
- Select Test Scenarios for specific pollution levels
- Adjust update interval (1-10 seconds)

View:
- Live AQI status with color coding
- Temperature & humidity readings
- Interactive trend charts
- Alert notifications

Health recommendations
Console Mode
- Run python app.py
- Enter monitoring duration (seconds)
- Enter reading interval (seconds)
- Watch real-time sensor readings in terminal
- CSV logs saved automatically in data/ folder

## 📊 AQI Classification
| AQI Range | Category | Color | Health Impact |
| --------- | -------- | ----- | ------------- |
| 0-50 | Good | 🟢 Green | Air quality is satisfactory |
| 51-100 | Moderate | 🟡 Yellow | Acceptable air quality |
| 101-200 | Poor | 🟠 Orange | Sensitive groups may be affected |
| 201-300 | Unhealthy | 🔴 Red | Health effects for everyone |
| 301-500 | Hazardous | 🟣 Purple | Emergency health conditions |

# Alert Levels
- WARNING - Moderate pollution detected
- CRITICAL - Unhealthy air quality
- EMERGENCY - Hazardous conditions

## 🎯 Future Improvements
- Add GPS for location-based monitoring
- Implement mobile app notifications
- Add AI-based pollution prediction
- Support multiple sensor nodes (mesh network)
- Integrate real hardware (ESP32 + MQ135)
- Add database support (SQLite/PostgreSQL)
- Implement real-time email/SMS alerts
- Add historical data analytics

## 📚 Learning Outcomes
After completing this project, you will understand:
- ✅ IoT system architecture and data flow
- ✅ Sensor simulation and data generation
- ✅ AQI calculation and pollution classification
- ✅ Real-time dashboard development with Streamlit
- ✅ Data logging and CSV file handling
- ✅ Alert system implementation
- ✅ Report generation (HTML/TXT)
- ✅ Python project structuring for GitHub
- ✅ Virtual environment management
- ✅ Git version control best practices