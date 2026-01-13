#!/bin/bash
# Startup script for Trading Suite
echo "🚀 Launching Trading Suite on Port 8510..."
source venv/bin/activate
# Use 0.0.0.0 to ensure it's accessible on the network too
streamlit run Home.py --server.port 8510 --server.address 0.0.0.0
