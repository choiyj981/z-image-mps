#!/bin/bash
# 인터랙티브 CLI 실행 스크립트

cd "$(dirname "$0")"
source .venv/bin/activate
python interactive_cli.py
