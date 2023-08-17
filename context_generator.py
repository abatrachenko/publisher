import os
import requests
import json
import time

GOOGLE_SEARCH_API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

def get_search_results(query, num_results=2):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        return [item["link"] for item in results["items"]]
    else:
        raise Exception(f"Search failed with status {response.status_code}")


def get_summary(url):
    # Introduce a delay before making the request to adhere to the API's rate limit.
    time.sleep(12)  # wait for 12 seconds

    # Encode the URL to ensure it's correctly formatted for the API.
    encoded_url = requests.utils.quote(url, safe='')
    
    # Construct the API URL with the provided parameters.
    smmry_url = f"http://api.smmry.com/?SM_API_KEY=198C35D20D&SM_QUOTE_AVOID&SM_QUESTION_AVOID&SM_EXCLAMATION_AVOID&SM_LENGTH=15&SM_URL={encoded_url}"

    # Make the GET request to the smmry API.
    response = requests.get(smmry_url)

    # If the request is successful, retrieve and return the summary.
    if response.status_code == 200:
        summary = response.json()
        return summary["sm_api_content"]
    else:
        # Try to extract a more descriptive error message if it's present.
        try:
            error_message = response.json().get('sm_api_message', '')
        except:
            error_message = ''

        raise Exception(f"Summarization failed with status {response.status_code}. Message: {error_message}")


def generate_context(question):
    search_urls = get_search_results(question)
    
    for url in search_urls:
        try:
            summary = get_summary(url)
            return summary
        except:
            continue  # Move to the next URL if summarization fails
    
    raise Exception("Failed to generate context after trying multiple URLs.")

