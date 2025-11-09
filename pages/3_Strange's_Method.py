import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("Strange's Method Calculation")

rain_intensity = st.number_input("Enter Rain Intensity (mm/hr):", min_value=0.0)
area = st.number_input("Enter Catchment Area (km²):", min_value=0.0)

if st.button("Calculate Runoff"):
    runoff = rain_intensity * area * 0.278  # example formula
    st.session_state.result = runoff
    st.switch_page("pages/4_Runoff_Result.py")
