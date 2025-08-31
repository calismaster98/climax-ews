from __future__ import annotations
import os
from typing import List
import pandas as pd

# Optional LLM import (not required)
try:
    import openai  # type: ignore
    _OPENAI_OK = True
except Exception:
    _OPENAI_OK = False

def _templated(msg_rows: pd.DataFrame, languages: List[str]) -> pd.DataFrame:
    out = []
    for _, r in msg_rows.iterrows():
        base = {
            "cell_id": r["cell_id"],
            "risk_score": round(float(r["risk_score"]), 4),
            "priority": int(r["priority"]),
        }
        if "EN" in languages:
            base["message_en"] = (
                f"[Flood Warning] Cell {r['cell_id']} is at HIGH risk. "
                f"Risk score={r['risk_score']:.2f}. "
                f"If safe, move to higher ground and avoid rivers/bridges. "
                f"Assist children, older adults, and people with disabilities."
            )
        if "KM" in languages:
            # Note: placeholder Khmer string (template). Replace with verified translation in production.
            base["message_km"] = (
                f"[ព្រមានទឹកជំនន់] ក្រឡា {r['cell_id']} មានហានិភ័យខ្ពស់។ "
                f"ពិន្ទុហានិភ័យ={r['risk_score']:.2f}។ "
                "សូមផ្លាស់ទីទៅកន្លែងខ្ពស់ ប្រសិនបើមានសុវត្ថិភាព និងជៀសវាងអគារព្រំស្ទឹង "
                "ជួយកុមារ មនុស្សចំណាស់ និងមនុស្សពិការ។"
            )
        out.append(base)
    return pd.DataFrame(out)

def generate_messages(msg_rows: pd.DataFrame, languages: List[str], use_llm: bool=False) -> pd.DataFrame:
    # For this submission, LLM usage is optional and disabled by default.
    # This function always falls back to the templated messages to keep the demo self-contained.
    return _templated(msg_rows, languages)
