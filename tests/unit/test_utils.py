import pytest
from datetime import datetime
from src.utils.date_utils import is_overlap

def test_is_overlap():
    start1 = datetime(2023, 1, 1, 10, 0)
    end1 = datetime(2023, 1, 1, 12, 0)
    
    start2 = datetime(2023, 1, 1, 11, 0)
    end2 = datetime(2023, 1, 1, 13, 0)
    
    assert is_overlap(start1, end1, start2, end2) == True

def test_no_overlap():
    start1 = datetime(2023, 1, 1, 10, 0)
    end1 = datetime(2023, 1, 1, 12, 0)
    
    start2 = datetime(2023, 1, 1, 13, 0)
    end2 = datetime(2023, 1, 1, 14, 0)
    
    assert is_overlap(start1, end1, start2, end2) == False
