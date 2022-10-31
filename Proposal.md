# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay

Group members: David Lin, Qianru Zhang, Hazel Zhang, Xianda Xu, Shiying Pan

## Problem
In our daily life, we always experience flights delay, and there is no good way for us to be informed whether a flight will be delayed in advance. To solve this problem, we would like to use the previous flight data to predict the possibility of delays for flights with certain features. 

## Question
* Do on-time flights share some common features?
* Do some features serve as the main causes of flight delays?
* How might we tell whether a flight is more likely to be on time when buying tickets?

## Scope
* We would like to find the relationship between flight features and on-time rates from January 2018 to August 2022 in the US.
* And also try to build a machine-learning model that can predict 1) whether a flight will be on-time or not, and 2) how much it is likely to delay based on given features such as airline, departure/arrival locations, and time.

## Solution
* Visualizations
	* Geographical map to visualize frequently delayed routes, etc.
	* Correlations between variables such as departure/destination airport, weather, airline company, etc.
* Machine-learning Model
	* Machine learning models like Logistic Regression or Decision Trees to predict the flight delay probability and its potential delay time given factors provided by users.


### Appendix
Dataset: [Bureau Transportation Statistics](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr)
