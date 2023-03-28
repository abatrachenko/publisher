import os
import requests
import base64

WP_API_BASE_URL = os.environ.get("WP_API_BASE_URL")
USERNAME = os.environ.get("WP_USERNAME")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD")

def publish_post(title, content, json_ld_markup, featured_image_url=None):
    url = f"{WP_API_BASE_URL}/wp-json/wp/v2/posts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64.b64encode(f'{USERNAME}:{APP_PASSWORD}'.encode('utf-8')).decode('utf-8')}"
    }
    data = {
        "title": title,
        "content": content + f'\n\n<script type="application/ld+json">{json_ld_markup}</script>',
        "status": "publish"
    }

    if featured_image_url:
        media_id = upload_featured_image(featured_image_url)
        data["featured_media"] = media_id

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Successfully published post.")
    else:
        raise Exception(f"Failed to publish post. Status code: {response.status_code}. Error: {response.text}")

def upload_featured_image(image_url):
    url = f"{WP_API_BASE_URL}/wp-json/wp/v2/media"
    headers = {
        "Content-Type": "image/png",
        "Content-Disposition": 'attachment; filename="featured_image.png"',
        "Authorization": f"Basic {base64.b64encode(f'{USERNAME}:{APP_PASSWORD}'.encode('utf-8')).decode('utf-8')}"
    }

    response = requests.get(image_url)
    image_data = response.content

    upload_response = requests.post(url, headers=headers, data=image_data)

    if upload_response.status_code == 201:
        json_response = upload_response.json()
        return json_response["id"]
    else:
        raise Exception(f"Failed to upload featured image. Status code: {upload_response.status_code}. Error: {upload_response.text}")
