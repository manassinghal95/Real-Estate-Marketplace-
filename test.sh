#!/bin/bash

# Define terminal colors
DEEP_PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to display the menu
show_menu() {
    echo -e "${DEEP_PURPLE}"
    echo '================================================='
    echo '                   T-CHAT MENU                   '
    echo '================================================='
    echo '  1. Start Server'
    echo '  2. Start Client'
    echo '  3. Exit'
    echo '================================================='
    echo -e "${NC}"
    echo -n "Enter your choice (1-3): "
}

# Clear screen and set title
clear
echo -e "\033]0;T-CHAT\007"

# Print "T-CHAT" in block letters with deep purple color
echo -e "${DEEP_PURPLE}"
echo '████████╗       ██████╗██╗  ██╗ █████╗ ████████╗'
echo '╚══██╔══╝      ██╔════╝██║  ██║██╔══██╗╚══██╔══╝'
echo '   ██║  █████╗ ██║     ███████║███████║   ██║   '
echo '   ██║  ╚════╝ ██║     ██╔══██║██╔══██║   ██║   '
echo '   ██║         ╚██████╗██║  ██║██║  ██║   ██║   '
echo '   ╚═╝          ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   '
echo -e "${NC}"

# Show initial menu
show_menu

# Read user input for menu choice
read choice

# Process user choice
case $choice in
    1)
        echo "Starting server..."
        ./server &    # Start the server in the background
        sleep 1       # Give some time for the server to start (adjust as needed)
        ;;
    2)
        echo "Starting client..."
        ./client      # Start the client
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please enter a number from 1 to 3."
        ;;
esac

# Clean up after program ends (if needed)
# Example: killall server

exit 0
