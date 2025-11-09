import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime
from pathlib import Path

# ---------------- Page Configuration ----------------
st.set_page_config(page_title="Runmeter — Runoff Estimation", page_icon="🌧️", layout="wide")

# ---------------- Helpers ----------------
@st.cache_data(ttl=300)
def get_weather(lat: float, lon: float, api_key: str, units: str = "metric"):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    rain_1h = data.get("rain", {}).get("1h", None)
    weather_main = (data.get("weather") or [{}])[0].get("main", "")
    emoji = {"Rain": "🌧️", "Clouds": "☁️", "Clear": "☀️"}.get(weather_main, "🌍")
    return {
        "temp": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "wind": data.get("wind", {}).get("speed"),
        "rain": rain_1h,
        "emoji": emoji,
        "desc": (data.get("weather") or [{}])[0].get("description", "").title(),
        "dt": data.get("dt"),
    }

def read_key_from_config():
    try:
        p = Path("config.txt")
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip().startswith("OPENWEATHER_API_KEY"):
                    return line.split("=", 1)[1].strip()
    except Exception:
        pass
    try:
        return st.secrets["openweather"]["api_key"]
    except Exception:
        return None

# Read API key
OWM_KEY = read_key_from_config()



# ---------------- Layout ----------------
col1, col2 = st.columns([1, 2], gap="large")

# Default location: Chennai, India
chennai_lat, chennai_lon = 13.0827, 80.2707

# ----------- Left Column: Map -------------
with col1:
    st.markdown("### 🌍 Location: Chennai, India")
    world_map = folium.Map(location=[chennai_lat, chennai_lon], zoom_start=10)
    folium.Marker([chennai_lat, chennai_lon], popup="Chennai").add_to(world_map)
    st_folium(world_map, width=420, height=420)

# ----------- Right Column: App Info + Weather -------------
with col2:
    st.title("🌧️ Runmeter — Runoff Estimation App")
    st.write("Choose your method to estimate surface runoff using SCS CN or Strange’s Method.")
    st.markdown("---")

    st.subheader("💡 About Runmeter")
    st.write(
        """
        **Runmeter** estimates surface runoff using:
        - **SCS Curve Number (CN) Method**
        - **Strange’s Method**
        """
    )

    st.markdown("---")
    st.subheader("🌦️ Live Weather in Chennai")

    if not OWM_KEY:
        st.error("OpenWeatherMap API key not found. Add it in `config.txt` as `OPENWEATHER_API_KEY=YOUR_KEY` or set Streamlit secrets.")
    else:
        try:
            wx = get_weather(chennai_lat, chennai_lon, OWM_KEY, units="metric")
            last_updated = datetime.utcfromtimestamp(wx["dt"]).strftime("%Y-%m-%d %H:%M UTC") if wx.get("dt") else "—"
            colA, colB, colC = st.columns(3)
            with colA:
                st.metric(
                    label=f"Temperature {wx['emoji']}",
                    value=f"{wx['temp']:.1f}°C" if wx['temp'] is not None else "—",
                    delta=f"Feels {wx['feels_like']:.1f}°C" if wx['feels_like'] is not None else ""
                )

            with colB:
                st.metric(label="Humidity", value=f"{wx['humidity']}%" if wx['humidity'] is not None else "—")

            with colC:
                st.metric(label="Rain (1h)", value=f"{wx['rain'] or 0} mm")

            st.caption(f"{wx['desc']} · Updated: {last_updated}")
            if refresh:
                st.cache_data.clear()
                st.rerun()
        except Exception:
            st.warning("⚠️ Unable to fetch live weather right now. Please try again later.")

    st.markdown("---")
    if st.button("Proceed to Method Selection ➡️"):
        st.switch_page("pages/1_Method_Selection.py")


