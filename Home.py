import streamlit as st
import subprocess
import os
import sys
import time
import requests
import streamlit.components.v1 as components
try:
    from streamlit_option_menu import option_menu
except ImportError:
    st.error("Please install requirements: pip install streamlit-option-menu")
    st.stop()

# --- Configuration ---
st.set_page_config(
    page_title="Trading Suite",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Overrides for Seamless Integration ---
# --- CSS Overrides ---
# Standard layout with padding adjustments for a cleaner look.
st.markdown("""
    <style>
        /* Remove whitespace mainly on sides and bottom */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        /* Hide the Streamlit footer */
        footer {visibility: hidden;}
        
        /* Ensure iframe takes maximum height */
        iframe {
            height: 95vh !important;
        }
    </style>
""", unsafe_allow_html=True)
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
            cmd = [
                sys.executable, "-m", "streamlit", "run", config["file"],
                "--server.port", str(config["port"]),
                "--server.headless", "true",
                "--server.address", "localhost",
                "--theme.base", "dark"
            ]
            working_dir = os.path.join(os.getcwd(), config["dir"])
            
            # Create logs directory if it doesn't exist
            log_dir = os.path.join(os.getcwd(), "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"{name.replace(' ', '_').lower()}.log")
            
            with open(log_file, "w") as f:
                subprocess.Popen(
                    cmd,
                    cwd=working_dir,
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    start_new_session=True
                )

# --- Initialization ---
# Run launch logic only once per session/reload to save resources
if 'apps_launched' not in st.session_state:
    with st.spinner("Initializing Trading Suite & Launching Sub-Engines..."):
        launch_all_apps()
        time.sleep(3) 
    st.session_state.apps_launched = True
    st.rerun() 

# --- Sidebar Navigation ---
with st.sidebar:
    # Use logo or title
    # st.image("https://img.icons8.com/3d-fluency/94/rocket.png", width=60)
    st.title("💸 Trading Suite")
    st.caption("Unified Command Center")
    
    # Map apps to Bootstrap icons
    # Icons: https://icons.getbootstrap.com/
    icons = {
        "News Fetcher": "newspaper",
        "Analyst Workbench": "graph-up-arrow",
        "Data Harvester": "database-fill",
        "Key Manager": "key-fill",
        "Pre-Market Scanner": "activity",
        "Market Rewind": "clock-history"
    }
    
    app_list = list(APPS.keys())
    
    # Modern Option Menu
    selected_app = option_menu(
        "Navigation",
        app_list,
        icons=[icons.get(app, "app") for app in app_list],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#FF4B4B", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#333333"},
            "nav-link-selected": {"background-color": "#262730", "border-left": "5px solid #FF4B4B"},
        }
    )

st.sidebar.divider()
st.sidebar.info(f"**Status:** {selected_app} is Active")

# --- Main Content Area ---
config = APPS[selected_app]
url = f"http://localhost:{config['port']}"

# Check if it's actually ready
if is_port_open(config['port']):
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
