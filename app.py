"""
app.py
Main entry point for the Air Quality Monitoring System
Run with: python app.py
"""

import os
import sys
import time
import csv
from datetime import datetime

# Import custom modules
from simulation.sensor_simulator import AirQualitySensorSimulator
from processing.aqi_calculator import AQICalculator
from processing.alert_generator import AlertGenerator

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ['data', 'outputs', 'outputs/charts', 'outputs/reports', 'outputs/exports']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created successfully")

def log_to_csv(data, filename="data/sensor_logs.csv"):
    """Log sensor data to CSV file"""
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'air_quality', 'temperature_c', 'humidity_percent', 
                     'smoke_ppm', 'co2_ppm', 'aqi_category', 'alert_status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

def generate_report(data_history, alert_history, duration_seconds):
    """Generate summary report"""
    report_filename = f"outputs/reports/air_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_filename, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("AIR QUALITY MONITORING REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Monitoring Duration: {duration_seconds} seconds\n")
        f.write(f"Total Readings: {len(data_history)}\n")
        f.write(f"Total Alerts: {len(alert_history)}\n\n")
        
        if data_history:
            # Calculate statistics
            avg_air_quality = sum(d['air_quality'] for d in data_history) / len(data_history)
            max_air_quality = max(d['air_quality'] for d in data_history)
            min_air_quality = min(d['air_quality'] for d in data_history)
            
            avg_temp = sum(d['temperature_c'] for d in data_history) / len(data_history)
            avg_humidity = sum(d['humidity_percent'] for d in data_history) / len(data_history)
            
            f.write("STATISTICS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Average Air Quality: {avg_air_quality:.1f}\n")
            f.write(f"Max Air Quality: {max_air_quality}\n")
            f.write(f"Min Air Quality: {min_air_quality}\n")
            f.write(f"Average Temperature: {avg_temp:.1f}°C\n")
            f.write(f"Average Humidity: {avg_humidity:.1f}%\n\n")
            
            # Category distribution
            categories = {}
            for d in data_history:
                cat = d['aqi_category']
                categories[cat] = categories.get(cat, 0) + 1
            
            f.write("AIR QUALITY DISTRIBUTION:\n")
            f.write("-" * 40 + "\n")
            for cat, count in categories.items():
                percentage = (count / len(data_history)) * 100
                f.write(f"{cat}: {count} readings ({percentage:.1f}%)\n")
            
            if alert_history:
                f.write("\nALERT SUMMARY:\n")
                f.write("-" * 40 + "\n")
                alert_levels = {}
                for alert in alert_history:
                    level = alert['alert_level']
                    alert_levels[level] = alert_levels.get(level, 0) + 1
                for level, count in alert_levels.items():
                    f.write(f"{level}: {count} alerts\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("END OF REPORT\n")
    
    print(f"\n📄 Report saved to: {report_filename}")
    return report_filename

def print_banner():
    """Display welcome banner"""
    print("\n" + "=" * 60)
    print("   IoT-Based Air Quality & Pollution Monitoring System")
    print("   Environmental Data Analysis & Real-time Monitoring")
    print("=" * 60)
    print("\n📡 System initialized successfully!")
    print("🔄 Starting data collection...\n")

def main():
    """Main function to run the air quality monitoring system"""
    
    # Setup
    setup_directories()
    print_banner()
    
    # Initialize components
    simulator = AirQualitySensorSimulator()
    alert_gen = AlertGenerator()
    
    # Data storage
    data_history = []
    alert_history = []
    
    # Monitoring parameters
    duration = int(input("Enter monitoring duration in seconds (e.g., 30): ") or "30")
    interval = int(input("Enter reading interval in seconds (e.g., 5): ") or "5")
    
    print(f"\n📊 Starting {duration} seconds of monitoring...")
    print(f"⏱️ Reading every {interval} seconds\n")
    print("-" * 60)
    
    start_time = time.time()
    readings_count = 0
    
    try:
        while time.time() - start_time < duration:
            # Generate sensor reading
            sensor_data = simulator.get_all_readings()
            
            # Calculate AQI
            aqi_result = AQICalculator.calculate_aqi(sensor_data["air_quality"])
            
            # Check for alerts
            alert = alert_gen.check_and_alert(sensor_data, aqi_result)
            
            # Prepare log entry
            log_entry = {
                "timestamp": sensor_data["timestamp"],
                "air_quality": sensor_data["air_quality"],
                "temperature_c": sensor_data["temperature_c"],
                "humidity_percent": sensor_data["humidity_percent"],
                "smoke_ppm": sensor_data["smoke_ppm"],
                "co2_ppm": sensor_data["co2_ppm"],
                "aqi_category": aqi_result["category"],
                "alert_status": "ALERT" if alert else "NORMAL"
            }
            
            # Store data
            data_history.append(log_entry)
            if alert:
                alert_history.append(alert)
            
            # Log to CSV
            log_to_csv(log_entry)
            
            # Display current reading
            readings_count += 1
            print(f"[{readings_count}] {sensor_data['timestamp']} | "
                  f"AQI: {sensor_data['air_quality']} ({aqi_result['category']}) | "
                  f"Temp: {sensor_data['temperature_c']}°C | "
                  f"Humidity: {sensor_data['humidity_percent']}% | "
                  f"Smoke: {sensor_data['smoke_ppm']}ppm")
            
            # Wait for next reading
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Monitoring stopped by user")
    
    # Generate final report
    elapsed_time = time.time() - start_time
    print("\n" + "-" * 60)
    print("\n✅ Monitoring completed!")
    print(f"📊 Total readings collected: {readings_count}")
    print(f"🚨 Total alerts triggered: {len(alert_history)}")
    
    # Generate report
    report_file = generate_report(data_history, alert_history, int(elapsed_time))
    
    # Display alert summary
    print(alert_gen.get_alert_summary())
    
    print("\n✨ System shutdown complete!")
    print(f"📁 Check 'data/sensor_logs.csv' for all readings")
    print(f"📁 Check 'data/alerts_log.csv' for alert history")
    print(f"📁 Check 'outputs/reports/' for detailed reports")

if __name__ == "__main__":
    main()