import pandas as pd
import pytest

from process_mining_analysis import filter_year_and_completed, validate_columns


def synthetic_log():
    return pd.DataFrame(
        [
            {"case_id": "1", "activity": "Order_arrives", "time:timestamp": "2030-01-01 10:00:00"},
            {"case_id": "1", "activity": "Order_is_served", "time:timestamp": "2030-01-01 11:00:00"},
            {"case_id": "2", "activity": "Order_arrives", "time:timestamp": "2030-01-02 10:00:00"},
            {"case_id": "2", "activity": "Order_is_rejected", "time:timestamp": "2030-01-02 10:05:00"},
            {"case_id": "3", "activity": "Order_arrives", "time:timestamp": "2029-01-01 10:00:00"},
            {"case_id": "3", "activity": "Order_is_served", "time:timestamp": "2029-01-01 11:00:00"},
        ]
    )


def test_filter_keeps_only_completed_cases_in_selected_year():
    result = filter_year_and_completed(synthetic_log(), year=2030)
    assert set(result["case_id"]) == {"1"}
    assert len(result) == 2


def test_filter_accepts_custom_completion_activity():
    log = synthetic_log().copy()
    result = filter_year_and_completed(
        log,
        year=2030,
        completion_activity="Order_is_rejected",
    )
    assert set(result["case_id"]) == {"2"}


def test_validate_columns_reports_missing_fields():
    bad = pd.DataFrame({"case_id": ["1"]})
    with pytest.raises(ValueError, match="missing required column"):
        validate_columns(bad)
