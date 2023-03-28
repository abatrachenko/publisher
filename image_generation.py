import os
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def generate_image(prompt, size="1024x1024", n=1, variations=False):
    if not variations:
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        data = {
            "prompt": prompt,
            "n": n,
            "size": size
        }
        response = requests.post(url, headers=headers, json=data)
    else:
        # First, generate an image
        base_image_url = generate_image(prompt, size=size, n=1)
        base_image = requests.get(base_image_url).content

        url = "https://api.openai.com/v1/images/variations"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        files = {
            "image": (f"{prompt}.png", base_image, "image/png")
        }
        data = {
            "n": 4,  # Number of variations to generate
            "size": size
        }
        response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        json_response = response.json()
        if variations:
            return [image["url"] for image in json_response["data"]]
        else:
            return json_response["data"][0]["url"]
    else:
        raise Exception(f"Failed to generate image. Status code: {response.status_code}. Error: {response.text}")
