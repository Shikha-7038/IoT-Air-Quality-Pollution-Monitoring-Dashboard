"""
sensor_simulator.py
Generates realistic fake sensor data for air quality monitoring
No hardware required - simulates MQ135, DHT11 sensors
"""

import random
import time
from datetime import datetime
import numpy as np

class AirQualitySensorSimulator:
    """
    Simulates:
    - MQ135 sensor: Measures air quality (0-1023) - higher = more pollution
    - DHT22 sensor: Temperature (15-45°C) and Humidity (20-90%)
    - Smoke/Gas level: 0-500 ppm
    """
    
    def __init__(self):
        self.base_air_quality = 100  # Normal baseline
        self.base_temperature = 25.0
        self.base_humidity = 55.0
        self.pollution_trend = 0  # 0 = normal, 1 = increasing, -1 = decreasing
        
    def generate_air_quality(self):
        """
        Simulates MQ135 sensor
        Returns: value between 0-500 (0=clean air, 500=highly polluted)
        """
        # Random walk simulation for realistic variations
        change = random.uniform(-15, 15)
        
        # Occasionally simulate pollution spikes
        if random.random() < 0.05:  # 5% chance of pollution spike
            change += random.uniform(50, 150)
            
        self.base_air_quality += change
        # Keep within realistic bounds
        self.base_air_quality = max(20, min(500, self.base_air_quality))
        
        return int(self.base_air_quality)
    
    def generate_temperature(self):
        """
        Simulates DHT22 temperature sensor
        Returns: temperature in Celsius (15°C to 45°C)
        """
        # Gradual temperature changes with small random variations
        change = random.uniform(-0.5, 0.5)
        self.base_temperature += change
        
        # Day/Night cycle simulation (simplified)
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 18:  # Daytime
            self.base_temperature += 0.1
        else:  # Nighttime
            self.base_temperature -= 0.1
            
        # Keep within realistic bounds
        self.base_temperature = max(15, min(45, self.base_temperature))
        
        return round(self.base_temperature, 1)
    
    def generate_humidity(self):
        """
        Simulates DHT22 humidity sensor
        Returns: relative humidity percentage (20-90%)
        """
        # Humidity inversely related to temperature
        temp = self.base_temperature
        ideal_humidity = 60 - (temp - 25) * 0.5  # Higher temp = lower humidity
        
        # Add random variation
        variation = random.uniform(-5, 5)
        humidity = ideal_humidity + variation
        
        # Keep within realistic bounds
        humidity = max(20, min(90, humidity))
        self.base_humidity = humidity
        
        return round(humidity, 1)
    
    def generate_smoke_level(self):
        """
        Simulates smoke/gas detection
        Returns: smoke level in ppm (0-500)
        """
        # Smoke often correlates with air quality
        smoke = self.base_air_quality * 0.8
        
        # Add random spikes for gas leakage simulation
        if random.random() < 0.03:  # 3% chance of gas leak
            smoke += random.uniform(100, 300)
            
        smoke = min(500, smoke)
        return int(smoke)
    
    def generate_co2_level(self):
        """
        Simulates CO2 levels in ppm
        Returns: 350-2000 ppm (350=normal outdoor, 1000+=poor)
        """
        co2 = 400 + (self.base_air_quality * 1.5)
        co2 = min(2000, co2)
        return int(co2)
    
    def get_all_readings(self):
        """
        Returns complete sensor reading as dictionary
        """
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "air_quality": self.generate_air_quality(),  # 0-500 scale
            "temperature_c": self.generate_temperature(),
            "humidity_percent": self.generate_humidity(),
            "smoke_ppm": self.generate_smoke_level(),
            "co2_ppm": self.generate_co2_level()
        }
    
    def get_specific_scenario(self, scenario="normal"):
        """
        Generate readings for specific test scenarios
        scenarios: "normal", "moderate", "poor", "hazardous"
        """
        if scenario == "normal":
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "air_quality": random.randint(20, 80),
                "temperature_c": round(random.uniform(20, 28), 1),
                "humidity_percent": round(random.uniform(45, 65), 1),
                "smoke_ppm": random.randint(10, 50),
                "co2_ppm": random.randint(350, 500)
            }
        elif scenario == "moderate":
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "air_quality": random.randint(81, 180),
                "temperature_c": round(random.uniform(28, 32), 1),
                "humidity_percent": round(random.uniform(40, 55), 1),
                "smoke_ppm": random.randint(51, 100),
                "co2_ppm": random.randint(501, 800)
            }
        elif scenario == "poor":
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "air_quality": random.randint(181, 300),
                "temperature_c": round(random.uniform(32, 38), 1),
                "humidity_percent": round(random.uniform(35, 50), 1),
                "smoke_ppm": random.randint(101, 200),
                "co2_ppm": random.randint(801, 1200)
            }
        elif scenario == "hazardous":
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "air_quality": random.randint(301, 500),
                "temperature_c": round(random.uniform(35, 45), 1),
                "humidity_percent": round(random.uniform(20, 40), 1),
                "smoke_ppm": random.randint(201, 500),
                "co2_ppm": random.randint(1201, 2000)
            }


# For testing the simulator independently
if __name__ == "__main__":
    simulator = AirQualitySensorSimulator()
    print("Testing Air Quality Sensor Simulator")
    print("-" * 40)
    
    # Test normal readings
    print("\n1. Normal Readings:")
    for i in range(5):
        reading = simulator.get_all_readings()
        print(f"  {reading['timestamp']} - AQ:{reading['air_quality']}, "
              f"Temp:{reading['temperature_c']}°C, Humidity:{reading['humidity_percent']}%")
        time.sleep(1)
    
    # Test scenarios
    print("\n2. Testing Different Scenarios:")
    for scenario in ["normal", "moderate", "poor", "hazardous"]:
        reading = simulator.get_specific_scenario(scenario)
        print(f"  {scenario.upper()}: AQ={reading['air_quality']}, "
              f"Smoke={reading['smoke_ppm']}ppm, CO2={reading['co2_ppm']}ppm")