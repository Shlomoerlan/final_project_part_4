from typing import List
from datetime import datetime
import pandas as pd
from app.db.models import DataSource, TerrorEvent
from app.service.location_service import get_coordinates
from app.service.terror_event_service import create_terror_event
from app.utills.process_utils import _parse_date, _extract_coordinates, _create_content, _clean_text


def process_main_csv(filepath: str, limit: int = None) -> List[TerrorEvent]:
    df = pd.read_csv(filepath, encoding='iso-8859-1')
    if limit:
        df = df.head(limit)
    events = []
    for _, row in df.iterrows():
        try:
            date = _parse_date(row['iyear'], row['imonth'], row['iday'])
            if not date:
                continue

            coordinates = _extract_coordinates(row)
            location = f"{row['city']}, {row['country_txt']}"

            event = create_terror_event(
                title=f"Terror Attack in {location}",
                content=_create_content(row),
                date=date,
                location=location,
                coordinates=coordinates,
                source=DataSource.MAIN_CSV
            )
            events.append(event)
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    return events

def process_secondary_csv(filepath: str, limit: int = None) -> List[TerrorEvent]:
    df = pd.read_csv(filepath, encoding='iso-8859-1')
    if limit:
        df = df.head(limit)
    events = []

    for _, row in df.iterrows():
        try:
            date = datetime.strptime(row['Date'], '%d-%b-%y')
            location = f"{row['City']}, {row['Country']}"
            coordinates = get_coordinates(row['City'], row['Country'])

            event = create_terror_event(
                title=f"Terror Attack in {location}",
                content=_clean_text(row['Description']),
                date=date,
                location=location,
                coordinates=coordinates,
                source=DataSource.SECONDARY_CSV
            )
            events.append(event)
        except Exception as e:
            print(f"Error processing row from secondary CSV: {e}")
            continue
    return events

