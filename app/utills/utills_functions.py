from app.service.csv_processor import process_main_csv, process_secondary_csv
from app.service.elastic_service import save_events_for_terror


def import_historic_data(main_csv_path: str, secondary_csv_path: str) -> None:
    print("Processing main CSV file...")
    main_events = process_main_csv(main_csv_path)
    save_events_for_terror(main_events)
    print(f"Saved {len(main_events)} events from main CSV")

    print("Processing secondary CSV file...")
    secondary_events = process_secondary_csv(secondary_csv_path)
    save_events_for_terror(secondary_events)
    print(f"Saved {len(secondary_events)} events from secondary CSV")

