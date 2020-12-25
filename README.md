# external-ip
Report the public IP of your device by uploading a file to Google Storage.

## Install

`git clone https://github.com/dylancaponi/external-ip.git`

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip install -r reqs.txt`

## Setup

Create a Google Service Account here: https://console.cloud.google.com/identity/serviceaccounts

Add a key and download that to the same folder as this repo

Set `GOOGLE_CREDS` in main.py to the filename of your downloaded key

Add your service account in IAM: https://console.cloud.google.com/access/iam

Give it `Storage Object Creator` roles

Edit these values to match your setup:
```
GOOGLE_CREDS = '<service-role-that-can-upload-to-cloud-storage>.json'
BUCKET_NAME = '<bucket-name-for-data>'
BUCKET_FOLDER = '<bucket-folder-for-data>'
```

## Run

`python main.py`
