#!/usr/bin/env bash
set -euo pipefail
[ -d data/raw ] || bash src/00_download.sh
python3 src/01_load.py data/raw
python3 src/02_run_queries.py
python3 src/03_dashboard.py
echo "Dashboard written to docs/index.html"
