from src.extraction.github_client import GitHubClient

class UserExtractor:
    def __init__(self, client: GitHubClient):
        self.client = client

    def search_users_by_location(self, location, max_users=1000):
        users = []
        page = 1
        while len(users) < max_users:
            result = self.client.make_request(
                "search/users",
                params={
                    "q": f"location:{location}",
                    "per_page": 100,
                    "page": page,
                    "sort": "followers",
                    "order": "desc"
                }
            )
            if not result.get("items"):
                break
            users.extend(result["items"])
            page += 1
            if page * 100 >= 1000:
                break
        return users[:max_users]

    def get_user_details(self, username):
        return self.client.make_request(f"users/{username}")

    def get_user_repos(self, username):
        repos = []
        page = 1
        while True:
            result = self.client.make_request(
                f"users/{username}/repos",
                params={"per_page": 100, "page": page, "type": "owner"}
            )
            if not result:
                break
            repos.extend(result)
            page += 1
        return repos