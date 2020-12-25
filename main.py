from datetime import datetime, timezone
import json
import os

import requests

from google.cloud import storage

# Get datetime
dt = datetime.now(timezone.utc)
dtstr = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
out_file = f'{dt.strftime("%Y-%m-%d-%H-%M-%S")}.json'
TMP_FILE = 'last_ip.json'
GOOGLE_CREDS = '<service-role-that-can-upload-to-cloud-storage>.json'
BUCKET_NAME = '<bucket-name-for-data>'
BUCKET_FOLDER = '<bucket-folder-for-data>'

# Load data if file exists
try:
    with open(TMP_FILE, 'r') as f:
        data = json.load(f)
except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
    data = {}

# Get external IP
r = requests.get('http://ifconfig.me')
r.raise_for_status()
external_ip = r.text
# TODO - confirm it is in IP format

# Quit if IP has not changed
if data.get('external_ip') == external_ip:
    print(f"IP has not changed: {external_ip}")
    quit()

# Log change
print(f"IP changed to {external_ip} from {data.get('external_ip')}")

# Create payload
new_data = {"datetime": dtstr, "external_ip": external_ip}
out_data = json.dumps(new_data)

# Upload file to Google Storage
print('Upload to Google Storage')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CREDS
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(f'{BUCKET_FOLDER}/{out_file}')
blob.upload_from_string(out_data)

# If it changed overwrite local file
print('Overwrite local file')
with open(TMP_FILE, 'w') as f:
    f.write(out_data)
