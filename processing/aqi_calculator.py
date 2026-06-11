"""
aqi_calculator.py
Calculates Air Quality Index (AQI) and classifies pollution levels
Based on standard AQI formulas (EPA standards)
"""

class AQICalculator:
    
    
    # AQI Breakpoints (based on PM2.5 standard, adapted for our simulation)
    AQI_BREAKPOINTS = {
        "Good": {"min": 0, "max": 50, "color": "GREEN", "message": "Air quality is satisfactory"},
        "Moderate": {"min": 51, "max": 100, "color": "YELLOW", "message": "Acceptable air quality"},
        "Poor": {"min": 101, "max": 200, "color": "ORANGE", "message": "Sensitive groups may experience effects"},
        "Unhealthy": {"min": 201, "max": 300, "color": "RED", "message": "Everyone may begin to experience health effects"},
        "Hazardous": {"min": 301, "max": 500, "color": "PURPLE", "message": "Health alert: serious risk of health effects"}
    }
    
    @classmethod
    def calculate_aqi(cls, air_quality_value):
        """
        Calculate AQI category from raw air quality value
        Args: air_quality_value (int): 0-500 reading from sensor
        Returns: dict with category, color, message
        """
        for category, thresholds in cls.AQI_BREAKPOINTS.items():
            if thresholds["min"] <= air_quality_value <= thresholds["max"]:
                return {
                    "value": air_quality_value,
                    "category": category,
                    "color": thresholds["color"],
                    "message": thresholds["message"]
                }
        # Default fallback
        return {
            "value": air_quality_value,
            "category": "Unknown",
            "color": "⚪",
            "message": "Unable to determine air quality"
        }
    
    @classmethod
    def get_aqi_level_code(cls, air_quality_value):
        """Returns numeric code: 1=Good, 2=Moderate, 3=Poor, 4=Unhealthy, 5=Hazardous"""
        if air_quality_value <= 50:
            return 1
        elif air_quality_value <= 100:
            return 2
        elif air_quality_value <= 200:
            return 3
        elif air_quality_value <= 300:
            return 4
        else:
            return 5
    
    @classmethod
    def is_safe(cls, air_quality_value):
        """Returns True if air quality is Good or Moderate"""
        return air_quality_value <= 100
    
    @classmethod
    def get_health_recommendation(cls, air_quality_value):
        """Provides health recommendations based on AQI"""
        if air_quality_value <= 50:
            return "Ideal conditions. Enjoy outdoor activities!"
        elif air_quality_value <= 100:
            return "Fine for most people. Sensitive individuals should limit prolonged outdoor exertion."
        elif air_quality_value <= 200:
            return "Reduce outdoor activities. Keep windows closed. Use air purifier if available."
        elif air_quality_value <= 300:
            return "Avoid outdoor activities. Wear N95 mask if going out. Use air purifier."
        else:
            return "STAY INDOORS! Emergency conditions. Use N95 mask. Seek medical help if breathing issues."
    
    @classmethod
    def calculate_from_multiple_factors(cls, air_quality, smoke_ppm, co2_ppm):
        """
        Advanced AQI calculation considering multiple pollutants
        Returns the highest risk category
        """
        # Individual risk levels
        aqi_risk = cls.get_aqi_level_code(air_quality)
        
        # Smoke risk (ppm: 0-50 safe, 50-100 moderate, 100-200 poor, 200-500 hazardous)
        if smoke_ppm <= 50:
            smoke_risk = 1
        elif smoke_ppm <= 100:
            smoke_risk = 2
        elif smoke_ppm <= 200:
            smoke_risk = 3
        else:
            smoke_risk = 5
            
        # CO2 risk (ppm: 350-500 safe, 500-800 moderate, 800-1200 poor, 1200+ hazardous)
        if co2_ppm <= 500:
            co2_risk = 1
        elif co2_ppm <= 800:
            co2_risk = 2
        elif co2_ppm <= 1200:
            co2_risk = 3
        else:
            co2_risk = 5
            
        # Take the highest risk level
        overall_risk = max(aqi_risk, smoke_risk, co2_risk)
        
        # Convert back to category
        risk_to_category = {
            1: "Good",
            2: "Moderate", 
            3: "Poor",
            4: "Unhealthy",
            5: "Hazardous"
        }
        
        risk_to_color = {
            1: "🟢",
            2: "🟡",
            3: "🟠",
            4: "🔴",
            5: "🟣"
        }
        
        return {
            "value": air_quality,
            "category": risk_to_category[overall_risk],
            "color": risk_to_color[overall_risk],
            "smoke_ppm": smoke_ppm,
            "co2_ppm": co2_ppm,
            "overall_risk_level": overall_risk
        }


# Test the calculator
if __name__ == "__main__":
    print("AQI Calculator Test")
    print("-" * 50)
    
    test_values = [25, 75, 150, 250, 400]
    for value in test_values:
        result = AQICalculator.calculate_aqi(value)
        print(f"AQI {value}: {result['color']} {result['category']} - {result['message']}")
        print(f"  Safe? {AQICalculator.is_safe(value)}")
        print(f"  Recommendation: {AQICalculator.get_health_recommendation(value)}")
        print()