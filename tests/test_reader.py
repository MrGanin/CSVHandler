import pytest
import tempfile
from pathlib import Path
from core.reader import load_videos_from_files



def test_load_single_valid_file():
    content = """title,ctr,retention_rate,views,likes,avg_watch_time
Test Video,15.5,45,1000,50,5.2
Another,22.0,30,2000,100,3.0
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp_path = f.name

    try:
        videos = load_videos_from_files([tmp_path])
        assert len(videos) == 2
        assert videos[0].title == "Test Video"
        assert videos[0].ctr == 15.5
        assert videos[1].title == "Another"
    finally:
        Path(tmp_path).unlink()


def test_load_multiple_files():
    content1 = "title,ctr,retention_rate,views,likes,avg_watch_time\nVideo1,10.0,50,100,10,5.0"
    content2 = "title,ctr,retention_rate,views,likes,avg_watch_time\nVideo2,20.0,40,200,20,6.0"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f1:
        f1.write(content1)
        path1 = f1.name

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f2:
        f2.write(content2)
        path2 = f2.name

    try:
        videos = load_videos_from_files([path1, path2])
        assert len(videos) == 2
        titles = {v.title for v in videos}
        assert titles == {"Video1", "Video2"}
    finally:
        Path(path1).unlink()
        Path(path2).unlink()


def test_file_not_found():
    with pytest.raises(FileNotFoundError, match="File not found: nonexistent.csv"):
        load_videos_from_files(["nonexistent.csv"])


def test_missing_columns():
    content = "title,ctr,views\nTest,10.0,100"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp_path = f.name

    try:
        with pytest.raises(ValueError, match="missing required columns"):
            load_videos_from_files([tmp_path])
    finally:
        Path(tmp_path).unlink()


def test_invalid_data_type():
    content = """title,ctr,retention_rate,views,likes,avg_watch_time
Bad Video,invalid,30,100,10,5.0
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp_path = f.name

    try:
        with pytest.raises(ValueError, match="Invalid data"):
            load_videos_from_files([tmp_path])
    finally:
        Path(tmp_path).unlink()