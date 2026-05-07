import pytest
from core.models import Video
from core.reports import report_clickbait, get_report


def test_clickbait_filtering():
    videos = [
        Video("Video1", 18.0, 35, 100, 10, 5.0),   # Matches: CTR>15, retention<40
        Video("Video2", 22.0, 30, 200, 20, 4.0),   # Matches
        Video("Video3", 16.0, 45, 150, 15, 4.5),   # No: retention too high
        Video("Video4", 14.0, 38, 120, 12, 5.5),   # No: CTR too low
        Video("Video5", 20.0, 50, 180, 18, 3.5),   # No: retention too high
    ]

    result = report_clickbait(videos)

    assert len(result) == 2
    assert result[0]["title"] == "Video2"  # Highest CTR first
    assert result[0]["ctr"] == 22.0
    assert result[1]["title"] == "Video1"
    assert result[1]["ctr"] == 18.0


def test_clickbait_empty_result():
    videos = [
        Video("Video1", 10.0, 60, 100, 10, 5.0),
        Video("Video2", 12.0, 55, 200, 20, 4.0),
    ]
    result = report_clickbait(videos)
    assert result == []


def test_clickbait_sorts_by_ctr_descending():
    videos = [
        Video("Low", 16.0, 35, 100, 10, 5.0),
        Video("High", 30.0, 20, 100, 10, 5.0),
        Video("Medium", 22.0, 25, 100, 10, 5.0),
    ]
    result = report_clickbait(videos)
    titles = [r["title"] for r in result]
    assert titles == ["High", "Medium", "Low"]


def test_get_report_known():
    func = get_report("clickbait")
    assert func == report_clickbait


def test_get_report_unknown():
    with pytest.raises(ValueError, match="Unknown report 'fake'"):
        get_report("fake")