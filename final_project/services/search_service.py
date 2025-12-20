import csv
import io
import os
from typing import List, Dict, Any, Optional
from aiofile import async_open
from final_project.infrastructure.github_client import GitHubClient


class SearchService:
    def __init__(self):
        self.client = GitHubClient()

    async def create_search_report(
            self,
            limit: int,
            offset: int,
            lang: str,
            stars_min: int = 0,
            stars_max: Optional[int] = None,
            forks_min: int = 0,
            forks_max: Optional[int] = None
    ) -> str:
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

        final_query = " ".join(query_parts)

        all_items: List[Dict[str, Any]] = []
        page = 1
        target_count = offset + limit

        while len(all_items) < target_count:
            data = await self.client.search_repositories(
                query=final_query,
                page=page,
                per_page=100
            )

            items = data.get("items", [])
            if not items:
                break

            all_items.extend(items)
            page += 1

            if len(items) < 100:
                break

        sliced_items = all_items[offset: offset + limit]

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        file_path = os.path.join("static", filename)

        await self._save_to_csv(sliced_items, file_path)

        return filename

    async def _save_to_csv(self, items: List[Dict[str, Any]], path: str):
        fieldnames = [
            'Name', 'Description', 'URL', 'Created At', 'Updated At', 'Homepage',
            'Size', 'Stars', 'Forks', 'Issues', 'Watchers', 'Language', 'License',
            'Topics', 'Has Issues', 'Has Projects', 'Has Downloads', 'Has Wiki',
            'Has Pages', 'Has Discussions', 'Is Fork', 'Is Archived', 'Is Template',
            'Default Branch'
        ]

        async with async_open(path, 'w') as afp:
            io_obj = io.StringIO()
            writer = csv.DictWriter(io_obj, fieldnames=fieldnames)

            writer.writeheader()
            await afp.write(io_obj.getvalue())
            io_obj.seek(0)
            io_obj.truncate(0)

            for item in items:
                row = self._map_item_to_row(item)
                writer.writerow(row)
                await afp.write(io_obj.getvalue())
                io_obj.seek(0)
                io_obj.truncate(0)

    def _map_item_to_row(self, item: Dict[str, Any]) -> Dict[str, Any]:
        license_data = item.get('license')
        license_name = license_data.get('spdx_id') if license_data else None

        return {
            'Name': item.get('name'),
            'Description': item.get('description'),
            'URL': item.get('html_url'),
            'Created At': item.get('created_at'),
            'Updated At': item.get('updated_at'),
            'Homepage': item.get('homepage'),
            'Size': item.get('size'),
            'Stars': item.get('stargazers_count'),
            'Forks': item.get('forks_count'),
            'Issues': item.get('open_issues_count'),
            'Watchers': item.get('watchers_count'),
            'Language': item.get('language'),
            'License': license_name,
            'Topics': str(item.get('topics', [])),
            'Has Issues': item.get('has_issues'),
            'Has Projects': item.get('has_projects'),
            'Has Downloads': item.get('has_downloads'),
            'Has Wiki': item.get('has_wiki'),
            'Has Pages': item.get('has_pages'),
            'Has Discussions': item.get('has_discussions', False),
            'Is Fork': item.get('fork'),
            'Is Archived': item.get('archived'),
            'Is Template': item.get('is_template', False),
            'Default Branch': item.get('default_branch')
        }
