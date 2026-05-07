from dataclasses import dataclass


@dataclass
class Video:
    """Represents a single video with its metrics."""
    title: str
    ctr: float          # Click-through rate (%)
    retention_rate: float  # Average retention (%)
    views: int
    likes: int
    avg_watch_time: float

    @classmethod
    def from_csv_row(cls, row: dict) -> "Video":
        """Create a Video instance from a CSV row dictionary."""
        return cls(
            title=row["title"],
            ctr=float(row["ctr"]),
            retention_rate=float(row["retention_rate"]),
            views=int(row["views"]),
            likes=int(row["likes"]),
            avg_watch_time=float(row["avg_watch_time"]),
        )