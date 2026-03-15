import json
import pandas as pd
from src.metrics.user_metrics import UserMetricsCalculator
from src.metrics.ecosystem_metrics import calculate_ecosystem_metrics

def main():
    print("Calculando métricas...")
    users_df = pd.read_csv("data/processed/users.csv")
    repos_df = pd.read_csv("data/processed/repositories.csv")
    classifications_df = pd.read_csv("data/processed/classifications.csv")

    calculator = UserMetricsCalculator()
    user_metrics_list = []

    for _, user in users_df.iterrows():
        user_repos = repos_df[repos_df["owner_login"] == user["login"]].to_dict("records")
        user_classifications = classifications_df[
            classifications_df["repo_name"].isin([r["name"] for r in user_repos])
        ].to_dict("records")

        metrics = calculator.calculate_all_metrics(user.to_dict(), user_repos, user_classifications)
        metrics["login"] = user["login"]
        metrics["name"] = user.get("name", "")
        user_metrics_list.append(metrics)

    metrics_df = pd.DataFrame(user_metrics_list)
    metrics_df.to_csv("data/metrics/user_metrics.csv", index=False)

    ecosystem = calculate_ecosystem_metrics(metrics_df, repos_df, classifications_df)
    with open("data/metrics/ecosystem_metrics.json", "w") as f:
        json.dump(ecosystem, f, indent=2)

    print(f"Métricas calculadas para {len(metrics_df)} usuarios")

if __name__ == "__main__":
    main()