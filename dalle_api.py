import os
import requests
import json

API_KEY = os.environ["DALLE_API_KEY"]
API_BASE_URL = "https://api.openai.com/v1/images"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def generate_image(prompt, n=1, size="1024x1024"):
    data = {
        "prompt": prompt,
        "n": n,
        "size": size
    }
    response = requests.post(f"{API_BASE_URL}/generations", headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()["data"][0]["url"]

def edit_image(image_path, mask_path, prompt, n=1, size="1024x1024"):
    with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
        files = {
            "image": image_file,
            "mask": mask_file
        }
        data = {
            "prompt": prompt,
            "n": n,
            "size": size
        }
        response = requests.post(f"{API_BASE_URL}/edits", headers=headers, data=data, files=files)
        response.raise_for_status()
        return response.json()["data"][0]["url"]

def generate_variations(image_path, n=4, size="1024x1024"):
    with open(image_path, "rb") as image_file:
        files = {
            "image": image_file
        }
        data = {
            "n": n,
            "size": size
        }
        response = requests.post(f"{API_BASE_URL}/variations", headers=headers, data=data, files=files)
        response.raise_for_status()
        return [img["url"] for img in response.json()["data"]]
