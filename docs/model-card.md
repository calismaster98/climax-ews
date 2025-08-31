# Model Card — CLIMAX-EWS no-UXO

**Model**: RandomForestClassifier (scikit-learn)  
**Intended use**: Demo early flood risk scoring on gridded features to produce top-N alerts.  
**Out-of-scope**: Real-time operations without vetted data; UXO/landmine inference; telephony dispatch.

## Data
Synthetic, non-PII demo features (see data sheet).

## Metrics
3-fold CV AUC printed during run; demo only.

## Limitations
- Synthetic data → numbers are illustrative.
- No hydrologic routing or SAR water detection here.
- Templates only for multilingual messages (LLM optional flag present but off).

## Ethical & Safety
- No personal data; generic guidance phrasing; UXO scope excluded.
