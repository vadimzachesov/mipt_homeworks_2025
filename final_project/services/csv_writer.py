import csv
import io
from dataclasses import asdict, fields
from pathlib import Path

from aiofile import async_open

from final_project.models.csv_models import RepositoryCsvRow


class CsvWriter:
    """CSV writer for writing repository data to a file."""

    async def write_repositories_csv(
        self,
        rows: list[RepositoryCsvRow],
        path: Path,
    ) -> None:
        """Write repository data to a CSV file."""
        fieldnames = RepositoryCsvRow.get_fieldnames()

        dataclass_field_names = [f.name for f in fields(RepositoryCsvRow)]
        header_map = dict(zip(dataclass_field_names, fieldnames, strict=True))

        async with async_open(path, "w") as afp:
            io_obj = io.StringIO()
            writer = csv.DictWriter(io_obj, fieldnames=fieldnames)

            writer.writeheader()
            await afp.write(io_obj.getvalue())
            io_obj.seek(0)
            io_obj.truncate(0)

            for row in rows:
                row_dict = asdict(row)
                formatted_row = {
                    header_map[key]: value for key, value in row_dict.items()
                }
                writer.writerow(formatted_row)
                await afp.write(io_obj.getvalue())
                io_obj.seek(0)
                io_obj.truncate(0)
