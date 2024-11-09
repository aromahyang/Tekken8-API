check_error() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}


# Step 1: Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate
check_error "Failed to activate virtual environment."

# Step 2: Start the server
echo "Starting the server..."
uvicorn app.main:app --reload
check_error "Failed to start server."

exit 1