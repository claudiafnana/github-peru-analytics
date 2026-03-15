import os
import time
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def check_rate_limit(self):
        response = requests.get(f"{self.base_url}/rate_limit", headers=self.headers)
        return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60))
    def make_request(self, endpoint, params=None):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            params=params
        )
        remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
        if remaining < 10:
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            sleep_time = max(reset_time - time.time(), 0) + 5
            print(f"Rate limit casi alcanzado. Esperando {sleep_time:.0f} segundos...")
            time.sleep(sleep_time)
        response.raise_for_status()
        return response.json()