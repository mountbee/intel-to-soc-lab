"""Auth log parser and helper aggregations."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {"timestamp", "user", "src_ip", "status", "user_agent"}


def load_auth_logs(path: str) -> pd.DataFrame:
    """Load auth logs CSV into a DataFrame with normalized fields."""
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df["user"] = df["user"].astype(str).str.strip()
    df["src_ip"] = df["src_ip"].astype(str).str.strip()
    df["user_agent"] = df["user_agent"].astype(str).str.strip()
    df["status"] = df["status"].astype(str).str.strip().str.lower()
    validate_schema(df)
    return df


def validate_schema(df: pd.DataFrame) -> None:
    """Validate required columns and status values."""
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    invalid_status = sorted(set(df.loc[~df["status"].isin(["success", "fail"]), "status"]))
    if invalid_status:
        raise ValueError(f"Invalid status values: {', '.join(map(str, invalid_status))}")


def add_time_window(df: pd.DataFrame, window_minutes: int) -> pd.DataFrame:
    """Add window_start column floored to a given minute window."""
    result = df.copy()
    result["window_start"] = result["timestamp"].dt.floor(f"{window_minutes}min")
    return result


def ip_user_stats(df: pd.DataFrame, window_minutes: int) -> pd.DataFrame:
    """Aggregate per (src_ip, window_start): unique users, attempts, fails, successes."""
    dfw = add_time_window(df, window_minutes)
    agg = dfw.groupby(["src_ip", "window_start"]).agg(
        unique_users=("user", "nunique"),
        attempts=("status", "count"),
        fails=("status", lambda s: (s == "fail").sum()),
        successes=("status", lambda s: (s == "success").sum()),
    )
    return agg.reset_index()


def user_ip_stats(df: pd.DataFrame, window_minutes: int) -> pd.DataFrame:
    """Aggregate per (user, window_start): unique IPs, attempts, fails, successes."""
    dfw = add_time_window(df, window_minutes)
    agg = dfw.groupby(["user", "window_start"]).agg(
        unique_ips=("src_ip", "nunique"),
        attempts=("status", "count"),
        fails=("status", lambda s: (s == "fail").sum()),
        successes=("status", lambda s: (s == "success").sum()),
    )
    return agg.reset_index()
