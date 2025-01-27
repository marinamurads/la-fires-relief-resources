import pandas as pd
import json
from data import getGoogleSeet

def process_local_csv(file_path):
    try:
        # Step 1: Retrieve the CSV file
        getGoogleSeet('1KMk34XY5dsvVJjAoD2mQUVHYU_Ib6COz6jcGH5uJWDY', 'tmp/', "data.csv")
        
        # Step 2: Handle potential CSV parsing errors
        # Use "on_bad_lines='skip'" to skip malformed rows
        df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
        
        # Debug: Show initial data structure
        print(f"Initial data shape: {df.shape}")
        print("Preview of raw data:")
        print(df.head(10))

        # Step 3: Check for sufficient rows and columns
        if len(df) < 4 or len(df.columns) < 13:
            print(f"Insufficient data: {len(df)} rows and {len(df.columns)} columns found.")
            return

        # Step 4: Set headers from row 2 (adjust column count as needed)
        headers = df.iloc[1].values[:15]  # Assuming the first 15 columns are relevant
        df = df.iloc[2:]  # Skip the header row and prior rows
        df.columns = headers

        # Step 5: Clean up the DataFrame
        # Remove empty rows and columns
        df = df.dropna(how="all").reset_index(drop=True)
        df = df.dropna(axis=1, how="all")

        # Step 6: Convert DataFrame to JSON and save it
        json_data = df.to_dict(orient="records")
        with open("data.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        print("Data processed and saved to 'data.json'.")
        print("Sample JSON preview:")
        print(json.dumps(json_data[:2], indent=4))  # Preview first 2 records

    except Exception as e:
        print(f"An error occurred while processing the CSV: {e}")

# Run the function
file_path = "tmp/data.csv"  # Ensure this is the correct file path
process_local_csv(file_path)





