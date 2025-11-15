# Climate Resilience Pipeline (MVP)

An **integrated AI–GIS framework** (minimal viable version) to forecast and visualize **ecosystem service risk** proxies using **RSD/GIS data**, **ML**, and an **NLP news layer**.

## What’s inside
- `data_pipeline.py` — builds features from synthetic climate + NDVI data and produces a simple **NDVI anomaly** target.
- `notebooks/nlp_analysis.ipynb` — minimal topic/sentiment extraction on sample news with region mapping.
- `notebooks/ml_forecast.ipynb` — baseline ML to predict next-day NDVI anomaly per region.
- `notebooks/map_visualization.ipynb` — Folium map with observed vs forecast risk; overlays NLP “events” points.
- `app.py` — Streamlit app to explore time series, predictions, and the NLP layer on a map.
- `configs/aoi_points.csv` — centroids for three regions (synthetic example lives in `data/raw/aoi_points.csv`).

> Replace the **synthetic** CSVs in `data/raw/` with real datasets (Sentinel-2/ERA5 etc.) as you extend.

## Quickstart
```bash
# 1) Create env
python -m venv .venv && source .venv/bin/activate  # (Windows) .venv\Scripts\activate

# 2) Install
pip install -r requirements.txt

# 3) Generate features
python data_pipeline.py

# 4) Explore notebooks
# open notebooks/nlp_analysis.ipynb, ml_forecast.ipynb, map_visualization.ipynb

# 5) Run app
streamlit run app.py
```

## Roadmap to full project
1. Swap synthetic data with real **Sentinel-2 NDVI/EVI**, **ERA5 temp/precip**, and **land cover**.
2. Expand target to drought/heat indices (SPI, SPEI, TX90p).
3. Move from baseline ML to **temporal models** (TFT/LSTM) with spatial features.
4. Improve NLP with **NER geocoding** (spaCy) + sentence-level climate sentiment.
5. Serve COG tiles via `titiler` for faster mapping.

---

**License:** MIT
