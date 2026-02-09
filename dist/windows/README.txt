# Windows Deployment Guide

## 1. Using the Batch File (Recommended)
The `Trading Suite.bat` file in this folder acts exactly like an executable.
1.  Move the entire folder (or just double-click here) to verify it works.
2.  It will automatically setup the Python environment and launch the app.

## 2. Converting to .EXE
If you strictly require a `.exe` file (e.g., for policy reasons):

1.  Open this folder in a Command Prompt.
2.  Ensure you have a tool like `iexpress` (built-in to Windows) or install `bat-to-exe-converter`.
3.  Convert `Trading Suite.bat` into an `.exe`. 

**Note**: Since this project relies on many Python dependencies and sub-processes, a simple PyInstaller build is often unstable. The batch file method is the most robust way to ensure all sub-modules work correctly.
