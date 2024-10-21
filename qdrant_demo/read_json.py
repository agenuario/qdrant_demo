import json
import os.path

# Opening JSON file
payload_path = 'C:\\Users\\agenuario\\source\\repos\\qdrant_demo\\data\\pdc_1.json'
f = open(payload_path)

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
for i in data:
    print(i)

# Closing file
f.close()