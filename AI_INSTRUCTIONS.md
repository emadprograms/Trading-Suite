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
*   Any new dependency **MUST** be added to the root `requirements.txt`.
*   **Never** instruct the user to run `pip install` manually; update the file.

### 2. Secrets Management (Strict Security)
*   **NEVER** hardcode credentials.
*   **ALWAYS** use `st.secrets`.
*   **Location**: Each sub-app has its own `.streamlit/secrets.toml` (e.g., `News-Fetcher/.streamlit/secrets.toml`).
*   **Git**: Ensure `.gitignore` excludes `**/.streamlit/secrets.toml`.
*   **MISSING SECRETS PROTOCOL**:
    *   If secrets are missing, **DO NOT** ask the user what they are.
    *   **ACTION**: Run `mkdir -p <app>/.streamlit` and `touch <app>/.streamlit/secrets.toml` to create an empty file.
    *   **NOTIFY**: Tell the user: *"I have created the secrets file. Please open it and paste your API keys manually."*

### 3. Port Management (The "Zombie" Risk)
*   **Range**: 8502 (News) to 8507 (Rewind).
*   **Risk**: If an app crashes or is stopped improperly, the process may linger (Zombie).
*   **Fix**: `Home.py` has a "Shutdown All Engines" button.
*   **Coding**: When editing `Home.py` launch logic, ensure you check `is_port_open()` before spawning new processes.

### 4. Git Submodules
*   This repo uses submodules.
*   **Reading Code**: You can read sub-app code directly (e.g., `News-Fetcher/app.py`).
*   **Modifying Code**: You can edit files directly.
*   **Syncing**: Remind the user to run `git submodule update --remote` if they are pulling updates.

## 🚀 How to Extend the Suite (Adding a New App)
1.  **Drop code**: Place the new app folder in the root (e.g., `My-New-App/`).
2.  **Update `Home.py`**:
    *   Add entry to `APPS` dictionary:
        ```python
        "My New App": {
            "dir": "My-New-App",
            "file": "app.py",
            "port": 8508, # Next available port
            "icon": "🚀"
        }
        ```
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
