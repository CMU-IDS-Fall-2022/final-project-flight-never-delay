import streamlit as st
import pandas as pd
from constants import airline_name
import seaborn as sns
import matplotlib.pyplot as plt
from vega_datasets import data
import altair as alt

@st.cache
def load_airline_data():
    path = "data/airline.csv"
    return pd.read_csv(path)

@st.cache
def load_time_data():
    path = "data/time.csv"
    return pd.read_csv(path)

@st.cache
def load_destination_data():
    path = "data/destination.csv"
    return pd.read_csv(path)

def vis_airline_company():
    st.header("Airline company")
    st.write("Flight delay rate is an important factor when measuring the reliability of an airline company.")
    st.write("\"Which airline has the worst/best delay rate in 2021?\"")
    st.write("In this part, we have selected top 10 airlines with the most flights in 2021 and would like to explore "
             "how they hehave in dealing with the flight delay issues.")
    df = load_airline_data()
    airlines = st.multiselect("Please choose airline companies",
                              options=[key + ':' + value for key, value in airline_name.items()],
                              default=["WN:Southwest Airlines", "AA:American Airlines",
                                       "DL:Delta Airlines", "UA:United Airlines", "B6:JetBlue Airlines"])
    airlines_abbr = [x.split(":")[0] for x in airlines]
    df_airline = df[df["OP_UNIQUE_CARRIER"].isin(airlines_abbr)]
    st.write("First, we would like to compare the delay counts in a bar chart. "
             "Assume t is the flight delay time. If t is smaller than 20, it is approximately on time. "
             "If t is between 20 and 60, it is a small delay that most people can tolerate."
             "If t is bigger than 60, the flight encounters a serious delay.")
    def delay_type(x):
        if x <= 20:
            return 0
        elif x <= 60:
            return 1
        return 2
    df_airline["TYPE"] = df_airline["ARR_DELAY"].apply(delay_type)
    fig1 = plt.figure(figsize=(10, len(airlines_abbr)*1.5))
    ax = sns.countplot(data=df_airline, y="OP_UNIQUE_CARRIER", hue="TYPE")
    ax.yaxis.label.set_visible(False)
    new_labels = [airline_name[x.get_text()] for x in ax.get_yticklabels()]
    ax.set_yticklabels(new_labels)
    plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
    plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
    new_legend = plt.legend()
    new_legend.get_texts()[0].set_text("on time (<20 min)")
    new_legend.get_texts()[1].set_text("small delay (20~60 min)")
    new_legend.get_texts()[2].set_text("large delay (>60 min)")
    plt.xlabel('Number of flights', fontsize=16, weight='bold', labelpad=10)
    st.pyplot(fig1)
    st.write("It is easy to observe that the proportion of delays varies from airline to airline. "
             "Some airlines like JetBlue Airlines behave badly. They have a relatively low on-time rate and a relatively high large delay rate. "
             "Although Southwest Airlines has the largest number of flight delays, these delays are mainly small delays and "
             "the company maintains a pretty good on-time rate.")
    st.write("Second, we would like to walk deep into comparing the delay time in a box plot.")
    fig2 = plt.figure(figsize=(10, len(airlines_abbr)*1.5))
    ax = sns.boxplot(data=df_airline, x="ARR_DELAY", y="OP_UNIQUE_CARRIER", showfliers = False, width=0.4)
    ax.yaxis.label.set_visible(False)
    new_labels = [airline_name[x.get_text()] for x in ax.get_yticklabels()]
    ax.set_yticklabels(new_labels)
    plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
    plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
    plt.xlabel('Delay time (minutes)', fontsize=16, weight='bold', labelpad=10)
    st.pyplot(fig2)
    st.write("The median and the interquartile range in each box well demonstrate the performance of each airline in flight delay. "
             "Alaska Airlines, Southwest Airlines and Delta Airlines are the best 3 performers. "
             "Some airlines like Skywest Airlines and JetBlue Airlines do need to pay more attention to their flight delay issues.")
    st.write("To sum up, airline companies behave very much differently in dealing with flight delay problems. "
             "It is safe to deduce that choosing an airline company would influence flight delay.")

def vis_flight_time():
    st.header("Flight time")
    df = load_time_data()

def vis_flight_distance():
    st.header("Flight distance")

def map_chart():
    states = alt.topo_feature(data.us_10m.url, feature='states')
    base = alt.Chart(states).mark_geoshape(fill='lightgray', stroke='black', strokeWidth=0.5)
    df = load_destination_data()
    ansi = pd.read_csv('https://www2.census.gov/geo/docs/reference/state.txt', sep='|')
    ansi.columns = ['id', 'abbr', 'state', 'statens']
    ansi = ansi[['id', 'state', 'abbr']]
    geo_data = df.groupby('DEST_STATE')['ARR_DELAY'].mean().reset_index()
    geo_data.columns = ['abbr', 'time']
    geo_data = pd.merge(geo_data, ansi, how='left', on='abbr')
    alt_fig = alt.Chart(states).mark_geoshape().encode(
        color='time:Q',
        tooltip=['state:N', alt.Tooltip('time:Q')]
	).transform_lookup(
        lookup='id',
        from_=alt.LookupData(geo_data, 'id', ['time','state'])
	).project(
        type='albersUsa'
	)
    return base + alt_fig

def vis_flight_destination():
    st.header("Flight destination")
    st.altair_chart(map_chart()) 


def vis():
    st.write("# Which factors lead to flight delay?")
    vis_airline_company()
    vis_flight_time()
    vis_flight_distance()
    vis_flight_destination()
