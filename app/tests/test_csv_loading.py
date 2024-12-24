import pytest
from pathlib import Path

from app.service.csv_processor import process_main_csv, process_secondary_csv


@pytest.fixture
def csv_files():
    return {
        'main': Path('../data/globalterrorismdb_1000.csv'),
        'secondary': Path('../data/RAND_Database_5000.csv'),
    }

def test_event_creation_from_main_csv(csv_files):
    events = process_main_csv(csv_files['main'], limit=2)
    assert len(events) > 0
    event = events[0]
    assert event.title
    assert event.location
    assert event.coordinates

def test_event_creation_from_secondary_csv(csv_files):
    events = process_secondary_csv(csv_files['secondary'], limit=2)
    assert len(events) > 0
    event = events[0]
    assert event.title
    assert event.location