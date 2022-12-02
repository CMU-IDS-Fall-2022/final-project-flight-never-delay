import streamlit as st
import altair as alt
from constants import delay_category
import gdown
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.switch_page_button import switch_page

@st.cache(suppress_st_warning=True)
def get_data(filename):
    url = "https://drive.google.com/uc?id=1-4OXefZDioyrobHyhtBfAFMNMem_XmLp"
    output = filename
    gdown.download(url, output, quiet=False)

@st.cache(suppress_st_warning=True)
def profiler(df):
    pr = df.profile_report()
    st_profile_report(pr)

def intro():
    st.header("Project Flight Never Delay ✈️")
    st.markdown("As frequent travelers, our team members often experience flight delays and cancellations.\
        However, there is no good way for us to be informed on whether a flight will be delayed or cancelled in advance.")

    st.markdown("To address our problem, we built a flight delay and cancellation prediction model using previous \
        flight delay data from the [Bureau of Transportation Statistics - On-Time : Marketing Carrier On-Time Performance dataset](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr). \
        We further augmented our dataset with fine-grained geographic information by mapping airports to US state \
        names and coordinates (latitude and longitude) from a [Kaggle dataset](https://www.kaggle.com/datasets/usdot/flight-delays?select=airports.csv).")
    
    st.markdown("After data cleaning, we have a dataset of 1,141,693 flight delays from 2021 covering information such as flight time, \
        flight carrier, flight origin and destinations, flight delay times and reasons, flight cancellations and reasons, and geographical information. You may view \
        the full dataset at the bottom of the page.")
    
    # st.write("Cancel rate: 9.38 %")
    # st.write("Average delay time: 66.63 minutes")
    # df = pd.DataFrame(
    #     {"reasons of delay": list(delay_category.keys()), "value": list(delay_category.values())}
    # )
    # pie_chart = alt.Chart(df).mark_arc().encode(
    #     theta=alt.Theta(field="value", type="quantitative"),
    #     color=alt.Color(field="reasons of delay", type="nominal"),
    # )
    # st.altair_chart(pie_chart)

if __name__ == '__main__':
    # st.set_page_config(layout="wide")
    st.set_page_config(page_title='Flight Never Delay', page_icon = '✈️', layout = 'centered', initial_sidebar_state = 'expanded')
    intro()
    st.write("Click on one of the following buttons to continue.")
    if st.button("Predict my flight! 🧠"):
        switch_page("Prediction")
    if st.button("Visualize correlations in the data! 📊"):
        switch_page("Visualization")
    st.markdown("""---""")
    filename = "data-coordinates.csv"
    get_data(filename)
    df = pd.read_csv(filename)
    with st.expander("View full dataset"):
        st.subheader("Dataset")
        st.dataframe(df)
#         if st.checkbox("Generate data profile (this takes several minutes as the dataset is large)"):
#             profiler(df)
    
    # nav = st.sidebar.radio("Navigation",
    #                  ("Introduction", "Visualization", "Prediction"))
    # if nav == "Introduction":
    #     intro()
    # elif nav == "Visualization":
    #     vis()
    # else:
    #     pred()

    # profiler(filename)
