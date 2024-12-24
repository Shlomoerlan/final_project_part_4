import pytest
from app.db.models import TerrorEvent
from app.service.csv_processor import CSVProcessor


def test_process_main_csv_returns_correct_events(test_csv_path):
    events = CSVProcessor.process_main_csv(test_csv_path, limit=10)
    assert len(events) > 0
    assert all(isinstance(event, TerrorEvent) for event in events)


def test_terror_event_has_required_fields(test_csv_path):
    events = CSVProcessor.process_main_csv(test_csv_path, limit=1)
    event = events[0]

    assert event.title
    assert event.content
    assert event.publication_date
    assert event.category == "historic_terror"
    assert event.location
    assert event.confidence == 1.0
    assert event.source_url


def test_coordinates_extraction(test_csv_path):
    events = CSVProcessor.process_main_csv(test_csv_path, limit=1)
    event = events[0]

    if event.coordinates:
        assert hasattr(event.coordinates, 'lat')
        assert hasattr(event.coordinates, 'lon')
        assert isinstance(event.coordinates.lat, float)
        assert isinstance(event.coordinates.lon, float)