# Final Project Report

**Project URL**: TODO
**Video URL**: TODO

Short (~250 words) abstract of the concrete data science problem and how the solutions addresses the problem.

## Introduction

## Related Work

## Methods

### Data Processing and Interface



### Visualization

The main challenge we faced when doing visualization was choosing the best charts for our data.

+ Box Plot

We used box plots to show distributions of flight delay values based on airline companies and flight departure time. They can display the five-number summary of a group of data. The five-number summary includes the minimum, first quartile, median, third quartile, and maximum.

+ Binned Scatter Plot

We used binned scatter plots to investigate the relationship between flight delay time and flight distance. The data points in a binned scatter plot are grouped into bins, and an aggregate statistic is used to summarize each bin. For example, we can use a circular area to represent the count and show the density of data points.

+ Map



+ Interactive Chart with Cross-Highlight



### Machine Learning Model



## Results

We studied the relationship between flight delay time and some factors including airline companies, flight departure time, flight distance and flight destination.

+ Airline Companies

We firstly compared the delay time based on airline companies in a box plot. The median and the interquartile range in each box well demonstrate the performance of each airline in flight delay. Alaska Airlines, Southwest Airlines and Delta Airlines are the best 3 performers. Some airlines like Skywest Airlines and JetBlue Airlines do need to pay more attention to their flight delay issues.

Based on the box plot, we identified that the delay time could be categorized into <20 minutes, 20-60 minutes, and >60 minutes. If it is smaller than 20, it is approximately on time. If it is between 20 and 60, it is a small delay that most people can tolerate. If it is larger than 60, the flight encounters a serious delay.

With the new categories of delay, it is easy to observe that the proportion of delays varies from airline to airline. Some airlines like JetBlue Airlines behave badly. They have a relatively low on-time rate and a relatively high large delay rate. Although SouthWest Airlines has the largest number of flight delays, these delays are mainly small delays and the company maintains a pretty good on-time rate.

<div align=center><img width="1000" height="400" src="https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay/blob/main/image/report1.png"/></div>

To sum up, airline companies behave very much differently in dealing with flight delay problems. It is safe to deduce that choosing an airline company would influence flight delay.

+ Flight Departure Time



<div align=center><img width="900" height="350" src="https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay/blob/main/image/report2.png"/></div>



+ Flight Distance



<div align=center><img width="700" height="300" src="https://github.com/CMU-IDS-Fall-2022/final-project-flight-never-delay/blob/main/image/report3.png"/></div>



+ Flight Destination



## Discussion

## Future Work
