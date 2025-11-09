import streamlit as st

st.title("Method Selection")

method = st.radio("Select a method:", ["SCN Method", "Strange's Method"])

if st.button("Continue ➡️"):
    if method == "SCN Method":
        st.session_state.method = "scn"
        st.switch_page("pages/2_SCN_Method.py")
    else:
        st.session_state.method = "strange's"
        st.switch_page("pages/3_Strange's_Method.py")
