check_error() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}


# Step 1: Set up virtual environment
echo "Setting up virtual environment..."
py -m venv venv
check_error "Failed to create virtual environment."

# Step 2: Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate
check_error "Failed to activate virtual environment."

# Step 3: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
check_error "Failed to install dependencies."

exit 1