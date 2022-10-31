# Final Project Proposal

Group members: David Lin, Qianru Zhang, Hazel Zhang, Xianda Xu, Shiying Pan

**GitHub Repo URL**: https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay

## Problem Description
As frequent travelers, our group members often experience flight delays. However, there is no good way for us to be informed on whether a flight will be delayed in advance. To address this problem, we would like to use data on previous flights to predict the possibility of delays for future flights.

## Question
To guide our project, we ask the following questions:
* Do delayed flights share some common factors? If so, what are the factors that serve as the main causes of flight delays?
* Given a set of factors, can we predict whether a flight is likely to be delayed? This may serve as a recommendation system for buying tickets.

## Proposed Solution
To address our problem, we aim to build a prediction model and various visualization components.
* Modelling
	* We plan to explore training ML models such as logistic regression or decision trees to predict flight delay probabilities and its potential delay time given flight details from the user.
* Visualizations
	* We plan to create a geographical map to visualize delayed routes. This visualization may reveal patterns such as frequently delayed routes.
	* We plan to create correlation charts between various variables such as departure/destination airport, weather, airline company, etc. This visualization may reveal the importance of various factors and their correlations and dependencies.

## Scope
We plan to split our project evenly between our group members. The main components of this project include:
* Cleaning the dataset (see Appendix).
* Building various flight delay prediction models and analyzing their performances.
* Creating the visualizations, such as the geographical map and various types of correlation graphs. We plan to use Altair.
* Building the frontend interface to handle user interaction and display the visualizations. We plan to use Streamlit.

### Appendix
We plan to use the [Bureau of Transportation Statistics - On-Time : Marketing Carrier On-Time Performance dataset](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr) for our project. The dataset contains 563,738 data points of flight delays from January 2018 to August 2022 in the US (~300MB csv file). Each data points contains detailed information such as flight date, airline, origin/destination airport, distance between airports, and delay time (including carrier delay, weather delay, security delay, etc.).
