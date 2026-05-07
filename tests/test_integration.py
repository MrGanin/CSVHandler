import subprocess
import tempfile
from pathlib import Path
import csv


def create_test_csv(path: Path, rows: list):
    """Helper to create a CSV file with given rows (list of dicts)."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "ctr", "retention_rate", "views", "likes", "avg_watch_time"])
        writer.writeheader()
        writer.writerows(rows)


def test_cli_with_valid_files():
    rows1 = [
        {"title": "Clickbait video A", "ctr": "20.0", "retention_rate": "30", "views": "1000", "likes": "100", "avg_watch_time": "4.0"},
        {"title": "Good video B", "ctr": "10.0", "retention_rate": "80", "views": "500", "likes": "50", "avg_watch_time": "8.0"},
    ]
    rows2 = [
        {"title": "Clickbait video C", "ctr": "18.5", "retention_rate": "35", "views": "800", "likes": "80", "avg_watch_time": "3.5"},
        {"title": "Clickbait video D", "ctr": "25.0", "retention_rate": "20", "views": "2000", "likes": "200", "avg_watch_time": "2.0"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f1:
        path1 = Path(f1.name)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f2:
        path2 = Path(f2.name)

    try:
        create_test_csv(path1, rows1)
        create_test_csv(path2, rows2)

        result = subprocess.run(
            ["python", "main.py", "--files", str(path1), str(path2), "--report", "clickbait"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Clickbait video D" in result.stdout  # CTR 25.0
        assert "Clickbait video A" in result.stdout  # CTR 20.0
        assert "Clickbait video C" in result.stdout  # CTR 18.5
        assert "Good video B" not in result.stdout
    finally:
        path1.unlink(missing_ok=True)
        path2.unlink(missing_ok=True)


def test_cli_file_not_found():
    result = subprocess.run(
        ["python", "main.py", "--files", "nonexistent.csv", "--report", "clickbait"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "File not found" in result.stderr


def test_cli_unknown_report():
    rows = [{"title": "Test", "ctr": "10.0", "retention_rate": "50", "views": "100", "likes": "10", "avg_watch_time": "5.0"}]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        create_test_csv(Path(f.name), rows)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["python", "main.py", "--files", tmp_path, "--report", "unknown_report_type"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "Unknown report" in result.stderr
    finally:
        Path(tmp_path).unlink(missing_ok=True)