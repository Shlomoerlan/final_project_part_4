import pytest

from app.service.csv_processor import CSVProcessor
from app.service.elastic_service import save_events


@pytest.mark.integration
def test_save_events_to_elastic(test_csv_path):
    # בדיקת שמירה לאלסטיק
    events = CSVProcessor.process_main_csv(test_csv_path, limit=2)
    save_events(events)
    # בדיקה שהנתונים נשמרו
    # תלוי באיך בחרת לממש את הבדיקה מול אלסטיק