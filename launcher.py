import os
import sys
import webbrowser
import threading
import time

# --- BUNDLING IMPORTS ---
# We import these so PyInstaller finds them and bundles them.
# We don't use them directly in this script, but they need to be in the package.
try:
    import streamlit
    import streamlit.web.cli as stcli
    import pandas
    import numpy
    import altair
    import requests
    import psutil
    import watchdog
    import yfinance
    import plotly
    import bs4
    import PIL
    import cv2 
    import streamlit_option_menu
    import streamlit_lightweight_charts
    import infisical_client
    # Add other heavy imports here if needed
except ImportError:
    pass
# ------------------------

def run_streamlit(app_path):
    """Runs Streamlit using the internal CLI."""
    # Fake argv so Streamlit thinks it was called from command line
    sys.argv = [
        "streamlit", 
        "run", 
        app_path, 
        "--server.port", "8510", 
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--global.developmentMode", "false"
    ]
    sys.exit(stcli.main())

def open_browser():
    """Opens browser after a short delay."""
    time.sleep(3)
    print("🌍 Opening Browser...")
    webbrowser.open("http://localhost:8510")

def main():
    print("� Starting Trading Suite (Portable)...")
    
    # Determine base path (where the exe/script is located)
    if getattr(sys, 'frozen', False):
        # If frozen, sys.executable is the exe.
        # We assume the source code is in the SAME FOLDER as the internal Python env or strict relative path.
        # For --onedir, sys._MEIPASS is the temp folder, but we want the app folder.
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(application_path)
    print(f"📂 Working Directory: {os.getcwd()}")
    
    home_script = os.path.join(application_path, "Home.py")
    if not os.path.exists(home_script):
        print(f"❌ Error: Home.py not found at {home_script}")
        print("Please ensure 'Home.py' and the project folders are next to the executable.")
        input("Press Enter to exit...")
        return
        
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("🌟 Launching Application...")
    run_streamlit(home_script)

if __name__ == "__main__":
    main()
