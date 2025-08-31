# Data Sheet — Demo Features

## Summary
Synthetic gridded features approximating flood drivers (rainfall accumulation, water indices, elevation, distance to river/roads, population proxy).

## Composition
- 800 rows, columns: cell_id, ndwi, mndwi, rain_3h, rain_6h, rain_24h, elev, slope, river_dist, road_dist, pop_density, critical_facility_dist, label (demo target).

## Collection & Processing
- Programmatically generated (see repository creation script). No field collection; no PII.

## Uses
- Reproducible demonstration of pipeline behavior.

## Maintenance
- Replace with real, licensed datasets in production; update model card accordingly.
