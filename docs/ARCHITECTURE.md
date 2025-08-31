# Architecture

![pipeline](../assets/pipeline.png)

1) Load features (CSV)  
2) Train RF (demo CV) → probability per cell  
3) Select top-N or threshold τ  
4) Write risk_map.csv, alert_list.csv, alert_messages.csv (templated EN/KM)
