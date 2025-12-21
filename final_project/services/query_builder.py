def build_github_search_query(
    lang: str,
    stars_min: int = 0,
    stars_max: int | None = None,
    forks_min: int = 0,
    forks_max: int | None = None,
    created_from: str | None = None,
    created_to: str | None = None
) -> str:
    """Build a GitHub search query based on the provided parameters."""
    query_parts = []

    if lang:
        query_parts.append(f"language:{lang}")

    if stars_max:
        query_parts.append(f"stars:{stars_min}..{stars_max}")
    else:
        query_parts.append(f"stars:>={stars_min}")

    if forks_max:
        query_parts.append(f"forks:{forks_min}..{forks_max}")
    else:
        query_parts.append(f"forks:>={forks_min}")

    if created_from and created_to:
        query_parts.append(f"created:{created_from}..{created_to}")
    elif created_from:
        query_parts.append(f"created:>={created_from}")
    elif created_to:
        query_parts.append(f"created:<={created_to}")

    return " ".join(query_parts)
