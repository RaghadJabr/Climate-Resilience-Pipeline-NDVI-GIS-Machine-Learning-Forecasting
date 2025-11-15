import streamlit as st
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='Climate Resilience Pipeline', layout='wide')

st.title('🌍 Climate Resilience Forecast (MVP)')

features_path = 'data/processed/features.csv'
news_path = 'data/raw/news_sample.csv'

@st.cache_data
def load_data():
    feat = pd.read_csv(features_path, parse_dates=['date'])
    news = pd.read_csv(news_path, parse_dates=['date'])
    return feat, news

feat, news = load_data()
regions = sorted(feat['region'].unique().tolist())
region = st.sidebar.selectbox('Region', regions, index=0)


min_d = feat['date'].min().to_pydatetime()
max_d = feat['date'].max().to_pydatetime()

date_sel = st.sidebar.slider(
    'Date',
    min_value=min_d,
    max_value=max_d,
    value=max_d,
)


st.subheader(f'Region: {region} — {date_sel.date()}')
df_r = feat[(feat['region']==region) & (feat['date']<=date_sel)].sort_values('date')

c1, c2 = st.columns(2)
with c1:
    st.line_chart(df_r.set_index('date')[['ndvi','ndvi_roll7']])
with c2:
    st.line_chart(df_r.set_index('date')[['temp_c','precip_mm']])

st.markdown('---')
st.subheader('🗺️ Map regions')

m = folium.Map(location=[31.95, 35.9], zoom_start=7)

latest = feat.sort_values('date').groupby('region').tail(1)
for _, row in latest.iterrows():
    risk = row['ndvi_anom']
    popup = f"""<b>{row['region']}</b><br>
    NDVI anomaly: {risk:.3f}<br>
    Temp: {row['temp_c']:.1f}°C — Precip: {row['precip_mm']:.1f} mm"""
    folium.CircleMarker(location=[row['lat'], row['lon']], radius=10,
                        tooltip=row['region'], popup=popup).add_to(m)

for _, r in news.iterrows():
    loc = latest[latest['region']==r['region']]
    if len(loc):
        lat, lon = loc.iloc[0][['lat','lon']]
        folium.Marker([lat, lon], icon=folium.Icon(icon='info-sign'),
                      tooltip=f"{r['region']} — {r['date'].date()}",
                      popup=r['text']).add_to(m)

st_folium(m, width=1100, height=500)
