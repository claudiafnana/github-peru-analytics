import json
import pandas as pd
from src.extraction.github_client import GitHubClient
from src.extraction.user_extractor import UserExtractor
from src.extraction.repo_extractor import RepoExtractor

def main():
    print("Iniciando extracción de datos...")
    client = GitHubClient()
    user_extractor = UserExtractor(client)
    repo_extractor = RepoExtractor(client)

    # Buscar usuarios de Peru
    print("Buscando usuarios de Peru...")
    all_users = []
    for location in ["Peru", "Lima", "Arequipa", "Cusco", "Trujillo"]:
        print(f"  Buscando en: {location}")
        users = user_extractor.search_users_by_location(location, max_users=200)
        all_users.extend(users)

    # Eliminar duplicados
    seen = set()
    unique_users = []
    for u in all_users:
        if u["login"] not in seen:
            seen.add(u["login"])
            unique_users.append(u)
    print(f"Total usuarios únicos: {len(unique_users)}")

    # Obtener detalles de usuarios y sus repos
    all_repos = []
    users_detail = []
    for i, user in enumerate(unique_users[:200]):  # limitamos a 200 para no gastar rate limit
        print(f"Procesando usuario {i+1}/{min(200, len(unique_users))}: {user['login']}")
        try:
            detail = user_extractor.get_user_details(user["login"])
            users_detail.append(detail)
            repos = user_extractor.get_user_repos(user["login"])
            for r in repos:
                r["owner_login"] = user["login"]
            all_repos.extend(repos)
        except Exception as e:
            print(f"Error con {user['login']}: {e}")
            continue

    # Obtener READMEs
    print("Obteniendo READMEs...")
    for i, repo in enumerate(all_repos[:1000]):
        if i % 50 == 0:
            print(f"  README {i}/{min(1000, len(all_repos))}")
        owner = repo.get("owner_login", "")
        name = repo.get("name", "")
        repo["readme"] = repo_extractor.get_repo_readme(owner, name)

    # Guardar datos
    users_df = pd.DataFrame(users_detail)
    repos_df = pd.DataFrame(all_repos[:1000])

    users_df.to_csv("data/processed/users.csv", index=False)
    repos_df.to_csv("data/processed/repositories.csv", index=False)
    print(f"Guardado: {len(users_df)} usuarios y {len(repos_df)} repositorios")

if __name__ == "__main__":
    main()