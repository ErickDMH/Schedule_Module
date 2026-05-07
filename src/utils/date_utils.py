from datetime import datetime
import pytz

def normalize_to_utc(dt: datetime) -> datetime:
    """Normalize datetime to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=pytz.UTC)
    return dt.astimezone(pytz.UTC)

def is_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    """Check if two date ranges overlap."""
    return start1 < end2 and start2 < end1
