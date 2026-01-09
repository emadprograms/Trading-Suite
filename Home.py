import streamlit as st
import subprocess
import os
import sys
import time
import requests
import streamlit.components.v1 as components

# --- Configuration ---
st.set_page_config(
    page_title="Trading Suite",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Definitions
APPS = {
    "News Fetcher": {
        "dir": "News-Fetcher",
        "file": "app.py",
        "port": 8502,
        "icon": "📰",
    },
    "Analyst Workbench": {
        "dir": "analyst-workbench",
        "file": "app.py",
        "port": 8503,
        "icon": "🔬",
    },
    "Data Harvester": {
        "dir": "data-harvester",
        "file": "app.py",
        "port": 8504,
        "icon": "🌾",
    },
    "Key Manager": {
        "dir": "gemini-api-key-manager",
        "file": "app.py",
        "port": 8505,
        "icon": "🔑",
    },
    "Pre-Market Scanner": {
        "dir": "premarket-scanner",
        "file": "app.py",
        "port": 8506,
        "icon": "📈",
    },
    "Market Rewind": {
        "dir": "market-rewind",
        "file": "streamlit_app.py",
        "port": 8507,
        "icon": "⏪",
    }
}

# --- Utils ---
def is_port_open(port):
    """Checks if a local port is open (meaning app is running)."""
    try:
        response = requests.get(f"http://localhost:{port}/_stcore/health", timeout=0.5)
        return response.status_code == 200
    except:
        return False

def launch_all_apps():
    """Iterates through apps and launches them if not running."""
    for name, config in APPS.items():
        if not is_port_open(config['port']):
            # st.toast(f"Starting {name}...", icon="⏳")
            cmd = [
                sys.executable, "-m", "streamlit", "run", config["file"],
                "--server.port", str(config["port"]),
                "--server.headless", "true",
                "--server.address", "localhost",
                "--theme.base", "dark"
            ]
            working_dir = os.path.join(os.getcwd(), config["dir"])
            
            subprocess.Popen(
                cmd,
                cwd=working_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )

# --- Initialization ---
# Run launch logic only once per session/reload to save resources
if 'apps_launched' not in st.session_state:
    with st.spinner("Initializing Trading Suite & Launching Sub-Engines..."):
        launch_all_apps()
        # Give them a few seconds to warm up
        time.sleep(3) 
    st.session_state.apps_launched = True
    st.rerun() # Refresh to clear spinner

# --- Sidebar Navigation ---
st.sidebar.title("� Trading Suite")
st.sidebar.caption("Unified Command Center")

selected_app = st.sidebar.radio(
    "Select Application",
    list(APPS.keys()),
    index=0,
    format_func=lambda x: f"{APPS[x]['icon']} {x}"
)

st.sidebar.divider()
st.sidebar.info(f"**Status:** {selected_app} is Active")

# --- Main Content Area ---
config = APPS[selected_app]
url = f"http://localhost:{config['port']}"

# Check if it's actually ready
if is_port_open(config['port']):
    # Embed the app using an iframe
    # We use a height calculation or fixed height. 
    # 'scrolling=True' is important for nested streamlit apps.
    components.iframe(url, height=1000, scrolling=True)
else:
    st.warning(f"⚠️ {selected_app} is currently starting up...")
    st.info("Please wait a moment and click 'Refresh' below.")
    if st.button("Refresh View"):
        st.rerun()

# --- Global Controls (Bottom of sidebar) ---
st.sidebar.divider()
if st.sidebar.button("🛑 Shutdown All Engines"):
    import psutil
    count = 0
    for name, conf in APPS.items():
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == conf['port']:
                        proc.terminate()
                        count += 1
            except:
                pass
    st.sidebar.success(f"Stopped {count} engines. Please close the tab.")
