import pandas as pd
from pathlib import Path

RAW = Path('data/raw')
PROC = Path('data/processed')
PROC.mkdir(parents=True, exist_ok=True)

def build_features():
    df = pd.read_csv(RAW / 'synthetic_climate_ndvi.csv', parse_dates=['date'])
    # Aggregate to daily-region and compute a rolling mean for NDVI
    df = df.sort_values(['region','date'])
    df['ndvi_roll7'] = df.groupby('region')['ndvi'].transform(lambda s: s.rolling(7, min_periods=3).mean())
    df['ndvi_anom'] = df['ndvi'] - df['ndvi_roll7']  # simple anomaly proxy
    # Lag features
    for lag in [1,3,7]:
        df[f'temp_lag{lag}'] = df.groupby('region')['temp_c'].shift(lag)
        df[f'precip_lag{lag}'] = df.groupby('region')['precip_mm'].shift(lag)
        df[f'ndvi_lag{lag}'] = df.groupby('region')['ndvi'].shift(lag)
    # Drop early NaNs
    feat = df.dropna().reset_index(drop=True)
    feat.to_csv(PROC / 'features.csv', index=False)
    print(f'[OK] wrote {PROC / "features.csv"} with {len(feat)} rows.')

if __name__ == '__main__':
    build_features()
