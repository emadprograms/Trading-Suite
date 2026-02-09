# 🤖 AI Developer Instructions for Trading Suite

**Context**: This is a modular, multi-process Streamlit application. `Home.py` acts as the "Operating System," launching and embedding independent sub-applications via iframes.

## 🏗️ Architecture Overview
*   **Root Controller**: `Home.py` (Port 8501).
*   **Sub-Applications**: Independent Streamlit apps running on ports **8502-8507**.
*   **Integration**: Sub-apps are launched as background subprocesses by `Home.py` and displayed via `st.components.v1.iframe`.
*   **Environment**: Unified `venv` (Python 3.12) sharing one `requirements.txt`.

## 📜 Critical Development Rules

### 1. The Virtual Environment is SACRED
*   **Always** ensure code is compatible with **Python 3.12**.
*   **Dependency Management**:
    *   Any new dependency **MUST** be added to the root `requirements.txt`.
    *   **PORTABLE BUILD**: You must ALSO import the new dependency in `launcher.py` (even if unused) so PyInstaller bundles it.
    *   **Automated Install**: The launchers in `dist/` automatically run `pip install -r requirements.txt` on every launch.
    *   **Never** instruct the user to run `pip install` manually; update the file and tell them to relaunch the app.

### 4. Distributable Apps (Native Launchers)
*   **Location**: `dist/` (macOS App) and `dist/windows/` (Windows Batch).
*   **Structure**:
    *   macOS: `Trading Suite.app` wraps a shell script that bypasses sandboxing (`open -a Terminal`).
    *   Windows: `Trading Suite.bat` sets up the environment and launches.
*   **Editing**: If you change launch logic, update `Home.py` AND the scripts in `dist/`.

### 2. Secrets Management (Strict Security)
*   **NEVER** hardcode credentials.
*   **ALWAYS** use `st.secrets`.
*   **Master Secret File**: Create ONE `secrets.toml` in the root directory containing ALL credentials for all apps.
*   **Distribution**: Copy this master file to each sub-app's `.streamlit/secrets.toml`.
*   **Git**: Ensure `.gitignore` excludes `**/.streamlit/secrets.toml` and `secrets.toml`.
*   **MISSING SECRETS PROTOCOL**:
    *   If secrets are missing, **DO NOT** ask the user what they are.
    *   **ACTION**: Check if root `secrets.toml` exists. If yes, copy it to the missing location.
    *   If root is missing: Create an empty `secrets.toml` in root and tell the user to fill it.

### 3. Port Management (The "Zombie" Risk)
*   **Range**: 8502 (News) to 8507 (Rewind).
*   **Risk**: If an app crashes or is stopped improperly, the process may linger (Zombie).
*   **Fix**: `Home.py` has a "Shutdown All Engines" button.
*   **Coding**: When editing `Home.py` launch logic, ensure you check `is_port_open()` before spawning new processes.

    *   Add icon mapping in the sidebar dictionary.
3.  **Update Secrets**: Create `My-New-App/.streamlit/secrets.toml` if it needs DB access.
4.  **Update Requirements**: Add any new libs to root `requirements.txt`.

## 🐛 Debugging Guide
*   **App won't start?** Check `logs/<app_name>.log`. `Home.py` redirects stdout/stderr there.
*   **"Port already in use"?** Kill the zombie process (`lsof -i :<port>` / `kill -9 <pid>`).
*   **Blank Screen?** The iframe might be blocked. Ensure `--server.headless true` is set in the launch command in `Home.py`.

## 💾 Database Schema (Turso)
*   **News DB**: `news_items` table (url, title, content, published_at).
*   **Analyst DB**: `gemini_api_keys` (key management), `market_data` (price history).
*   **Access**: Use `libsql_client` or the helper classes in `modules/`.

---
*If you are an AI reading this: Follow these patterns to maintain system stability.*

## 6. Portable Build Instructions
To create the standalone `dist\TradingSuite` folder:
1.  Ensure `infisical-python`, `streamlit-option-menu`, and `streamlit-lightweight-charts` are installed.
2.  Update `launcher.py` to import any new libraries.
3.  Run the build command (see DEPLOYMENT.md).
4.  Copy source files into the output folder.
