from typing import List, Dict, Any, Callable
from core.models import Video


def report_clickbait(videos: List[Video]) -> List[Dict[str, Any]]:
    """
    Filter videos with CTR > 15% and retention_rate < 40%.
    Sort by CTR descending.
    """
    filtered = [
        v for v in videos
        if v.ctr > 15 and v.retention_rate < 40
    ]
    filtered.sort(key=lambda v: v.ctr, reverse=True)

    return [
        {"title": v.title, "ctr": v.ctr, "retention_rate": v.retention_rate}
        for v in filtered
    ]


# Registry of available reports
_REPORT_REGISTRY: Dict[str, Callable[[List[Video]], List[Dict[str, Any]]]] = {
    "clickbait": report_clickbait,
}


def get_report(report_name: str) -> Callable[[List[Video]], List[Dict[str, Any]]]:
    """Return the report function for the given name."""
    if report_name not in _REPORT_REGISTRY:
        available = ", ".join(_REPORT_REGISTRY.keys())
        raise ValueError(f"Unknown report '{report_name}'. Available: {available}")
    return _REPORT_REGISTRY[report_name]