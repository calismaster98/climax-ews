from __future__ import annotations
import os, sys, time, yaml, json, datetime as dt
from typing import Any, Dict

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def now_utc_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def ensure_dir(d: str) -> None:
    os.makedirs(d, exist_ok=True)

def log(msg: str, enabled: bool=True) -> None:
    if enabled:
        print(msg, flush=True)
