from __future__ import annotations
import os, argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from .utils import load_yaml, now_utc_iso, ensure_dir, log
from .llm_alerts import generate_messages

def fit_model(df: pd.DataFrame, progress: bool) -> tuple[RandomForestClassifier, np.ndarray]:
    X = df.drop(columns=["cell_id", "label"]).values
    y = df["label"].values
    clf = RandomForestClassifier(n_estimators=120, random_state=42, n_jobs=-1)
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    oof = np.zeros(len(df))
    for i, (tr, va) in enumerate(skf.split(X, y), 1):
        clf.fit(X[tr], y[tr])
        oof[va] = clf.predict_proba(X[va])[:,1]
        log(f"  Fold {i}: AUC={roc_auc_score(y[va], oof[va]):.3f}", progress)
    # Refit on full data for inference
    clf.fit(X, y)
    return clf, oof

def main(config: str, demo: bool=False, progress: bool=False):
    cfg = load_yaml(config)
    out_dir = cfg["runtime"]["output_dir"]
    ensure_dir(out_dir)
    ts = cfg["runtime"]["timestamp_utc"] or now_utc_iso()

    # 1) Load features
    df = pd.read_csv(cfg["data"]["features_csv"])
    features = df.drop(columns=["cell_id", "label"])
    log(f"Loaded features: {features.shape[0]} rows × {features.shape[1]} cols", progress)

    # 2) Train model with CV (demo)
    log("Training RandomForest with 3-fold CV...", progress)
    clf, oof = fit_model(df, progress)
    pred = clf.predict_proba(features.values)[:,1]
    risk = pd.DataFrame({"cell_id": df["cell_id"], "risk_score": pred})
    risk.to_csv(os.path.join(out_dir, "risk_map.csv"), index=False)

    # 3) Select alerts
    thr = cfg["alerts"]["threshold"]
    if thr is not None:
        alerts = risk[risk["risk_score"] >= float(thr)].copy()
    else:
        top_n = int(cfg["alerts"]["top_n"])
        alerts = risk.sort_values("risk_score", ascending=False).head(top_n).copy()
    alerts["priority"] = (alerts["risk_score"].rank(ascending=False, method="first")).astype(int)

    # 4) Alert list
    alert_list = alerts.assign(timestamp_utc=ts)[["cell_id", "risk_score", "priority", "timestamp_utc"]]
    alert_list.to_csv(os.path.join(out_dir, "alert_list.csv"), index=False)

    # 5) Messages (templated by default)
    msg_df = generate_messages(alert_list, cfg["alerts"]["languages"], use_llm=bool(cfg["alerts"]["use_llm"]))
    msg_df.to_csv(os.path.join(out_dir, "alert_messages.csv"), index=False)

    log(f"Saved: {out_dir}/risk_map.csv, alert_list.csv, alert_messages.csv", True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--demo", action="store_true")
    p.add_argument("--progress", action="store_true")
    args = p.parse_args()
    main(args.config, demo=args.demo, progress=args.progress)
