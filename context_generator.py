import os
import requests
import json

GOOGLE_SEARCH_API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

def get_search_results(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 1
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        return results["items"][0]["link"]
    else:
        raise Exception(f"Search failed with status {response.status_code}")

def get_summary(url):
    smmry_url = f"http://api.smmry.com/&SM_API_KEY=198C35D20D&SM_URL={url}"
    response = requests.get(smmry_url)

    if response.status_code == 200:
        summary = response.json()
        return summary["sm_api_content"]
    else:
        raise Exception(f"Summarization failed with status {response.status_code}")

def generate_context(question):
    search_url = get_search_results(question)
    summary = get_summary(search_url)
    return summary
