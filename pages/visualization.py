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
def load_distance_data():
    path = "data/distance.csv"
    return pd.read_csv(path)

@st.cache
def load_destination_data():
    path = "data/destination.csv"
    return pd.read_csv(path)

@st.cache
def load_airline_time_data():
    path = "data/airline_time.csv"
    return pd.read_csv(path)

@st.cache
def load_route_data():
    path = "data/routes.csv"
    return pd.read_csv(path)

@st.cache
def load_origin_data():
    path = "data/origin.csv"
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
                                       "DL:Delta Airlines", "UA:United Airlines", "B6:JetBlue Airlines"],
                              key='airlines')
    airlines_abbr = [x.split(":")[0] for x in airlines]
    df_airline = df[df["OP_UNIQUE_CARRIER"].isin(airlines_abbr)]

    def delay_type(x):
        if x <= 20:
            return 0
        elif x <= 60:
            return 1
        return 2
    df_airline["TYPE"] = df_airline["ARR_DELAY"].apply(delay_type)

    st.write("Firstly, we compared the delay time in a box plot. "
             "The median and the interquartile range in each box well demonstrate the performance of each airline in flight delay. "
             "Alaska Airlines, Southwest Airlines and Delta Airlines are the best 3 performers. "
             "Some airlines like Skywest Airlines and JetBlue Airlines do need to pay more attention to their flight delay issues.")
    fig2 = plt.figure(figsize=(10, len(airlines_abbr) * 1.5))
    ax = sns.boxplot(data=df_airline, x="ARR_DELAY", y="OP_UNIQUE_CARRIER", showfliers=False, width=0.4, palette='Spectral')
    ax.yaxis.label.set_visible(False)
    # change the plot box color
    for i, artist in enumerate(ax.patches):
        # Set the linecolor on the artist to the facecolor, and set the facecolor to None
        col = artist.get_facecolor()
        artist.set_edgecolor(col)    

    
    new_labels = [airline_name[x.get_text()] for x in ax.get_yticklabels()]
    ax.set_yticklabels(new_labels)
    plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
    plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
    plt.xlabel('Delay time (minutes)', fontsize=16, weight='bold', labelpad=10)
    st.pyplot(fig2)

    st.write("Based on the box plot, we identified that the delay time could be "
             "categorized into <20 minutes, 20-60 minutes, and >60 minutes. "
             "If it is smaller than 20, it is approximately on time. "
             "If it is between 20 and 60, it is a small delay that most people can tolerate. "
             "If it is larger than 60, the flight encounters a serious delay.")
    st.write("With the new categories of delay, it is easy to observe that the proportion of delays varies from "
             "airline to airline. Some airlines like JetBlue Airlines behave badly. They have a relatively "
             "low on-time rate and a relatively high large delay rate. "
             "Although SouthWest Airlines has the largest number of flight delays, these delays are mainly "
             "small delays and the company maintains a pretty good on-time rate.")
    fig1 = plt.figure(figsize=(10, len(airlines_abbr)*1.5))
    ax = sns.countplot(data=df_airline, y="OP_UNIQUE_CARRIER", hue="TYPE", palette='Spectral')
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

    st.write("To sum up, airline companies behave very much differently in dealing with flight delay problems. "
             "It is safe to deduce that choosing an airline company would influence flight delay.")

def vis_flight_time():
    st.header("Flight time")
    st.write("Next, we would like to sketch a box plot to identify the relationship between delay time and "
             "flight departure time (Quarter / Month / Day of Week).")
    time_scale = st.radio("Please select a time scale",
                          ("Quarter", "Month", "Day of Week"))
    df_time = load_time_data()
    if time_scale == "Quarter":
        st.write("It can be observed that a long flight delay is more likely to happen in Quarter 2 & 3 than in Quarter 1 & 4.")
        fig = plt.figure(figsize=(10, 4*1.5))
        ax = sns.boxplot(data=df_time, x="ARR_DELAY", y="QUARTER", showfliers=False, orient="h", width=0.4, palette='Spectral')
        # change the plot box color
        for i, artist in enumerate(ax.patches):
            # Set the linecolor on the artist to the facecolor, and set the facecolor to None
            col = artist.get_facecolor()
            artist.set_edgecolor(col)   
        plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
        plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
        plt.ylabel('Quarter', fontsize=16, weight='bold', labelpad=10)
        plt.xlabel('Delay time (minutes)', fontsize=16, weight='bold', labelpad=10)
        st.pyplot(fig)
    elif time_scale == "Month":
        st.write("It can be observed that summer is the peak season for flight delays.")
        fig = plt.figure(figsize=(10, 12 * 1))
        ax = sns.boxplot(data=df_time, x="ARR_DELAY", y="MONTH", showfliers=False, orient="h", width=0.4, palette='Spectral')
        for i, artist in enumerate(ax.patches):
            # Set the linecolor on the artist to the facecolor, and set the facecolor to None
            col = artist.get_facecolor()
            artist.set_edgecolor(col)  
        plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
        plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
        plt.ylabel('Month', fontsize=16, weight='bold', labelpad=10)
        plt.xlabel('Delay time (minutes)', fontsize=16, weight='bold', labelpad=10)
        st.pyplot(fig)
    else:
        st.write("It can be observed that it is more likely to encounter a flight delay on Monday.")
        fig = plt.figure(figsize=(10, 7 * 1))
        ax = sns.boxplot(data=df_time, x="ARR_DELAY", y="DAY_OF_WEEK", showfliers=False, orient="h", width=0.4, palette='Spectral')
        for i, artist in enumerate(ax.patches):
            # Set the linecolor on the artist to the facecolor, and set the facecolor to None
            col = artist.get_facecolor()
            artist.set_edgecolor(col)  
        plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
        plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
        plt.ylabel('Day of Week', fontsize=16, weight='bold', labelpad=10)
        plt.xlabel('Delay time (minutes)', fontsize=16, weight='bold', labelpad=10)
        st.pyplot(fig)
    st.write("To sum up, flight time is also an important factor leading to flight delay. "
             "Long flight delays are more likely to happen during the summer or on Monday.")

def vis_flight_distance():
    st.header("Flight distance")
    st.write("Even though we have "
             "Next, we would like to sketch a binned scattered plot to identify the relationship between delay time "
             "and flight distance. The data points in the plot are grouped into bins with a circle in each bin to "
             "represent the amount of flights in that bin and its percentage to the total number of flights.")
    data_type = st.radio("Please select a data type",
                          ("Amount", "Percentage"))
    df = load_distance_data()
    df_distance = df[["DISTANCE", "ARR_DELAY"]]
    def delay_type(x):
        if x <= 20:
            return 0
        elif x <= 60:
            return 1
        return 2
    df_distance["TYPE"] = df_distance["ARR_DELAY"].apply(delay_type)
    df_distance = df_distance[df_distance["ARR_DELAY"] < 120]
    df_distance = df_distance[df_distance["DISTANCE"] < 2000]
    df_distance = df_distance.sample(50000, random_state=0)

    # fig = plt.figure(figsize=(10, 10))
    # ax = sns.histplot(data=df_distance, x="ARR_DELAY", y="DISTANCE", bins=20)
    # plt.setp(ax.get_yticklabels(), fontsize=10, weight='bold', rotation=0)
    # plt.setp(ax.get_xticklabels(), fontsize=10, weight='bold', rotation=0)
    # plt.ylabel('Flight Distance (miles)', fontsize=16, weight='bold', labelpad=10)
    # plt.xlabel('Delay time (minutes)', fontsize=16, weight='bold', labelpad=10)
    # st.pyplot(fig)

    if data_type == "Percentage":
        fig1 = alt.Chart(df_distance).transform_bin(
            "ARR_DELAY_bin", field="ARR_DELAY"
        ).transform_joinaggregate(
            total="count()",
            groupby=["ARR_DELAY_bin"]
        ).transform_joinaggregate(
            in_group="count()",
            groupby=["ARR_DELAY_bin", "DISTANCE"]
        ).transform_calculate(
            percentage=alt.datum.in_group / alt.datum.total
        ).mark_circle(color= '#66c2a5').encode(
            alt.X("ARR_DELAY:Q", bin=True, axis=alt.Axis(title="Delay Time (minutes)", titleFontSize=20)),
            alt.Y("DISTANCE", bin=True, axis=alt.Axis(title="Flight Distance (miles)", titleFontSize=20)),
            alt.Size("percentage:Q", legend=alt.Legend(format='%', title='Percentage', titleFontSize=15)),
            tooltip=[alt.Tooltip('percentage:Q')]
        )
        fig1.width = 800
        fig1.height = 400
        st.altair_chart(fig1)
    else:
        fig2 = alt.Chart(df_distance).mark_circle(color= '#66c2a5').encode(
            alt.X("ARR_DELAY:Q", bin=True, axis=alt.Axis(title="Delay Time (minutes)", titleFontSize=20)),
            alt.Y("DISTANCE:Q", bin=True, axis=alt.Axis(title="Flight Distance (miles)", titleFontSize=20)),
            size="count()",
            tooltip=["count()"]
        )
        fig2.width = 800
        fig2.height = 400
        st.altair_chart(fig2)
    st.write("It can be seen in the plot that flight distance seems not to be a key factor to delay time.")

def destination_map():
    states = alt.topo_feature(data.us_10m.url, feature='states')
    base = alt.Chart(states).mark_geoshape(fill='lightgray', stroke='black', strokeWidth=0.5)
    df = load_destination_data()
    df = df[df["ARR_DELAY"] < 400]
    ansi = pd.read_csv('https://www2.census.gov/geo/docs/reference/state.txt', sep='|')
    ansi.columns = ['id', 'abbr', 'state', 'statens']
    ansi = ansi[['id', 'state', 'abbr']]
    geo_data = df.groupby('DEST_STATE')['ARR_DELAY'].mean().reset_index()
    geo_data.columns = ['abbr', 'Delay Time']
    geo_data = pd.merge(geo_data, ansi, how='left', on='abbr')
    alt_fig = alt.Chart(states).mark_geoshape().encode(
        color = alt.Color('Delay Time:Q', scale=alt.Scale(scheme='lightmulti')),
        tooltip=['state:N', alt.Tooltip('Delay Time:Q')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(geo_data, 'id', ['Delay Time','state'])
    ).project(
        type='albersUsa'
    ).properties(
        width=800
    )
    return base + alt_fig

def vis_flight_destination():
    st.header("Flight destination")
    st.write("We are also interested the relationship between the delay time and destination. We want to see whether "
             "there are some destinations that are likely to delay longer time than other places. The data points in the plot are "
             "grouped into states. We caluculated the average delay time for the flights that arrives at each state."
             "to avoid the impact of extreme data points, we only take delay times that are under 400 mins.")
    st.altair_chart(destination_map())
    st.write("We can see if you are planning to go to the north eastern part of the country, the flights might delay longer.") 

def origin_map():
    states = alt.topo_feature(data.us_10m.url, feature='states')
    base = alt.Chart(states).mark_geoshape(fill='lightgray', stroke='black', strokeWidth=0.5)
    df = load_origin_data()
    df = df[df["ARR_DELAY"] < 400]
    ansi = pd.read_csv('https://www2.census.gov/geo/docs/reference/state.txt', sep='|')
    ansi.columns = ['id', 'abbr', 'state', 'statens']
    ansi = ansi[['id', 'state', 'abbr']]
    geo_data = df.groupby('ORIGIN_STATE')['ARR_DELAY'].mean().reset_index()
    geo_data.columns = ['abbr', 'Delay Time']
    geo_data = pd.merge(geo_data, ansi, how='left', on='abbr')
    alt_fig = alt.Chart(states).mark_geoshape().encode(
        color = alt.Color('Delay Time:Q', scale=alt.Scale(scheme='lightmulti')),
        tooltip=['state:N', alt.Tooltip('Delay Time:Q')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(geo_data, 'id', ['Delay Time','state'])
    ).project(
        type='albersUsa'
    ).properties(
        width=800
    )
    return base + alt_fig


def vis_flight_origin():
    st.header("Flight origin")
    st.write("Same as the previous one, we also want to see relationship between the delay time and origins.")
    st.altair_chart(origin_map()) 
    st.write("We can see from the map that if you departure from several states in the middle US (like North Dakota, Wyoming or Mississipi)"
             "you might delay for longer time.")



def vis_flight_delay_distribution_over_time():
    st.header("Flight delay distribution over time")
    st.write("To further discuss the relationship between delay time and different timestamp, we take a look at the delay time. The color indicates the number of flights with the delay time (y-axis) on the given time categoary (x-axis) for a selected time scale. The size of circle indicates the percentage (likelihood) of a delay time occured on each time categoary. Randomly sample 5000 from the data for efficient computation purpose.")
    scale = st.radio("Please select a time scale",
                          ("Quarter", "Month", "Day of Week"), key='scale')
    st.altair_chart(plot_delay_over_time(scale)) 
    st.write("If we choose quarter at the above chart, we can see that quarter 3 has the most number of flights thats delay under 40 mins, it seems that quarter 3 might be a good choice to fly. But if we take a look at the percentage(likelyhood) of a delay time happend in each quarter, we can see that quarter 1 actually has the highest percentage of flights that delay under 40 mins, which means, if you travel in quarter 1, you'll have higher chance to delay for a little while. Likewise, we can also see March and Wednesday has the lowest chances of delay higher than 40. These time might be the better choice for flying.")
    st.write("We could also spect the distribution for specfic airlines. Take American Airline (AA) as an example, we can see Wednesday has most flights and lowest delay rate, which makes Wednesday a best choice for AA. Same for quarters and months.")


def plot_delay_over_time(scale):

    time_scale_dic = {"Quarter": "QUARTER", "Month": "MONTH", "Day of Week": "DAY_OF_WEEK"}
    airlines = ['WN','AA','OO','DL','UA','B6','YX','NK']
    df_time = load_airline_time_data()
    df_time = df_time[df_time["ARR_DELAY"] < 200]
    df_time = df_time[df_time["OP_UNIQUE_CARRIER"].isin(airlines)]
    df_time = df_time.sample(5000, random_state=0)
    
    pts = alt.selection(type="single", encodings=['x'])
    # "QUARTER" "%s:N"%(time_scale_dic[scale])

    rect = alt.Chart(df_time).mark_rect().encode(
                alt.Y("ARR_DELAY:Q", bin=True),
                alt.X("%s:N"%(time_scale_dic[scale])),
                color = alt.Color("count()", scale=alt.Scale(scheme='lightmulti'))
            ).transform_filter(
                pts
            )
    rect.width = 600
    rect.height = 400

    circle = alt.Chart(df_time).transform_bin(
                "ARR_DELAY_bin", field="ARR_DELAY"
            ).transform_filter(
                pts
            ).transform_joinaggregate(
                total="count()",
                groupby=["%s"%(time_scale_dic[scale])]
            ).transform_joinaggregate(
                in_group="count()",
                groupby=["%s"%(time_scale_dic[scale]), "ARR_DELAY_bin"]
            ).transform_calculate(
                PERCENT_BY_ARR_DELAY=alt.datum.in_group / alt.datum.total
            ).mark_circle(color= '#66c2a5').encode(
                alt.Y("ARR_DELAY:Q", bin=True, axis=alt.Axis(title="Delay Time (minutes)", titleFontSize=14)),
                alt.X("%s:N"%(time_scale_dic[scale]), axis=alt.Axis(title=scale, titleFontSize=14, labelAngle=0)),
                alt.Size("PERCENT_BY_ARR_DELAY:Q", scale=alt.Scale(range=[0, 2000]), legend=alt.Legend(format='%', title='Percentage')),
                tooltip=["%s:N"%(time_scale_dic[scale]), "count()", alt.Tooltip('PERCENT_BY_ARR_DELAY:Q', format='.2f')]
            )
    circle.width = 600
    circle.height = 400

    bar = alt.Chart(df_time).mark_bar().encode(
        x=alt.X('OP_UNIQUE_CARRIER:N', sort='-y', axis=alt.Axis(title="Operating Carrier", labelAngle=0, titleFontSize=14)),
        y=alt.Y('count()', axis=alt.Axis(titleFontSize=14)),
        color=alt.condition(pts, alt.ColorValue("#5aa6bb"), alt.ColorValue("lightgrey")),
        tooltip=['OP_UNIQUE_CARRIER:N', 'count()']
    ).properties(
        width=600,
        height=200
    ).add_selection(pts)

    fig = alt.vconcat(
        rect + circle,
        bar
    ).resolve_legend(
        color="independent",
        size="independent"
    )
    
    return fig


def vis_flight_delay_distribution_over_location():
    st.header("Flight delay distribution over origin and destination")
    st.write("Finally, we want to see whether there are some specific routes between cities are especially likely to delay. "
             "The circle indicate the number of flights departed from this airport. We can see there are some larger airport hub where the circles are larger. If we hover on one airport, we can see all the routes that departs from this airport. The width of the connection indicates the number of flights between the two airports and the color of the edge indicates the average delay time between the two airports. Let's take Chicago ORD airport as an example. We can see it has most frequent flights to Los Angles, and the delay time is relatively low. However if you go to Rhode Island from Chicago, there will be less flights options and there are higher chances for delay.")
    st.write("P.S. We randomly sampled 5000 from the dataset for efficient computation purpose.")
    st.altair_chart(plot_delay_over_location()) 


def plot_delay_over_location():
    df_routes = load_route_data()
    df_routes = df_routes[df_routes["ARR_DELAY"] < 400]
    df_routes = df_routes.sample(5000, random_state=0)
    
    states = alt.topo_feature(data.us_10m.url, feature="states")

    background = alt.Chart(states).mark_geoshape(
        fill="#ecf4f6",
        stroke="white"
    ).properties(
        width=750,
        height=500
    ).project("albersUsa")

    flights_airport = df_routes
    select_city = alt.selection_single(
        on="mouseover", nearest=True, fields=["ORIGIN"], empty="none"
    )

    connections = alt.Chart(flights_airport
    ).transform_filter(
        (alt.datum.ORIGIN_STATE != "PR") & (alt.datum.ORIGIN_STATE != "VI") & (alt.datum.DEST_STATE != "PR") & (alt.datum.DEST_STATE != "VI")
    ).transform_joinaggregate(
        Count="count()",
        Avg_Delay='mean(ARR_DELAY)',
        groupby=["ORIGIN", "DEST"]
    ).mark_rule(opacity=0.5).encode(
        latitude="ORIGIN_LAT:Q",
        longitude="ORIGIN_LONG:Q",
        latitude2="DEST_LAT:Q",
        longitude2="DEST_LONG:Q",
        size=alt.Size("Count:Q", scale=alt.Scale(range=[0, 500]), legend=None),
        color=alt.Color("Avg_Delay:Q", scale=alt.Scale(scheme='lightmulti', domain=[0, 200]), legend=alt.Legend(title='Average Delay (min)'))
    ).transform_filter(
        select_city
    )

    points = alt.Chart(flights_airport
    ).transform_filter(
        (alt.datum.ORIGIN_STATE != "PR") & (alt.datum.ORIGIN_STATE != "VI") & (alt.datum.DEST_STATE != "PR") & (alt.datum.DEST_STATE != "VI")
    ).transform_joinaggregate(
        Total_Flights="count()",
        groupby=["ORIGIN"]
    ).mark_circle(color= '#66c2a5').encode(
        latitude="ORIGIN_LAT:Q",
        longitude="ORIGIN_LONG:Q",
        size=alt.Size("Total_Flights:Q", scale=alt.Scale(range=[0, 1000]), legend=None),
        order=alt.Order("Total_Flights:Q", sort="descending"),
        tooltip=["ORIGIN:N", "Total_Flights:Q"]
    ).add_selection(
        select_city
    )

    return (background + connections + points).configure_view(stroke=None)


def vis():
    st.write("# Which factors lead to flight delay?")
    vis_airline_company()
    vis_flight_time()
    vis_flight_distance()
    vis_flight_destination()
    vis_flight_origin()
    vis_flight_delay_distribution_over_time()
    vis_flight_delay_distribution_over_location()

vis()