import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class IndustryClassifier:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.industries = {
            "A": "Agriculture, forestry and fishing",
            "B": "Mining and quarrying",
            "C": "Manufacturing",
            "D": "Electricity, gas, steam supply",
            "E": "Water supply; sewerage",
            "F": "Construction",
            "G": "Wholesale and retail trade",
            "H": "Transportation and storage",
            "I": "Accommodation and food services",
            "J": "Information and communication",
            "K": "Financial and insurance activities",
            "L": "Real estate activities",
            "M": "Professional, scientific activities",
            "N": "Administrative and support activities",
            "O": "Public administration and defense",
            "P": "Education",
            "Q": "Human health and social work",
            "R": "Arts, entertainment and recreation",
            "S": "Other service activities",
            "T": "Activities of households",
            "U": "Extraterritorial organizations"
        }

    def classify_repository(self, name, description, readme, topics, language):
        prompt = f"""Analyze this GitHub repository and classify it into ONE industry category.

REPOSITORY:
- Name: {name}
- Description: {description or 'No description'}
- Language: {language or 'Not specified'}
- Topics: {', '.join(topics) if topics else 'None'}
- README: {readme[:2000] if readme else 'No README'}

INDUSTRIES:
{json.dumps(self.industries, indent=2)}

Respond ONLY in JSON:
{{
    "industry_code": "X",
    "industry_name": "Full industry name",
    "confidence": "high|medium|low",
    "reasoning": "Brief explanation"
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You classify GitHub repos by industry. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        text = response.choices[0].message.content
        clean = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)

    def batch_classify(self, repositories, batch_size=10):
        results = []
        for i, repo in enumerate(repositories):
            print(f"Clasificando {i+1}/{len(repositories)}: {repo.get('name', '')}")
            try:
                classification = self.classify_repository(
                    name=repo.get("name", ""),
                    description=repo.get("description", ""),
                    readme=repo.get("readme", ""),
                    topics=repo.get("topics", []),
                    language=repo.get("language", "")
                )
                results.append({
                    "repo_id": repo["id"],
                    "repo_name": repo["name"],
                    **classification
                })
            except Exception as e:
                print(f"Error clasificando {repo.get('name')}: {e}")
                results.append({
                    "repo_id": repo["id"],
                    "repo_name": repo["name"],
                    "industry_code": "J",
                    "industry_name": "Information and communication",
                    "confidence": "low",
                    "reasoning": "Classification failed, defaulting to J"
                })
        return results