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

## 5. Launch the Suite (Manual Method)
Always launch from the root directory.

```bash
# Activate venv first (if not already active)
source venv/bin/activate

# Launch the Main Hub
streamlit run Home.py
```
