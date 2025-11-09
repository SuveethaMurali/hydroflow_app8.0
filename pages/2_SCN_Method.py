import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("SCS CN Method Calculation")

rainfall = st.number_input("Enter Rainfall (mm):", min_value=0.0)
curve_number = st.number_input("Enter Curve Number (CN):", min_value=0.0, max_value=100.0)

if st.button("Calculate Runoff"):
    # Example SCS CN formula
    runoff = (rainfall - 0.2 * curve_number) ** 2 / (rainfall + 0.8 * curve_number)
    st.session_state.result = runoff
    st.switch_page("pages/4_Runoff_Result.py")
