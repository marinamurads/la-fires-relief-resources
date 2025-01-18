import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_data_and_convert_to_json():
    # Fetch the spreadsheet HTML
    url = 'https://docs.google.com/spreadsheets/d/1KMk34XY5dsvVJjAoD2mQUVHYU_Ib6COz6jcGH5uJWDY/edit?usp=sharing'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table
    table = soup.find('table')

    # Extract rows from the table
    data = []
    for row in table.find_all('tr'):
        columns = [col.text.strip() for col in row.find_all('td')]
        if columns:  # Skip empty rows
            data.append(columns)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Ensure there are enough rows and columns
    if len(df) >= 4 and len(df.columns) >= 37:
        # Set headers from row 3 (index 2)
        headers = df.iloc[2].values[:37]  # First 37 columns as headers
        df = df.iloc[4:]  # Data starts from row 4
        df.columns = headers  # Set headers
        
        # Remove any rows that have a lot of empty columns
        df = df.dropna(how='all').reset_index(drop=True)

        # Remove any columns that are completely empty
        df = df.dropna(axis=1, how='all')

        # Ensure the columns are aligned by resetting the DataFrame index and cleaning up unwanted columns
        df = df.reset_index(drop=True)

    else:
        print("The table doesn't have enough rows or columns to extract the data.")
        return None

    # Convert the DataFrame to a list of dictionaries
    json_data = df.to_dict(orient='records')

    # Save the JSON data to a file
    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("Data has been converted to JSON and saved to 'data.json'.")

    return json_data



# Call the function
try:
    json_output = scrape_data_and_convert_to_json()
    if json_output:
        # Print a preview of the JSON data
        print("JSON Preview (First 2 Records):")
        print(json.dumps(json_output[:2], indent=4))
except Exception as e:
    print(f"Error occurred: {e}")













