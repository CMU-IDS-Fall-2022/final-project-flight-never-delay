import streamlit as st
import altair as alt
import pandas as pd
from constants import delay_category

def intro():
    st.header("Introduction")
    st.write("Cancel rate: 9.38 %")
    st.write("Average delay time: 66.63 minutes")
    df = pd.DataFrame(
        {"reasons of delay": list(delay_category.keys()), "value": list(delay_category.values())}
    )
    pie_chart = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="reasons of delay", type="nominal"),
    )
    st.altair_chart(pie_chart)
