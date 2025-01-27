from flask import Flask, render_template, jsonify, request
from data import getGoogleSeet
from source import process_local_csv
import json
import os
import math
import atexit  # For cleanup on app termination

app = Flask(__name__)

# Path to the pre-processed JSON file
JSON_FILE_PATH = 'data.json'

# Path to the temporary file
TMP_FILE_PATH = 'tmp/data.csv'

def load_donation_centers():
    """Load and clean donation center data from the JSON file."""
    process_local_csv(TMP_FILE_PATH)
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as json_file:
            donation_centers = json.load(json_file)
            
            # Clean the data to fix NaN or invalid values
            for center in donation_centers:
                for key, value in center.items():
                    # Check for None or NaN
                    if value is None or (isinstance(value, float) and math.isnan(value)):  # NaN check
                        center[key] = "-"  # Replace with placeholder "-"
                    elif value == '':  # Check for empty string
                        center[key] = "-"  # Replace empty strings with placeholder "-"
            
            return donation_centers
    else:
        print(f"JSON file not found at {JSON_FILE_PATH}")
        return []

# Cleanup function to delete the temporary file
def delete_tmp_file():
    """Delete the temporary file if it exists."""
    if os.path.exists(TMP_FILE_PATH):
        os.remove(TMP_FILE_PATH)
        print(f"Temporary file '{TMP_FILE_PATH}' has been deleted.")
    else:
        print(f"No temporary file '{TMP_FILE_PATH}' found to delete.")

# Ensure temporary file cleanup on app termination
atexit.register(delete_tmp_file)

# Route to display the donation centers page
@app.route('/')
def home():
    donation_centers = load_donation_centers()

    # Debug: Log the loaded data
    print(f"Loaded Donation Centers Data: {donation_centers}")

    if not donation_centers:  # If no data, set headers as an empty list
        headers = []
    else:
        headers = list(donation_centers[0].keys())  # Extract headers from the first record
    return render_template('index.html', donation_centers=donation_centers, headers=headers)

# Route to search for donation centers by item or volunteer need
@app.route('/api/search', methods=['GET'])
def search_donation_centers():
    query = request.args.get('query', '').lower()
    donation_centers = load_donation_centers()

    # Ensure keys match those used in the template and frontend
    results = [
        {
            "Name": center.get("Name", ""),
            "Location": center.get("Location", ""),
            "Aid Type": center.get("Aid Type", ""),
            "Dates": center.get("Dates", ""),
            "Address": center.get("Address", ""),
            # "Accepting": center.get("Accepting", ""),
            "Providing": center.get("Providing", ""),
            "Source": center.get("Source", ""),
            "LINK (DO NOT HYPERLINK)": center.get("LINK (DO NOT HYPERLINK)", ""),
            "Last Updated": center.get("Last Updated", ""),
        }
        for center in donation_centers
        if any(query in str(value).lower() for value in center.values())
    ]

    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if no PORT env is set
    app.run(host="0.0.0.0", port=port)


