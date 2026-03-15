from datetime import datetime
from collections import Counter

class UserMetricsCalculator:
    def __init__(self):
        self.today = datetime.now()

    def calculate_all_metrics(self, user, repos, classifications):
        metrics = {}

        # Activity
        metrics["total_repos"] = len(repos)
        metrics["total_stars_received"] = sum(r["stargazers_count"] for r in repos)
        metrics["total_forks_received"] = sum(r["forks_count"] for r in repos)
        metrics["avg_stars_per_repo"] = (
            metrics["total_stars_received"] / metrics["total_repos"]
            if metrics["total_repos"] > 0 else 0
        )
        created_at = datetime.fromisoformat(user["created_at"].replace("Z", ""))
        metrics["account_age_days"] = (self.today - created_at).days
        metrics["repos_per_year"] = (
            metrics["total_repos"] / (metrics["account_age_days"] / 365)
            if metrics["account_age_days"] > 0 else 0
        )

        # Influence
        metrics["followers"] = user.get("followers", 0)
        metrics["following"] = user.get("following", 0)
        metrics["follower_ratio"] = (
            metrics["followers"] / metrics["following"]
            if metrics["following"] > 0 else metrics["followers"]
        )
        metrics["h_index"] = self._calculate_h_index(repos)
        metrics["impact_score"] = (
            metrics["total_stars_received"] +
            (metrics["total_forks_received"] * 2) +
            metrics["followers"]
        )

        # Technical
        languages = [r["language"] for r in repos if r.get("language")]
        lang_counts = Counter(languages)
        metrics["primary_languages"] = [l for l, _ in lang_counts.most_common(3)]
        metrics["primary_language_1"] = metrics["primary_languages"][0] if metrics["primary_languages"] else None
        metrics["language_diversity"] = len(set(languages))

        industry_codes = [c["industry_code"] for c in classifications]
        metrics["industries_served"] = len(set(industry_codes))
        metrics["primary_industry"] = Counter(industry_codes).most_common(1)[0][0] if industry_codes else None

        # Documentation
        repos_with_license = sum(1 for r in repos if r.get("license"))
        metrics["has_license_pct"] = repos_with_license / len(repos) if repos else 0

        # Engagement
        metrics["total_open_issues"] = sum(r["open_issues_count"] for r in repos)
        if repos:
            last_push = max(
                datetime.fromisoformat(r["pushed_at"].replace("Z", ""))
                for r in repos if r.get("pushed_at")
            )
            metrics["days_since_last_push"] = (self.today - last_push).days
            metrics["is_active"] = metrics["days_since_last_push"] < 90
        else:
            metrics["days_since_last_push"] = None
            metrics["is_active"] = False

        return metrics

    def _calculate_h_index(self, repos):
        stars = sorted([r["stargazers_count"] for r in repos], reverse=True)
        h = 0
        for i, s in enumerate(stars):
            if s >= i + 1:
                h = i + 1
            else:
                break
        return h