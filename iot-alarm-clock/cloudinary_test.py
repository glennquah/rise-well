import os
import requests

# Your Cloudinary credentials
CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
UPLOAD_PRESET = os.getenv("CLOUDINARY_UPLOAD_PRESET", "")
UPLOAD_URL = f"https://api.cloudinary.com/v1_1/{CLOUD_NAME}/auto/upload"

# Replace with an existing image path on your Pi
TEST_IMAGE = os.getenv("TEST_IMAGE", "test-image.jpg")
def upload_image(path):
    with open(path, "rb") as f:
        files = {"file": f}
        data = {"upload_preset": UPLOAD_PRESET}

        print("📤 Uploading to Cloudinary...")
        response = requests.post(UPLOAD_URL, files=files, data=data)

    if response.status_code == 200:
        image_url = response.json().get("secure_url")
        print("✅ Uploaded successfully!")
        print("🌐 URL:", image_url)
    else:
        print("❌ Upload failed.")
        print(response.status_code)
        print(response.text)

upload_image(TEST_IMAGE)
