"""Reproducible process-mining analysis for a restaurant order-fulfillment event log.

The module refactors the original university notebook into testable functions while
preserving the original filtering logic and analytical outputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import pm4py
from pm4py.algo.discovery.temporal_profile import algorithm as temporal_profile_discovery


REQUIRED_COLUMNS = {"case_id", "activity", "time:timestamp"}
DEFAULT_COMPLETION_ACTIVITY = "Order_is_served"


def validate_columns(log: pd.DataFrame) -> None:
    """Raise a clear error if required event-log columns are missing."""
    missing = REQUIRED_COLUMNS.difference(log.columns)
    if missing:
        raise ValueError(
            "Event log is missing required column(s): " + ", ".join(sorted(missing))
        )


def load_event_log(path: Path) -> pd.DataFrame:
    """Load an XES log and normalize its timestamp and case-id fields."""
    if not path.exists():
        raise FileNotFoundError(
            f"Event log not found: {path}. Place the XES file at this path "
            "or pass a different path with --input."
        )

    log = pm4py.read_xes(str(path))
    validate_columns(log)

    log = log.copy()
    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"])
    log["case_id"] = log["case_id"].astype(str)
    return log


def summarize_log(log: pd.DataFrame) -> Dict[str, object]:
    """Return basic event-log statistics in a serializable dictionary."""
    validate_columns(log)
    summary = {
        "events": int(len(log)),
        "cases": int(log["case_id"].nunique()),
        "activities": int(log["activity"].nunique()),
        "start_timestamp": str(log["time:timestamp"].min()),
        "end_timestamp": str(log["time:timestamp"].max()),
    }
    if "resource" in log.columns:
        summary["resources"] = int(log["resource"].nunique())
    return summary


def filter_year_and_completed(
    log: pd.DataFrame,
    year: int,
    completion_activity: str = DEFAULT_COMPLETION_ACTIVITY,
) -> pd.DataFrame:
    """Filter to one year and retain only cases that reach the completion activity."""
    validate_columns(log)

    working = log.copy()
    working["time:timestamp"] = pd.to_datetime(working["time:timestamp"])
    working["case_id"] = working["case_id"].astype(str)

    year_log = working[working["time:timestamp"].dt.year == year].copy()
    completed_cases = year_log.loc[
        year_log["activity"] == completion_activity, "case_id"
    ].unique()

    completed = year_log[year_log["case_id"].isin(completed_cases)].copy()
    completed["case_id"] = completed["case_id"].astype(str)
    return completed


def to_pm4py_event_log(filtered: pd.DataFrame):
    """Convert the filtered DataFrame to PM4Py's event-log representation."""
    return pm4py.convert_to_event_log(
        filtered,
        case_id_key="case_id",
        activity_key="activity",
        timestamp_key="time:timestamp",
    )


def discover_models(event_log, figures_dir: Path) -> Dict[str, object]:
    """Discover process models and save their visualizations."""
    figures_dir.mkdir(parents=True, exist_ok=True)

    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    pm4py.save_vis_petri_net(
        net,
        initial_marking,
        final_marking,
        str(figures_dir / "petri_net.png"),
    )

    bpmn_model = pm4py.discover_bpmn_inductive(event_log)
    pm4py.save_vis_bpmn(bpmn_model, str(figures_dir / "bpmn_model.png"))

    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
    pm4py.save_vis_dfg(
        dfg,
        start_activities,
        end_activities,
        str(figures_dir / "dfg_frequency.png"),
    )

    performance_dfg, perf_start, perf_end = pm4py.discover_performance_dfg(event_log)
    pm4py.save_vis_performance_dfg(
        performance_dfg,
        perf_start,
        perf_end,
        str(figures_dir / "dfg_performance.png"),
    )

    return {
        "petri_net": net,
        "initial_marking": initial_marking,
        "final_marking": final_marking,
        "bpmn": bpmn_model,
        "dfg": dfg,
        "performance_dfg": performance_dfg,
        "start_activities": start_activities,
        "end_activities": end_activities,
    }


def build_temporal_profile(event_log) -> pd.DataFrame:
    """Calculate mean and standard deviation between activity pairs."""
    temporal_profile = temporal_profile_discovery.apply(event_log)

    rows = []
    for (source, target), (mean_seconds, std_seconds) in temporal_profile.items():
        rows.append(
            {
                "from_activity": source,
                "to_activity": target,
                "mean_seconds": float(mean_seconds),
                "std_seconds": float(std_seconds),
                "mean_hours": round(float(mean_seconds) / 3600, 2),
                "std_hours": round(float(std_seconds) / 3600, 2),
            }
        )

    return pd.DataFrame(rows).sort_values("mean_hours", ascending=False)


def direct_transition_table(performance_dfg: Dict[Tuple[str, str], float]) -> pd.DataFrame:
    """Convert the performance DFG into a sortable direct-transition table."""
    rows = [
        {
            "from_activity": source,
            "to_activity": target,
            "mean_seconds": float(seconds),
            "mean_hours": round(float(seconds) / 3600, 2),
        }
        for (source, target), seconds in performance_dfg.items()
    ]
    return pd.DataFrame(rows).sort_values("mean_hours", ascending=False)


def case_duration_summary(filtered: pd.DataFrame) -> Dict[str, float]:
    """Calculate end-to-end case-duration statistics in hours."""
    durations = filtered.groupby("case_id")["time:timestamp"].agg(["min", "max"])
    hours = (durations["max"] - durations["min"]).dt.total_seconds() / 3600
    return {
        "mean_case_duration_hours": round(float(hours.mean()), 2),
        "min_case_duration_hours": round(float(hours.min()), 2),
        "max_case_duration_hours": round(float(hours.max()), 2),
    }


def run_analysis(
    input_path: Path,
    year: int,
    completion_activity: str,
    output_dir: Path,
    figures_dir: Path,
) -> Dict[str, object]:
    """Run the full analysis and save structured outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)

    log = load_event_log(input_path)
    full_summary = summarize_log(log)

    filtered = filter_year_and_completed(log, year, completion_activity)
    filtered_summary = summarize_log(filtered)
    duration_summary = case_duration_summary(filtered)

    event_log = to_pm4py_event_log(filtered)
    models = discover_models(event_log, figures_dir)

    temporal_df = build_temporal_profile(event_log)
    temporal_df.to_csv(output_dir / "temporal_profile.csv", index=False)

    direct_df = direct_transition_table(models["performance_dfg"])
    direct_df.to_csv(output_dir / "direct_transition_performance.csv", index=False)

    summary = {
        "analysis_year": year,
        "completion_activity": completion_activity,
        "full_log": full_summary,
        "filtered_completed_log": filtered_summary,
        **duration_summary,
    }

    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process-mine a restaurant order-fulfillment XES event log."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/event_log.xes"),
        help="Path to the XES event log.",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2030,
        help="Calendar year to analyze.",
    )
    parser.add_argument(
        "--completion-activity",
        default=DEFAULT_COMPLETION_ACTIVITY,
        help="Activity used to identify completed cases.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory for CSV/JSON outputs.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("figures"),
        help="Directory for process-model images.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_analysis(
        input_path=args.input,
        year=args.year,
        completion_activity=args.completion_activity,
        output_dir=args.output_dir,
        figures_dir=args.figures_dir,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
