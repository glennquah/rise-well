import os
import requests

CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
UPLOAD_PRESET = os.getenv("CLOUDINARY_UPLOAD_PRESET", "")
CLOUDINARY_URL = f"https://api.cloudinary.com/v1_1/{CLOUD_NAME}/auto/upload"

def upload_image_to_cloudinary(image_path):
    with open(image_path, "rb") as file:
        files = {"file": file}
        data = {"upload_preset": UPLOAD_PRESET}

        response = requests.post(CLOUDINARY_URL, files=files, data=data)

    if response.status_code == 200:
        url = response.json().get("secure_url")
        print("✅ Uploaded to Cloudinary:", url)
        return url
    else:
        print("❌ Upload failed:", response.text)
        return None
