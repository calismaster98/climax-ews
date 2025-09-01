# CLIMAX-EWS (submission no-UXO)

Early flood Early Warning System (EWS) **without UXO/landmine scope** for DPG submission demo.
![Uploading pipeline_readme.png…]()


## Quick start (Colab)
```bash
%cd /content
!unzip -q climax-ews-1.1.2-submission-no-uxo.zip -d /content
%cd /content/climax-ews-1.1.2-submission-no-uxo
!pip -q install -e .
!python -m climax_ews.run_pipeline --config configs/config.yaml --demo --progress
# Outputs: alerts/alert_list.csv, alerts/alert_messages.csv, alerts/risk_map.csv
```
- LLM is **off** by default. If you enable it in config, template fallback is used unless a key is present.

## What’s inside
- `src/climax_ews`: pipeline code (RandomForest risk model → top-N alerts → EN/KM templated messages)
- `configs/config.yaml`: all knobs (no telephony/SMS integration)
- `data/demo_features.csv`: synthetic demo features (for reproducibility)
- `docs/`: DPG docs (checklist, model card, data sheet, risk, privacy, standards, ownership, architecture, roadmap)
- `LICENSE`: Apache-2.0
- `CITATION.cff`: how to cite

## No-UXO decision
The UXO/landmine stream is **excluded** from this submission to avoid safety/accuracy risks. See `docs/ROADMAP.md` for a staged plan to add it later with proper governance and validation.
