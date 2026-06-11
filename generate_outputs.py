"""
generate_outputs.py
ONE CLICK SOLUTION - Generates all reports, charts, and exports
Run this file to populate all output folders with data
Run with: python generate_outputs.py
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import project modules
from simulation.sensor_simulator import AirQualitySensorSimulator
from processing.aqi_calculator import AQICalculator
from processing.alert_generator import AlertGenerator

def create_directories():
    """Create all necessary directories"""
    dirs = [
        'data',
        'outputs',
        'outputs/charts',
        'outputs/exports',
        'outputs/reports',
        'images'
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    print("✅ Directories created")

def generate_sample_data():
    """Generate sample sensor data for 24 hours"""
    print("\n📊 Generating 24 hours of sample data...")
    
    simulator = AirQualitySensorSimulator()
    data = []
    
    # Generate data for 24 hours (1 reading per hour)
    start_time = datetime.now() - timedelta(hours=24)
    
    for i in range(25):  # 25 readings for 24 hours
        timestamp = start_time + timedelta(hours=i)
        
        # Create different scenarios throughout the day
        hour = timestamp.hour
        
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            # Rush hours - higher pollution
            scenario = "moderate"
        elif 22 <= hour or hour <= 5:
            # Night time - lower pollution
            scenario = "normal"
        else:
            # Day time - variable
            scenario = "normal" if i % 3 != 0 else "poor"
        
        reading = simulator.get_specific_scenario(scenario)
        reading['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        data.append(reading)
    
    print(f"✅ Generated {len(data)} readings")
    return data

def save_to_csv(data, filename="outputs/exports/sensor_data_export.csv"):
    """Save data to CSV file"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ CSV saved: {filename}")
    return df

def generate_charts(df):
    """Generate and save charts"""
    print("\n📈 Generating charts...")
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Chart 1: Air Quality Trend
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(df)), df['air_quality'], marker='o', linewidth=2, color='red', markersize=4)
    plt.axhline(y=50, color='green', linestyle='--', label='Good Limit (50)')
    plt.axhline(y=100, color='yellow', linestyle='--', label='Moderate Limit (100)')
    plt.axhline(y=200, color='orange', linestyle='--', label='Poor Limit (200)')
    plt.fill_between(range(len(df)), 0, 50, alpha=0.2, color='green', label='Good')
    plt.fill_between(range(len(df)), 50, 100, alpha=0.2, color='yellow', label='Moderate')
    plt.fill_between(range(len(df)), 100, 200, alpha=0.2, color='orange', label='Poor')
    plt.fill_between(range(len(df)), 200, 500, alpha=0.2, color='red', label='Unhealthy/Hazardous')
    plt.xlabel('Reading Number', fontsize=12)
    plt.ylabel('Air Quality Value', fontsize=12)
    plt.title('Air Quality Trend - 24 Hour Analysis', fontsize=14, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/charts/air_quality_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Chart 1: Air Quality Trend saved")
    
    # Chart 2: Temperature vs Humidity
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax1.set_xlabel('Reading Number', fontsize=12)
    ax1.set_ylabel('Temperature (°C)', color='tab:red', fontsize=12)
    ax1.plot(range(len(df)), df['temperature_c'], color='tab:red', marker='s', linewidth=2, markersize=4, label='Temperature')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Humidity (%)', color='tab:blue', fontsize=12)
    ax2.plot(range(len(df)), df['humidity_percent'], color='tab:blue', marker='^', linewidth=2, markersize=4, label='Humidity')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    
    plt.title('Temperature and Humidity Relationship', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig('outputs/charts/temp_humidity_chart.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Chart 2: Temperature vs Humidity saved")
    
    # Chart 3: Pollution Distribution (Pie Chart)
    categories = []
    for value in df['air_quality']:
        if value <= 50:
            categories.append('Good')
        elif value <= 100:
            categories.append('Moderate')
        elif value <= 200:
            categories.append('Poor')
        elif value <= 300:
            categories.append('Unhealthy')
        else:
            categories.append('Hazardous')
    
    category_counts = pd.Series(categories).value_counts()
    
    colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336', '#9C27B0']
    plt.figure(figsize=(8, 8))
    plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', 
            colors=colors[:len(category_counts)], startangle=90)
    plt.title('Air Quality Distribution', fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.savefig('outputs/charts/pollution_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Chart 3: Pollution Distribution saved")
    
    # Chart 4: Smoke and CO2 Levels
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(df)), df['smoke_ppm'], alpha=0.7, label='Smoke (ppm)', color='orange', width=0.4)
    plt.bar(range(len(df)), df['co2_ppm']/10, alpha=0.7, label='CO2/10 (ppm)', color='red', width=0.4)
    plt.xlabel('Reading Number', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.title('Smoke and CO2 Levels', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/charts/smoke_co2_levels.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Chart 4: Smoke and CO2 Levels saved")

def generate_report(df, alert_count):
    """Generate a comprehensive HTML report"""
    print("\n📄 Generating report...")
    
    # Calculate statistics
    avg_air = df['air_quality'].mean()
    max_air = df['air_quality'].max()
    min_air = df['air_quality'].min()
    avg_temp = df['temperature_c'].mean()
    avg_humidity = df['humidity_percent'].mean()
    
    # Categorize
    good_count = len(df[df['air_quality'] <= 50])
    moderate_count = len(df[(df['air_quality'] > 50) & (df['air_quality'] <= 100)])
    poor_count = len(df[(df['air_quality'] > 100) & (df['air_quality'] <= 200)])
    unhealthy_count = len(df[(df['air_quality'] > 200) & (df['air_quality'] <= 300)])
    hazardous_count = len(df[df['air_quality'] > 300])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Air Quality Monitoring Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1000px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #555;
                margin-top: 30px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }}
            .stat-card.good {{ background: linear-gradient(135deg, #4CAF50, #45a049); }}
            .stat-card.moderate {{ background: linear-gradient(135deg, #FFC107, #FFB300); }}
            .stat-card.poor {{ background: linear-gradient(135deg, #FF9800, #F57C00); }}
            .stat-card.unhealthy {{ background: linear-gradient(135deg, #F44336, #D32F2F); }}
            .stat-card.hazardous {{ background: linear-gradient(135deg, #9C27B0, #7B1FA2); }}
            .stat-number {{
                font-size: 36px;
                font-weight: bold;
                margin: 10px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 Air Quality Monitoring Report</h1>
            <p style="text-align: center; color: #666;">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>📊 Summary Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div>Average Air Quality</div>
                    <div class="stat-number">{avg_air:.1f}</div>
                </div>
                <div class="stat-card">
                    <div>Max Air Quality</div>
                    <div class="stat-number">{max_air}</div>
                </div>
                <div class="stat-card">
                    <div>Min Air Quality</div>
                    <div class="stat-number">{min_air}</div>
                </div>
                <div class="stat-card">
                    <div>Average Temperature</div>
                    <div class="stat-number">{avg_temp:.1f}°C</div>
                </div>
                <div class="stat-card">
                    <div>Average Humidity</div>
                    <div class="stat-number">{avg_humidity:.1f}%</div>
                </div>
                <div class="stat-card">
                    <div>Total Alerts</div>
                    <div class="stat-number">{alert_count}</div>
                </div>
            </div>
            
            <h2>📈 Air Quality Distribution</h2>
            <div class="stats-grid">
                <div class="stat-card good">
                    <div>Good (0-50)</div>
                    <div class="stat-number">{good_count}</div>
                    <div>{good_count/len(df)*100:.1f}%</div>
                </div>
                <div class="stat-card moderate">
                    <div>Moderate (51-100)</div>
                    <div class="stat-number">{moderate_count}</div>
                    <div>{moderate_count/len(df)*100:.1f}%</div>
                </div>
                <div class="stat-card poor">
                    <div>Poor (101-200)</div>
                    <div class="stat-number">{poor_count}</div>
                    <div>{poor_count/len(df)*100:.1f}%</div>
                </div>
                <div class="stat-card unhealthy">
                    <div>Unhealthy (201-300)</div>
                    <div class="stat-number">{unhealthy_count}</div>
                    <div>{unhealthy_count/len(df)*100:.1f}%</div>
                </div>
                <div class="stat-card hazardous">
                    <div>Hazardous (300+)</div>
                    <div class="stat-number">{hazardous_count}</div>
                    <div>{hazardous_count/len(df)*100:.1f}%</div>
                </div>
            </div>
            
            <h2>📋 Sample Data (Last 10 Readings)</h2>
            {df.tail(10).to_html(index=False, classes='data-table')}
            
            <h2>💡 Recommendations</h2>
            <ul>
                <li><strong>Good Days:</strong> Enjoy outdoor activities</li>
                <li><strong>Moderate Days:</strong> Sensitive individuals should limit prolonged outdoor exertion</li>
                <li><strong>Poor Days:</strong> Reduce outdoor activities, keep windows closed</li>
                <li><strong>Unhealthy Days:</strong> Avoid outdoor activities, wear masks if going out</li>
                <li><strong>Hazardous Days:</strong> Stay indoors, use air purifiers</li>
            </ul>
            
            <div class="footer">
                <p>IoT-Based Air Quality Monitoring System | Environmental Data Analysis</p>
                <p>This report was automatically generated by the Air Quality Monitoring Dashboard</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save HTML report
    report_path = 'outputs/reports/air_quality_report.html'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ HTML Report saved: {report_path}")
    
    # Also save text report
    txt_report_path = 'outputs/reports/summary_report.txt'
    with open(txt_report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("AIR QUALITY MONITORING REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Readings: {len(df)}\n")
        f.write(f"Average Air Quality: {avg_air:.1f}\n")
        f.write(f"Max Air Quality: {max_air}\n")
        f.write(f"Min Air Quality: {min_air}\n")
        f.write(f"Average Temperature: {avg_temp:.1f}°C\n")
        f.write(f"Average Humidity: {avg_humidity:.1f}%\n")
        f.write(f"Total Alerts: {alert_count}\n\n")
        f.write("Air Quality Distribution:\n")
        f.write(f"  Good: {good_count} ({good_count/len(df)*100:.1f}%)\n")
        f.write(f"  Moderate: {moderate_count} ({moderate_count/len(df)*100:.1f}%)\n")
        f.write(f"  Poor: {poor_count} ({poor_count/len(df)*100:.1f}%)\n")
        f.write(f"  Unhealthy: {unhealthy_count} ({unhealthy_count/len(df)*100:.1f}%)\n")
        f.write(f"  Hazardous: {hazardous_count} ({hazardous_count/len(df)*100:.1f}%)\n")
    
    print(f"✅ Text Report saved: {txt_report_path}")

def main():
    """Main function to generate all outputs"""
    print("\n" + "=" * 60)
    print("   AIR QUALITY MONITORING - OUTPUT GENERATOR")
    print("   One-click solution for all reports and charts")
    print("=" * 60)
    
    # Create directories
    create_directories()
    
    # Generate sample data
    data = generate_sample_data()
    
    # Save to CSV
    df = save_to_csv(data)
    
    # Generate charts
    generate_charts(df)
    
    # Generate alerts summary
    alert_gen = AlertGenerator()
    alert_count = 0
    for reading in data:
        aqi_result = AQICalculator.calculate_aqi(reading["air_quality"])
        alert = alert_gen.check_and_alert(reading, aqi_result)
        if alert:
            alert_count += 1
    
    # Generate report
    generate_report(df, alert_count)
    
    print("\n" + "=" * 60)
    print("✅ ALL OUTPUTS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📁 Outputs saved in:")
    print("   📊 Charts: outputs/charts/")
    print("      - air_quality_trend.png")
    print("      - temp_humidity_chart.png")
    print("      - pollution_distribution.png")
    print("      - smoke_co2_levels.png")
    print("   📄 Reports: outputs/reports/")
    print("      - air_quality_report.html (Open in browser)")
    print("      - summary_report.txt")
    print("   💾 Exports: outputs/exports/")
    print("      - sensor_data_export.csv")
    print("\n💡 Tip: Open the HTML report in your browser for a formatted report!")
    print("=" * 60)

if __name__ == "__main__":
    # Check if matplotlib is installed
    try:
        import matplotlib
    except ImportError:
        print("⚠️ matplotlib not found. Installing...")
        os.system("pip install matplotlib")
        print("✅ matplotlib installed. Run the script again.")
        sys.exit(0)
    
    main()