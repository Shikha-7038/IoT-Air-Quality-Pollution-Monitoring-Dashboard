"""
alert_generator.py
Generates alerts when pollution exceeds safe limits
Supports console, file, and visual alerts
"""

from datetime import datetime
import os

class AlertGenerator:
    """
    Alert levels:
    - INFO: General information
    - WARNING: Moderate pollution
    - CRITICAL: Hazardous pollution
    - EMERGENCY: Severe health risk
    """
    
    def __init__(self):
        self.alert_history = []
        self.alert_file = "data/alerts_log.csv"
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Initialize alert log file
        if not os.path.exists(self.alert_file):
            with open(self.alert_file, 'w', encoding='utf-8') as f:
                f.write("timestamp,alert_level,air_quality_value,category,message\n")
    
    def check_and_alert(self, sensor_data, aqi_result):
        """
        Check sensor data and generate alerts if needed
        Returns: dict with alert info (or None if no alert)
        """
        air_quality = sensor_data["air_quality"]
        category = aqi_result["category"]
        
        alert_level = None
        alert_message = None
        
        # Determine alert level based on AQI category
        if category == "Poor":
            alert_level = "WARNING"
            alert_message = f"WARNING: Poor air quality detected (AQI: {air_quality}). {aqi_result['message']}"
            
        elif category == "Unhealthy":
            alert_level = "CRITICAL"
            alert_message = f"CRITICAL ALERT: Unhealthy air quality (AQI: {air_quality}). {aqi_result['message']}"
            
        elif category == "Hazardous":
            alert_level = "EMERGENCY"
            alert_message = f"EMERGENCY ALERT: Hazardous air quality (AQI: {air_quality})! {aqi_result['message']}"
        
        # Check individual pollutant thresholds
        if sensor_data["smoke_ppm"] > 150:
            alert_level = "CRITICAL"
            alert_message = f"SMOKE ALERT: High smoke levels detected ({sensor_data['smoke_ppm']} ppm)!"
            
        if sensor_data["co2_ppm"] > 1000:
            alert_level = "WARNING"
            alert_message = f"CO2 ALERT: Elevated CO2 levels ({sensor_data['co2_ppm']} ppm). Ensure proper ventilation!"
        
        if alert_level:
            alert_info = {
                "timestamp": sensor_data["timestamp"],
                "alert_level": alert_level,
                "air_quality_value": air_quality,
                "category": category,
                "message": alert_message,
                "smoke_ppm": sensor_data["smoke_ppm"],
                "co2_ppm": sensor_data["co2_ppm"],
                "temperature": sensor_data["temperature_c"],
                "humidity": sensor_data["humidity_percent"]
            }
            
            # Store in history
            self.alert_history.append(alert_info)
            
            # Log to CSV file
            self._log_alert_to_csv(alert_info)
            
            # Display alert
            self._display_alert(alert_info)
            
            return alert_info
        
        return None
    
    def _log_alert_to_csv(self, alert_info):
        """Write alert to CSV log file (without special characters)"""
        with open(self.alert_file, 'a', encoding='utf-8') as f:
            # Remove any special characters from message
            clean_message = alert_info['message'].replace('⚠️', '').replace('🔴', '').replace('🚨', '').replace('🔥', '').replace('💨', '').strip()
            f.write(f"{alert_info['timestamp']},{alert_info['alert_level']},"
                   f"{alert_info['air_quality_value']},{alert_info['category']},"
                   f"\"{clean_message}\"\n")
    
    def _display_alert(self, alert_info):
        """Display alert in console with formatting"""
        print("\n" + "=" * 70)
        print(f"{alert_info['alert_level']} ALERT!")
        print("=" * 70)
        print(f"Time: {alert_info['timestamp']}")
        print(f"Air Quality: {alert_info['air_quality_value']} ({alert_info['category']})")
        print(f"Smoke Level: {alert_info['smoke_ppm']} ppm")
        print(f"CO2 Level: {alert_info['co2_ppm']} ppm")
        print(f"Temperature: {alert_info['temperature']}°C")
        print(f"Humidity: {alert_info['humidity']}%")
        print(f"\n{alert_info['message']}")
        print("=" * 70 + "\n")
    
    def get_alert_summary(self):
        """Get summary of all alerts generated"""
        if not self.alert_history:
            return "No alerts generated during this session."
        
        summary = f"\nAlert Summary ({len(self.alert_history)} alerts):\n"
        summary += "-" * 50 + "\n"
        
        alert_counts = {}
        for alert in self.alert_history:
            level = alert['alert_level']
            alert_counts[level] = alert_counts.get(level, 0) + 1
        
        for level, count in alert_counts.items():
            summary += f"  {level}: {count} alert(s)\n"
        
        return summary
    
    def clear_alert_history(self):
        """Clear current session alert history (does not clear file)"""
        self.alert_history = []
    
    def generate_test_alerts(self):
        """Generate test alerts for demonstration"""
        print("\nGenerating test alerts for demonstration...\n")
        
        test_scenarios = [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "air_quality_value": 250,
                "category": "Unhealthy",
                "message": "Test unhealthy alert",
                "smoke_ppm": 120,
                "co2_ppm": 900,
                "temperature": 32.5,
                "humidity": 45.0
            },
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "air_quality_value": 400,
                "category": "Hazardous",
                "message": "Test hazardous alert",
                "smoke_ppm": 300,
                "co2_ppm": 1500,
                "temperature": 38.0,
                "humidity": 30.0
            }
        ]
        
        for scenario in test_scenarios:
            alert_info = {
                "timestamp": scenario["timestamp"],
                "alert_level": "TEST_" + scenario["category"].upper(),
                "air_quality_value": scenario["air_quality_value"],
                "category": scenario["category"],
                "message": scenario["message"],
                "smoke_ppm": scenario["smoke_ppm"],
                "co2_ppm": scenario["co2_ppm"],
                "temperature": scenario["temperature"],
                "humidity": scenario["humidity"]
            }
            self._display_alert(alert_info)


# Test the alert generator
if __name__ == "__main__":
    alert_gen = AlertGenerator()
    
    # Test with simulated data
    from simulation.sensor_simulator import AirQualitySensorSimulator
    from processing.aqi_calculator import AQICalculator
    
    simulator = AirQualitySensorSimulator()
    
    print("Testing Alert Generator")
    print("-" * 50)
    
    # Test different pollution levels
    scenarios = ["normal", "moderate", "poor", "hazardous"]
    
    for scenario in scenarios:
        sensor_data = simulator.get_specific_scenario(scenario)
        aqi_result = AQICalculator.calculate_aqi(sensor_data["air_quality"])
        
        print(f"\nTesting {scenario.upper()} scenario...")
        alert = alert_gen.check_and_alert(sensor_data, aqi_result)
        
        if not alert:
            print("  No alert - Air quality is safe")
    
    print(alert_gen.get_alert_summary())