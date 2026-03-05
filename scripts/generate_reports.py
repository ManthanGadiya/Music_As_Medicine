import json
from pathlib import Path

from app.services.analytics_service import participant_progress


def generate_participant_report(participant_id: int) -> Path:
    report_data = participant_progress(participant_id)
    output_path = (
        Path(__file__).resolve().parents[1]
        / "reports"
        / "participant_reports"
        / f"participant_{participant_id}_progress.json"
    )
    output_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    generated = generate_participant_report(1)
    print(f"Report generated: {generated}")
