"""
run_simulation.py
Quick start script for the air quality monitoring system
Runs a default 30-second simulation
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit, pandas, numpy, plotly
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required packages"""
    print("📦 Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "streamlit", "pandas", "numpy", "plotly"])
    print("✅ Dependencies installed successfully!")

def main():
    print("\n" + "=" * 60)
    print("   IoT Air Quality Monitoring System")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("⚠️ Required packages not found!")
        install = input("Do you want to install them now? (y/n): ").lower()
        if install == 'y':
            install_dependencies()
        else:
            print("❌ Cannot run without dependencies. Exiting...")
            sys.exit(1)
    
    print("\nSelect mode:")
    print("1. 📊 Streamlit Dashboard (Web Interface)")
    print("2. 💻 Console Mode (Command Line)")
    print("3. 🧪 Run Test Suite")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Streamlit Dashboard...")
        print("🌐 Dashboard will open in your browser")
        subprocess.run([sys.executable, "-m", "streamlit", "run", 
                       "dashboard/streamlit_app.py"])
    
    elif choice == "2":
        print("\n🚀 Starting Console Mode...")
        subprocess.run([sys.executable, "app.py"])
    
    elif choice == "3":
        print("\n🧪 Running Test Suite...")
        subprocess.run([sys.executable, "tests/run_tests.py"])
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()