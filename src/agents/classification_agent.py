import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ClassificationAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_readme",
                    "description": "Fetch the README content of a repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner": {"type": "string"},
                            "repo": {"type": "string"}
                        },
                        "required": ["owner", "repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_languages",
                    "description": "Get programming languages used in a repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner": {"type": "string"},
                            "repo": {"type": "string"}
                        },
                        "required": ["owner", "repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "classify_industry",
                    "description": "Submit final industry classification",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo_name": {"type": "string"},
                            "industry_code": {"type": "string"},
                            "confidence": {"type": "string"},
                            "reasoning": {"type": "string"}
                        },
                        "required": ["repo_name", "industry_code", "confidence", "reasoning"]
                    }
                }
            }
        ]

    def run(self, repository):
        messages = [
            {
                "role": "system",
                "content": """You are an AI agent that classifies GitHub repositories into industry categories.
Industry codes: A(Agriculture), B(Mining), C(Manufacturing), D(Utilities),
E(Water), F(Construction), G(Trade), H(Transport), I(Hospitality),
J(Information/Tech), K(Finance), L(Real Estate), M(Professional),
N(Administrative), O(Public Admin), P(Education), Q(Health), R(Arts),
S(Other Services), T(Households), U(International)
Steps: 1) Review repo info 2) Fetch README if unclear 3) Classify using classify_industry tool"""
            },
            {
                "role": "user",
                "content": f"""Classify this repository:
Name: {repository['name']}
Description: {repository.get('description', 'No description')}
Language: {repository.get('language', 'Unknown')}
Topics: {', '.join(repository.get('topics', []))}
Stars: {repository.get('stargazers_count', 0)}"""
            }
        ]

        for _ in range(5):  # max 5 iteraciones
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            message = response.choices[0].message
            messages.append(message)

            if not message.tool_calls:
                break

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if function_name == "classify_industry":
                    return arguments

                elif function_name == "get_readme":
                    result = self._get_readme(arguments["owner"], arguments["repo"])
                elif function_name == "get_languages":
                    result = self._get_languages(arguments["owner"], arguments["repo"])
                else:
                    result = "Tool not found"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        return {"repo_name": repository["name"], "industry_code": "J", "confidence": "low", "reasoning": "Agent timeout"}

    def _get_readme(self, owner, repo):
        import base64
        headers = {"Authorization": f"token {self.github_token}"}
        try:
            r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/readme", headers=headers)
            content = base64.b64decode(r.json()["content"]).decode("utf-8")
            return content[:3000]
        except:
            return "README not found"

    def _get_languages(self, owner, repo):
        headers = {"Authorization": f"token {self.github_token}"}
        try:
            r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/languages", headers=headers)
            return r.json()
        except:
            return {}