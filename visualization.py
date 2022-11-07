import streamlit as st
import pandas as pd
from constants import airline_name
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache
def load_airline_data():
    path = "data/airline.csv"
    return pd.read_csv(path)

def vis_airline_company():
    st.header("Visualize airline company")
    df = load_airline_data()
    airlines = st.multiselect("Please choose airlines",
                              options=[key + ':' + value for key, value in airline_name.items()],
                              default=["WN:Southwest Airlines", "AA:American Airlines",
                                       "DL:Delta Airlines", "UA:United Airlines", "B6:JetBlue Airlines"])
    airlines_abbr = [x.split(":")[0] for x in airlines]
    df_airline = df[df["OP_UNIQUE_CARRIER"].isin(airlines_abbr)]
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
    fig2 = plt.figure(figsize=(10, len(airlines_abbr)*1.5))
    ax = sns.boxplot(data=df_airline, x="ARR_DELAY", y="OP_UNIQUE_CARRIER", showfliers = False, width=0.4)
    ax.yaxis.label.set_visible(False)
    new_labels = [airline_name[x.get_text()] for x in ax.get_yticklabels()]
    ax.set_yticklabels(new_labels)
    plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
    plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
    plt.xlabel('Delay time (minutes)', fontsize=16, weight='bold', labelpad=10)
    st.pyplot(fig2)

def vis_flight_time():
    st.header("Visualize flight time")

def vis_flight_distance():
    st.header("Visualize flight distance")

def vis_flight_destination():
    st.header("Visualize flight destination")

def vis():
    vis_airline_company()
    vis_flight_time()
    vis_flight_distance()
    vis_flight_destination()
