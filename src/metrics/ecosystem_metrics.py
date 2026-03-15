from collections import Counter

def calculate_ecosystem_metrics(users_df, repos_df, classifications_df):
    metrics = {}
    metrics["total_developers"] = len(users_df)
    metrics["total_repositories"] = len(repos_df)
    metrics["total_stars"] = int(repos_df["stargazers_count"].sum())
    metrics["avg_repos_per_user"] = round(repos_df.groupby("owner_login").size().mean(), 2)
    metrics["most_popular_languages"] = (
        repos_df["language"].dropna().value_counts().head(10).to_dict()
    )
    metrics["industry_distribution"] = (
        classifications_df["industry_name"].value_counts().to_dict()
    )
    metrics["active_developer_pct"] = round(
        (users_df["is_active"].sum() / len(users_df)) * 100, 2
    )
    metrics["avg_account_age_days"] = round(users_df["account_age_days"].mean(), 2)
    return metrics