#!/bin/bash

# Exit on error
set -e

# Virtual environment directory
VENV_DIR="venv"

# Step 1: Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv $VENV_DIR
else
  echo "Virtual environment already exists."
fi

# Step 2: Activate virtual environment
source "$VENV_DIR/bin/activate"

# Step 3: Install dependencies
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Post-setup message
echo
echo "✅ Setup complete!"
echo "👉 Please rename '.env.py' to 'env.py' and add the required fields:"
echo "   - host"
echo "   - user"
echo "   - password"
echo "   - database"
