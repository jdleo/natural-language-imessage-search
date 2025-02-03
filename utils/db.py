import sqlite3
from os import path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


def get_db_connection() -> sqlite3.Connection:
    """Get connection to iMessage database"""
    db_path = path.expanduser("~/Library/Messages/chat.db")
    # Add read-only flag to prevent accidental writes
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def execute_query(query: str) -> Optional[Tuple[List[str], List[List[str]]]]:
    """
    Execute SQL query and return results formatted for Gradio Dataframe
    Returns: (headers, rows) or None on error
    """
    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(query)
        # Get column names for headers
        headers = [description[0] for description in cursor.description]
        rows = []

        for row in cursor.fetchall():
            # Convert row to list and handle timestamp conversion
            row_data = []
            for i, value in enumerate(row):
                if isinstance(value, int) and "date" in headers[i].lower():
                    # Convert Apple's timestamp to readable date
                    mac_epoch = datetime(2001, 1, 1)
                    timestamp = mac_epoch.timestamp() + value / 1e9
                    formatted_value = datetime.fromtimestamp(timestamp).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                else:
                    formatted_value = str(value) if value is not None else ""
                row_data.append(formatted_value)
            rows.append(row_data)

        return headers, rows
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
