#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🏗️  Setting up your Flask Champions League app..."

# 1. Create virtual environment if it doesn’t exist
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
else
  echo "✅ Virtual environment already exists."
fi

# 2. Activate the virtual environment
echo "🟢 Activating virtual environment..."
source venv/bin/activate

# 3. Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 4. Install dependencies
echo "📚 Installing Flask, Requests, and python-dotenv..."
pip install flask requests python-dotenv

# 5. Create requirements.txt
echo "🧾 Freezing dependencies..."
pip freeze > requirements.txt

echo "✅ Setup complete!"
echo "👉 To start the app, run: source venv/bin/activate && python app.py"
