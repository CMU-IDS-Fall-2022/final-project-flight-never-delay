# Final Project Report

**Project URL**: https://cmu-ids-fall-2022-final-project-flight-never-delay-app-v0b442.streamlit.app/

**Video URL**: TODO

Short (~250 words) abstract of the concrete data science problem and how the solutions addresses the problem.

## Introduction
As frequent travelers, our group members often experience flight delays. Flight delays can be heavily disrupted to travel schedules, such as missing important events or having to book extra nights for accomodation. However, this is no good way for us to know whether a flight will be delayed, until at the final moment. In this project, we aim to address this problem by predicting potential flight delays through analyzing past flight delay records. Specifically, we ask the following two questions to guide our exploration:

1. What are the main factors that serve as the causes of flight delays? To answer this question, we perform exploratory data analysis and describe our results through several interactive data visualizations.
2. Given a set of factors, can we predict whether a flight is likely to be delayed? To answer this question, we implement a machine learning model to predict flight delays and possible reasons, given a selection of flight details.

In this report, we give an overview of our dataset, outline how we built our interface, visualizations, and machine learning model, and discuss key findings from our data exploration.

## Related Work

Our project is situated among previous works in visualization flight data and recommender systems with interactive visualizations.

### Visualizing Flight Data

### Recommeder Systems with Interactive Visualizations

## Methods

### Data Processing

#### Data Cleaning and Augmentation

We use a dataset containing flight delay records from the [Bureau of Transportation Statistics - On-Time : Marketing Carrier On-Time Performance](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr). The full dataset is very large (many millions of data points) - spanning from January 2018 to August 2022 with over 100 fields. For the purpose of this project, we select a subset of the data from January 2021 to December 2021 and include only 23 fields. The 23 fields are:
* Time information (YEAR, QUARTER, MONTH, DAY_OF_MONTH, DAY_OF_WEEK) - We include this to uncover correlations between time and flight delays. We also hypothesize that day of the week (e.g. Monday) will influence flight delays.
* Flight carrier (OP_UNIQUE_CARRIER, OP_CARRIER_FL_NUM) - We include this to uncover correlations between flight carriers (e.g. United Airlines) and flight delays.
* Location information (ORIGIN, DEST, DISTANCE) - We include this to uncover correlations between location/distance and flight delays.
* Flight times, delays, and reasons (CRS_DEP_TIME, DEP_TIME, DEP_DELAY, CRS_ARR_TIME, ARR_TIME, ARR_DELAY, CARRIER_DELAY, WEATHER_DELAY, NAS_DELAY, SECURITY_DELAY, LATE_AIRCRAFT_DELAY) - We include this to measure whether a flight is delayed and the degree that it was delayed for. We also include the reasons behind the delays (e.g. weather) to see if they have correlations with other fields (e.g. location).
* Cancellations and reasons (CANCELLED, CANCELLATION_CODE) - Like delays and reasons, we include similar attributes for cancellations.

Our uncleaned dataset contains 6,311,871 data points.

<img src="image/img_1.png" alt="uncleaned dataset" width="500"/>

For data cleaning, we first drop duplicates and remove data points that contain empty fields. Then, we separate flights that are delayed and cancelled. For delayed flights, we data points that do not have a delay reason (e.g. one of CARRIER_DELAY, WEATHER_DELAY, NAS_DELAY, SECURITY_DELAY, LATE_AIRCRAFT_DELAY). For canceled flights, we similarly remove data points that do not have a cancellation reason (CANCELLATION_CODE).

We also augment our dataset with more fine-grained geographic information as we would like to create a geographic map to visualize the flight delays. Therefore, we map airport location (ORIGIN, DEST) to US state names and coordinates (latitude and longitude) from a [Kaggle dataset](https://www.kaggle.com/datasets/usdot/flight-delays?select=airports.csv). This adds 6 more fields to our dataset (ORIGIN_STATE, ORIGIN_LAT, ORIGIN_LONG, DEST_STATE, DEST_LAT, DEST_LONG). We remove data points that include airports with unknown geographical locations.

Our final dataset contains 1,141,693 data points with 29 fields.

<img src="image/img_2.png" alt="cleaned dataset" width="500"/>

#### Data Exploration

<img src="image/img_3.png" alt="basic data exploration" width="400"/>

We explored the relationship between DEP_DELAY and factors including MONTH, DAY_OF_MONTH, DAY_OF_WEEK, OP_UNIQUE_CARRIER, ORIGIN, DEST, DEP_TIME, and DISTANCE.
These explorations provide us with the following inspirations:

* Divide the DEP_DELAY(delay time) into different intervals as there are too many data points, which is hard for us to tell the correlations. 

* Instead of using scatter plots, we probably need to use binned scatter points to better display the distribution of the dataset.

* When exploring relationships between ORIGIN (departure location) and DEP_DELAY, it makes more sense to use a map.

* Meanwhile, we find that aside from the number of flights, the percentage of flights(delayed flights/all flights) is also important, as some big hubs might have more flights and therefore have more delays, but that doesn’t mean you have a higher chance of delay when you depart from this city.

<img src="image/img_4.png" alt="drawing" width="30%"/><img src="image/img_5.png" alt="drawing" width="30%"/><img src="image/img_6.png" alt="drawing" width="30%"/><img src="image/img_7.png" alt="drawing" width="30%"/><img src="image/img_8.png" alt="drawing" width="30%"/><img src="image/img_9.png" alt="drawing" width="30%"/><img src="image/img_10.png" alt="drawing" width="30%"/><img src="image/img_11.png" alt="drawing" width="30%"/>

### Interface

We use Streamlit for our interface implementation. Our app is a multipage app containing the Home page, the Prediction page, and the Visualization page. We use [Streamlit Extras](https://github.com/arnaudmiribel/streamlit-extras) to support page switching buttons. We use caching (`@st.cache()`) for intensive operations such as downloading the data file hosted on Google Drive.

#### Home Page

The Home page gives a quick introduction of the project and an overview of the dataset the project is built on. The user may view the full dataset from an expander. In addition, two buttons lead to the other two pages.

<img src="image/home_interface.png" alt="home interface" width="400"/>

#### Prediction Page

The Prediction page allows users to fill in their flight information in a form. The form has various input fields such as an airline selection box, date picker, and text input fields. We have some basic data validation such as checking if the flight number is numeric and whether the arrival and departure airports are different. Based on user-provided details, we predict probabilities that the flight will be delayed or cancelled (see Machine Learning Model section).

<img src="image/prediction_interface.png" alt="prediction interface" width="400"/>

#### Visualization Page

The Visualization page presents our data explorations with several interactive data visualizations (see Visualization section and Results section). The user may play around with various input parameters based on their data exploration interests.

<img src="image/visualization_interface.png" alt="visualization interface" width="400"/>

### Visualization

We use Altair and Matplotlib for our visualizations implementation. The main challenge we faced when doing visualization was choosing the best charts for our data.

#### Box Plot

We used box plots to show distributions of flight delay values based on airline companies and flight departure time. They can display the five-number summary of a group of data. The five-number summary includes the minimum, first quartile, median, third quartile, and maximum.

#### Binned Scatter Plot

We used binned scatter plots to investigate the relationship between flight delay time and flight distance. The data points in a binned scatter plot are grouped into bins, and an aggregate statistic is used to summarize each bin. For example, we can use a circular area to represent the count and show the density of data points.

#### Map



#### Interactive Chart with Cross-Highlight



### Machine Learning Model



## Results

We studied the relationship between flight delay time and some factors including airline companies, flight departure time, flight distance and flight destination.

### Airline Companies

We firstly compared the delay time based on airline companies in a box plot. The median and the interquartile range in each box well demonstrate the performance of each airline in flight delay. Alaska Airlines, Southwest Airlines and Delta Airlines are the best 3 performers. Some airlines like Skywest Airlines and JetBlue Airlines do need to pay more attention to their flight delay issues.

Based on the box plot, we identified that the delay time could be categorized into <20 minutes, 20-60 minutes, and >60 minutes. If it is smaller than 20, it is approximately on time. If it is between 20 and 60, it is a small delay that most people can tolerate. If it is larger than 60, the flight encounters a serious delay.

With the new categories of delay, it is easy to observe that the proportion of delays varies from airline to airline. Some airlines like JetBlue Airlines behave badly. They have a relatively low on-time rate and a relatively high large delay rate. Although SouthWest Airlines has the largest number of flight delays, these delays are mainly small delays and the company maintains a pretty good on-time rate.

<div align=center><img width="1000" height="400" src="https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay/blob/main/image/report1.png"/></div>

To sum up, airline companies behave very much differently in dealing with flight delay problems. It is safe to deduce that choosing an airline company would influence flight delay.

### Flight Departure Time

We then sketched another box plot to study the distributions of flight delay time values based on flight departure time (Quarter / Month / Day of Week). It can be observed that: (1) a long flight delay is more likely to happen in Quarter 2 & 3 than in Quarter 1 & 4; (2) it is more likely to encounter a flight delay on Monday.

<div align=center><img width="900" height="350" src="https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay/blob/main/image/report2.png"/></div>

To sum up, flight time is also an important factor leading to flight delay. Long flight delays are more likely to happen during the summer or on Monday.

### Flight Distance

We then drew a binned scattered plot to identify the relationship between delay time and flight distance. The data points in the plot are grouped into bins with a circle in each bin to represent the amount of flights in that bin and its percentage to the total number of flights.

<div align=center><img width="600" height="300" src="https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay/blob/main/image/report3.png"/></div>

It can be seen in the plot that flight distance seems not to be a key factor to delay time.

### Flight Destination



## Discussion

## Future Work
