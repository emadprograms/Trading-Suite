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
        /* Remove whitespace ONLY in the main content area (where the iframe is) */
        section[data-testid="stMain"] .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }

        /* Restore padding for the sidebar so the close button is visible */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 2rem !important;
        }
        
        /* Hide the Streamlit footer */
        footer {visibility: hidden;}
        
        /* HEADER MANAGEMENT (Borderless but functional) */
        /* 1. Make the header container transparent and non-blocking */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* 2. Hide specific header elements we don't want */
        .stDeployButton {display: none !important;} /* Hide Deploy button */
        [data-testid="stMainMenu"] {visibility: hidden !important;} /* Hide Hamburger menu */
        [data-testid="stDecoration"] {visibility: hidden !important;} /* Hide colored line */
        
        /* 3. Ensure Sidebar Collapse Button is visible */
        [data-testid="stSidebarCollapseButton"] {
            visibility: visible !important;
            color: #FF4B4B !important; /* Optional: Make it pop */
        }
        
        /* Ensure iframe takes maximum height and pulls up to hide nested header */
        iframe {
            /* Full viewport height + offset to compensate for the top shift */
            height: calc(100vh + 55px) !important;
            top: -55px !important; /* Push up to hide sub-app header */
            position: relative !important;
            border: none !important;
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)


APPS = {
    "News Fetcher": {
        "dir": "News-Fetcher",
        "file": "app.py",
        "port": 8511,
        "icon": "📰",
    },
    "News Network": {
        "dir": "news-network",
        "file": "app.py",
        "port": 8517,
        "icon": "📡",
    },
    "Data Harvester": {
        "dir": "data-harvester",
        "file": "app.py",
        "port": 8513,
        "icon": "🌾",
    },
    "Analyst Workbench": {
        "dir": "analyst-workbench",
        "file": "app.py",
        "port": 8512,
        "icon": "🔬",
    },
    "Pre-Market Scanner": {
        "dir": "premarket-scanner",
        "file": "app.py",
        "port": 8515,
        "icon": "📈",
    },
    "Key Manager": {
        "dir": "gemini-api-key-manager",
        "file": "app.py",
        "port": 8514,
        "icon": "🔑",
    },
    "Market Rewind": {
        "dir": "market-rewind",
        "file": "streamlit_app.py",
        "port": 8516,
        "icon": "⏪",
    }
}

# --- Utils ---
def is_port_open(port):
    """Checks if a local port is open (meaning app is running)."""
    try:
        url = f"http://localhost:{port}/_stcore/health"
        response = requests.get(url, timeout=0.5)
        # st.toast(f"Port {port} check: {response.status_code}") # excessive noise
        return response.status_code == 200
    except Exception as e:
        # st.toast(f"Port {port} closed: {e}")
        return False

def get_local_ip():
    """Detects the network IP of the server."""
    import socket
    try:
        # This doesn't actually connect, just finds the interface used to reach the internet
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def launch_all_apps():
    """Iterates through apps and launches them if not running."""
    st.write("Debug: Starting Launch Sequence...")
    for name, config in APPS.items():
        is_open = is_port_open(config['port'])
        st.write(f"Debug: App {name} on {config['port']} - Open? {is_open}")
        
        if not is_open:
            st.write(f"Debug: Launching {name}...")
            cmd = [
                sys.executable, "-m", "streamlit", "run", config["file"],
                "--server.port", str(config["port"]),
                "--server.headless", "true",
                "--server.address", "0.0.0.0",
                "--server.fileWatcherType", "watchdog",
                "--theme.base", "dark"
            ]
            working_dir = os.path.join(os.getcwd(), config["dir"])
            
            # Create logs directory if it doesn't exist
            log_dir = os.path.join(os.getcwd(), "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"{name.replace(' ', '_').lower()}.log")
            
            try:
                with open(log_file, "w") as f:
                    subprocess.Popen(
                        cmd,
                        cwd=working_dir,
                        stdout=f,
                        stderr=subprocess.STDOUT,
                        start_new_session=True
                    )
                st.write(f"Debug: Launch command sent for {name}")
            except Exception as e:
                st.error(f"Failed to launch {name}: {e}")

# --- Initialization ---
if 'apps_launched' not in st.session_state:
    with st.expander("System Bootstrap Logs", expanded=True):
        launch_all_apps()
        time.sleep(5) # Increased wait time
    st.session_state.apps_launched = True
    st.rerun() 

# --- Sidebar Navigation ---
with st.sidebar:
    # 🛑 FORCE SPACER: Matches the main header offset to reveal the close button
    st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
    
    # Use logo or title
    # st.image("https://img.icons8.com/3d-fluency/94/rocket.png", width=60)
    # Map apps to Bootstrap icons
    # Icons: https://icons.getbootstrap.com/
    icons = {
        "News Fetcher": "newspaper",
        "News Network": "broadcast",
        "Analyst Workbench": "graph-up-arrow",
        "Data Harvester": "database-fill",
        "Key Manager": "key-fill",
        "Pre-Market Scanner": "activity",
        "Market Rewind": "clock-history"
    }
    
    app_list = list(APPS.keys())



    # Modern Option Menu
    selected_app = option_menu(
        "Trading Suite",
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
server_ip = get_local_ip()
url = f"http://{server_ip}:{config['port']}"

# Check if it's actually ready
if is_port_open(config['port']):
    components.iframe(url, height=800, scrolling=True)
else:
    st.warning(f"⚠️ {selected_app} is currently starting up...")
    st.info("Please wait a moment and click 'Refresh' below.")
    if st.button("Refresh View"):
        st.rerun()

# --- Global Controls (Bottom of sidebar) ---
# Show Network Access Info at the bottom
server_ip = get_local_ip()
st.sidebar.markdown(f"""
<div style='background-color: #262730; padding: 10px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #4B4B4B;'>
    <div style='font-size: 12px; color: #aaa;'>📡 Network Access</div>
    <div style='font-size: 14px; font-weight: bold; color: #fff;'>http://{server_ip}:8510</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()


if st.sidebar.button("☢️ KILL & RESTART SYSTEM", type="primary"):
    import psutil
    count = 0
    # Kill all sub-apps
    for name, conf in APPS.items():
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == conf['port']:
                        proc.kill()  # Force kill
                        count += 1
            except:
                pass
    
    # Clear session state to trigger re-launch
    if 'apps_launched' in st.session_state:
        del st.session_state['apps_launched']
    
    st.sidebar.warning(f"Killed {count} processes. Rebooting...")
    time.sleep(1)
    st.rerun()
