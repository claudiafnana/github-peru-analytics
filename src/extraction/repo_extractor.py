import base64
from src.extraction.github_client import GitHubClient

class RepoExtractor:
    def __init__(self, client: GitHubClient):
        self.client = client

    def search_repos_by_stars(self, location_users, min_stars=1):
        repos = []
        for username in location_users:
            try:
                user_repos = self.client.make_request(
                    f"users/{username}/repos",
                    params={"sort": "stars", "direction": "desc"}
                )
                for repo in user_repos:
                    if repo["stargazers_count"] >= min_stars:
                        repos.append(repo)
            except Exception as e:
                print(f"Error con usuario {username}: {e}")
                continue
        repos.sort(key=lambda x: x["stargazers_count"], reverse=True)
        return repos[:1000]

    def get_repo_readme(self, owner, repo):
        try:
            result = self.client.make_request(f"repos/{owner}/{repo}/readme")
            content = base64.b64decode(result["content"]).decode("utf-8")
            return content[:5000]
        except Exception:
            return ""

    def get_repo_languages(self, owner, repo):
        try:
            return self.client.make_request(f"repos/{owner}/{repo}/languages")
        except Exception:
            return {}