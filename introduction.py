import streamlit as st
import altair as alt
import pandas as pd

constants = {
    "carrier_delay": 26.715905850648916,
    "weather_delay": 4.561987648962998,
    "nas_delay": 11.274788825104947,
    "security_delay": 0.21346667066188915,
    "late_aircraft_delay": 23.864074798297647
}

def intro():
    st.header("Introduction")
    st.write("Cancel rate: 9.38 %")
    st.write("Average delay time: 66.63 minutes")
    df = pd.DataFrame(
        {"reasons of delay": list(constants.keys()), "value": list(constants.values())}
    )
    pie_chart = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="reasons of delay", type="nominal"),
    )
    st.altair_chart(pie_chart)
