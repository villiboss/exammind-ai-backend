#!/bin/bash

echo "===================================="
echo "   🚀 ExamMind AI (PRODUCTION MODE)"
echo "===================================="

cd "$(dirname "$0")"

# kill old server
pkill -f "uvicorn app.main:app" 2>/dev/null

# ensure DB exists
echo "🗄 Checking database..."
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)" || {
  echo "❌ DB init failed"
  exit 1
}

# start server (Termux-safe)
echo "🚀 Starting backend..."
uvicorn app.main:app --host 127.0.0.1 --port 8000
