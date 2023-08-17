import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(image_prompt, n=4, size="1024x1024"):
    response = openai.Image.create(
        prompt=image_prompt,
        n=n,
        size=size
    )

    if response is not None and "data" in response:
        # Extract URLs from the response
        return [item["url"] for item in response["data"]]
    else:
        raise Exception("Failed to generate image.")

