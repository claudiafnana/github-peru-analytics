import json
import pandas as pd
from src.classification.industry_classifier import IndustryClassifier

def main():
    print("Iniciando clasificación...")
    repos_df = pd.read_csv("data/processed/repositories.csv")
    classifier = IndustryClassifier()

    repos_list = repos_df.fillna("").to_dict("records")

    results = classifier.batch_classify(repos_list[:1000])

    classifications_df = pd.DataFrame(results)
    classifications_df.to_csv("data/processed/classifications.csv", index=False)
    print(f"Clasificados: {len(classifications_df)} repositorios")

if __name__ == "__main__":
    main()