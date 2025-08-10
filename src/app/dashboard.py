import streamlit as st
import requests
import pandas as pd

API="http://localhost:8080"

st.title("Real-Time Vehicle Tracking — Dashboard (In Progress)")

col1,col2=st.columns(2)
with col1:
    st.subheader("Latest Events")
    resp = requests.get(f"{API}/latest?n=25").json()
    st.dataframe(pd.DataFrame(resp))
with col2:
    st.subheader("Hourly Aggregates")
    agg = requests.get(f"{API}/agg/hour?n=48").json()
    df = pd.DataFrame(agg)
    if not df.empty:
        st.bar_chart(df.set_index("hour")[["count","speeding"]])
