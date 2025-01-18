import pandas as pd
import json

  # Update this path if the file is stored elsewhere

def process_local_csv(file_path):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)

        # Debug: Show initial data structure
        print(f"Initial data shape: {df.shape}")
        print("Preview of raw data:")
        print(df.head(10))

        # Check if there are enough rows and columns
        if len(df) < 4 or len(df.columns) < 13:  # Adjust column count if necessary
            print(f"Insufficient data: {len(df)} rows and {len(df.columns)} columns found.")
            return

        # Set headers from row 4 (index 3) based on available columns
        headers = df.iloc[1].values[:13]  # Use the first 13 columns as headers
        df = df.iloc[2:]  # Data starts from row 5 (index 4)
        df.columns = headers

        # Drop empty rows and columns
        df = df.dropna(how="all").reset_index(drop=True)
        df = df.dropna(axis=1, how="all")

        # Convert the cleaned DataFrame to JSON
        json_data = df.to_dict(orient="records")
        with open("data.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        print("Data processed and saved to 'data.json'.")
        print("Sample JSON preview:")
        print(json.dumps(json_data[:2], indent=4))  # Preview first 2 records

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
file_path = "data.csv"  # Ensure this is the correct file path
process_local_csv(file_path)





