from sqlite3 import Row
from typing import Any, Dict


def feedback_row_to_dict(row: Row) -> Dict[str, Any]:
    return dict(row)
