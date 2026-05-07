import csv
from pathlib import Path
from typing import List
from core.models import Video


def load_videos_from_files(file_paths: List[str]) -> List[Video]:
    """Load and combine videos from multiple CSV files."""
    videos = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        videos.extend(_load_videos_from_single_file(path))
    return videos


def _load_videos_from_single_file(file_path: Path) -> List[Video]:
    """Load videos from a single CSV file."""
    videos = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_columns = {"title", "ctr", "retention_rate", "views", "likes", "avg_watch_time"}

        if not required_columns.issubset(reader.fieldnames or []):
            missing = required_columns - set(reader.fieldnames or [])
            raise ValueError(f"File {file_path} missing required columns: {missing}")

        for row in reader:
            try:
                videos.append(Video.from_csv_row(row))
            except (ValueError, KeyError) as e:
                raise ValueError(f"Invalid data in {file_path}: {e}")

    return videos