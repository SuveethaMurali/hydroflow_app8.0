#  HydroFlow — Runoff Estimation Web App

HydroFlow estimates surface runoff using two hydrological methods:
- **SCS Curve Number (CN) Method**
- **Strange’s Method**

It also displays live weather data using the OpenWeatherMap API.

###  Features
- Interactive world map (via Folium)
- Live temperature, humidity, and rainfall
- Method selection and runoff result pages

###  Setup
1. Clone this repo
2. Add your OpenWeatherMap API key in `config.txt`
3. Run:
   ```bash
   pip install -r requirements.txt
   streamlit run Home.py
