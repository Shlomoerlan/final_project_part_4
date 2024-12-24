import pytest
from pathlib import Path
import os


@pytest.fixture
def csv_files():
    # קבלת הנתיב המוחלט לתיקיית הפרויקט
    current_dir = Path(__file__).parent  # תיקיית tests
    data_dir = current_dir.parent.parent / 'data'  # עולה שתי רמות ונכנס לdata

    return {
        'main': data_dir / 'globalterrorismdb_1000.csv',
        'secondary': data_dir / 'RAND_Database_5000.csv'
    }


@pytest.fixture(autouse=True)
def check_files_exist(csv_files):
    """בודק שהקבצים קיימים לפני הטסטים"""
    missing_files = []
    for name, path in csv_files.items():
        if not path.exists():
            missing_files.append(f"{name}: {path}")

    if missing_files:
        pytest.skip(f"Missing required files:\n" + "\n".join(missing_files))