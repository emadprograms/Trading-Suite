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

### Step 3b: Add Credentials
You must create a `secrets.toml` file in **each** of the folders above.

**Example Content (`.streamlit/secrets.toml`):**
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

## 4. Launch the Suite
Always launch from the root directory.

```bash
# Activate venv first (if not already active)
source venv/bin/activate

# Launch the Main Hub
streamlit run Home.py
```
