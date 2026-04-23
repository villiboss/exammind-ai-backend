#!/bin/bash

echo "🛑 Stopping ExamMind AI Backend..."

pkill -f "uvicorn app.main:app"

echo "✅ Server stopped"
