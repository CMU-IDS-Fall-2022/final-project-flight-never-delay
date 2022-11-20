import streamlit as st
import gdown
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

@st.cache
def get_data(filename):
    url = "https://drive.google.com/uc?id=1-4OXefZDioyrobHyhtBfAFMNMem_XmLp"
    output = filename
    gdown.download(url, output, quiet=False)

@st.cache
def profiler(filename):
    df = pd.read_csv(filename)
    pr = df.profile_report()
    st_profile_report(pr)

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

if __name__ == '__main__':
    filename = "data-coordinates.csv"
    get_data(filename)
    intro()
    
    # nav = st.sidebar.radio("Navigation",
    #                  ("Introduction", "Visualization", "Prediction"))
    # if nav == "Introduction":
    #     intro()
    # elif nav == "Visualization":
    #     vis()
    # else:
    #     pred()

    # profiler(filename)
