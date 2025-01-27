import os
import requests
import sys

def getGoogleSeet(spreadsheet_id, outDir, outFile):
  print({spreadsheet_id})
  url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'
  response = requests.get(url)
  if response.status_code == 200:
    filepath = os.path.join(outDir, outFile)
    with open(filepath, 'wb') as f:
      f.write(response.content)
      print('CSV file saved to: {}'.format(filepath))    
  else:
    print(f'Error downloading Google Sheet: {response.status_code}')
    sys.exit(1)

outDir = 'tmp/'

os.makedirs(outDir, exist_ok = True)
filepath = getGoogleSeet('1KMk34XY5dsvVJjAoD2mQUVHYU_Ib6COz6jcGH5uJWDY', outDir, "data.csv")

#sys.exit(0); ## success













