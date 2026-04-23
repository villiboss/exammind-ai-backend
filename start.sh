#!/bin/bash

echo "================================="
echo "   🚀 ExamMind AI Backend"
echo "================================="

cd "$(dirname "$0")"

# kill old server if running
pkill -f "uvicorn app.main:app" 2>/dev/null

# safety check
if [ ! -f "app/main.py" ]; then
  echo "❌ main.py not found!"
  exit 1
fi

echo "🔄 Starting server..."

# IMPORTANT: NO reload (Termux fix)
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000
