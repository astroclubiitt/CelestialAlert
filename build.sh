
# Exit if error is encountered
set -o errexit

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt
