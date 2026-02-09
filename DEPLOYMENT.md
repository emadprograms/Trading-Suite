# 🚀 Trading Suite Deployment Guide

> [!WARNING]
> This repository does **NOT** work "out of the box" after cloning. You must manually configure **Secrets** and the **Python Environment** for security reasons.

## 1. Clone the Repository
Because this project uses **Git Submodules**, you must clone it recursively.

```bash
# Option A: Fresh Clone (Recommended)
git clone --recursive https://github.com/emadprograms/Trading-Suite.git

# Option B: If you already cloned normally
git submodule update --init --recursive
```

## 2. Set Up Python Environment (Python 3.12)
We use a unified virtual environment for all apps.

```bash
# 1. Create Virtual Environment (Python 3.12)
python3.12 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install Consolidated Dependencies
pip install -r requirements.txt
```

## 3. Configure Secrets (CRITICAL)
Credentials are **ignored** by Git for security. You must manually recreate the `secrets.toml` files on the new machine.

### Step 3a: Create the files
Run this command to create the necessary directories:
```bash
mkdir -p News-Fetcher/.streamlit analyst-workbench/.streamlit premarket-scanner/.streamlit
```

### Step 3b: Add Credentials (The "Master File" Method)

1.  **Create Master File**: Create a single `secrets.toml` file in the **root** directory of the project.
2.  **Populate It**: Add ALL credentials for ALL services (Turso, MarketAux, Gemini, etc.) into this one file.
3.  **Distribute It**: Run this command to copy it to all sub-applications automatically:

```bash
# Copy root secrets.toml to all sub-apps
for dir in News-Fetcher analyst-workbench data-harvester gemini-api-key-manager market-rewind news-network premarket-scanner; do
    mkdir -p "$dir/.streamlit"
    cp secrets.toml "$dir/.streamlit/secrets.toml"
    echo "✅ Copied secrets to $dir"
done
```

**Example Content (`secrets.toml`):**
```toml
[turso]
db_url = "libsql://your-database-url.turso.io"
auth_token = "your-auth-token"

[turso_news]
db_url = "libsql://news-database.turso.io"
auth_token = "news-token"

[marketaux]
api_keys = ["your-api-key"]
```

## 4. Launch the Suite (Easy Method)

We provide native-like launchers in the `dist/` folder.

*   **macOS**: Open `dist/` and double-click **Trading Suite.app**.
*   **Windows**: Open `dist/windows/` and double-click **Trading Suite.bat**.

> [!NOTE]
> **First Launch**: The app will automatically check for and install any missing dependencies (like `infisical-python`). This may take a minute or two on the first run.

## 5. Building the Portable Application (Windows)
This project includes a `launcher.py` that can be compiled into a standalone executable bundled with Python.

### Prerequisites
- Python 3.12+ installed.
- Virtual environment active and requirements installed.
- `pip install pyinstaller`

### Build Command
Run this from the project root:
```powershell
# 1. Clean previous builds
Remove-Item -Path "dist", "dist_portable", "build" -Recurse -Force -ErrorAction SilentlyContinue

# 2. Build with PyInstaller (Bundles Python + Deps)
.\venv\Scripts\pyinstaller --onedir --name "TradingSuite" --clean --noconfirm --distpath dist_portable `
    --collect-all streamlit `
    --collect-all altair `
    --collect-all pandas `
    --collect-all streamlit_option_menu `
    --collect-all infisical_client `
    --collect-all streamlit_lightweight_charts `
    launcher.py

# 3. Copy Source Files to Distribution
Copy-Item -Path Home.py -Destination dist_portable\TradingSuite\ -Force
Copy-Item -Path "News-Fetcher" -Destination dist_portable\TradingSuite -Recurse -Force
Copy-Item -Path "analyst-workbench" -Destination dist_portable\TradingSuite -Recurse -Force
Copy-Item -Path "data-harvester" -Destination dist_portable\TradingSuite -Recurse -Force
Copy-Item -Path "gemini-api-key-manager" -Destination dist_portable\TradingSuite -Recurse -Force
Copy-Item -Path "market-rewind" -Destination dist_portable\TradingSuite -Recurse -Force
Copy-Item -Path "news-network" -Destination dist_portable\TradingSuite -Recurse -Force
Copy-Item -Path "premarket-scanner" -Destination dist_portable\TradingSuite -Recurse -Force
Copy-Item -Path secrets.toml -Destination dist_portable\TradingSuite\ -Force
Copy-Item -Path ".streamlit" -Destination dist_portable\TradingSuite -Recurse -Force
```

### Final Output
The portable app will be in `dist_portable\TradingSuite`. You can zip this folder and share it.
- **Run**: Double-click `TradingSuite.exe`.
- **Config**: Edit `secrets.toml` inside the folder.

## 6. Launch the Suite (Manual Method)
Always launch from the root directory.

```bash
# Activate venv first (if not already active)
source venv/bin/activate
# Install dependencies manually if using this method
pip install -r requirements.txt

# Launch the Main Hub
streamlit run Home.py
```
