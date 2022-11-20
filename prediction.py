import streamlit as st
import pickle
import pandas as pd
from constants import *
import datetime

transformer_filename = 'Streamlit_rakuten/saved_models/data_transformer.sav'
delay_filename = 'Streamlit_rakuten/saved_models/delay_lin_reg.sav'
cancel_filename = 'Streamlit_rakuten/saved_models/cancel_log_reg.sav'

transformer = pickle.load(open(transformer_filename, 'rb'))
delay_lin_reg_model = pickle.load(open(delay_filename, 'rb'))
cancel_lin_reg_model = pickle.load(open(cancel_filename, 'rb'))


def pred():
    st.header("Predict Flight Delay and Cancellation")

    valid_input = True
    c1, c2 = st.columns(2)
    with c1:
        airline = st.selectbox("Airline",
                                options=[key + ' : ' + value for key, value in airline_name.items()]).split(" : ")[0]
        date = st.date_input("Departure Date", value = datetime.date.today(), min_value = datetime.datetime(2021, 1, 1), max_value = datetime.datetime(2023, 12, 30))
    with c2:
        flight_num = st.text_input('Flight Number', '1111')

    c3, c4 = st.columns(2)
    with c3:
        dpt_airport = st.selectbox("From Airport",
                                options=airports, index = 236)
        arv_airport = st.selectbox("To Airport",
                                options=airports, index = 39)
    with c4:
        dpt_time = int(st.time_input('Expected Departure Time', datetime.time(13,15)).strftime("%-H%M"))
        arv_time = int(st.time_input('Expected Arrival Time', datetime.time(15,00)).strftime("%-H%M"))
        

    if not flight_num.isnumeric():
        st.write('Please enter a numeric value(0-9).')
        valid_input = False
    elif dpt_airport == arv_airport:
        st.write('Please select different departure and arrival airport.')
        valid_input = False
    else:
        valid_input = True

    month = date.month
    day = date.day
    weekday = date.weekday() + 1
    

    if valid_input:
        dummy_data = [[month, day, weekday, airline, int(flight_num), dpt_airport, arv_airport, dpt_time, arv_time]]
        dummy_df = pd.DataFrame(dummy_data, columns=['MONTH', 'DAY_OF_MONTH', 
                'DAY_OF_WEEK', 'OP_UNIQUE_CARRIER', 'OP_CARRIER_FL_NUM', 
                'ORIGIN', 'DEST', 'CRS_DEP_TIME', 
                'CRS_ARR_TIME'])
        input = transformer.transform(dummy_df)
        delay_pred = delay_lin_reg_model.predict(input)[0]
        cancel_pred = cancel_lin_reg_model.predict_proba(input)[0][1] * 100
        if delay_pred < 0:
            st.markdown('\n### Your flight will arrive %d minutes early.\n### The probability of cancellation is %.2f%%.' % (delay_pred, cancel_pred))
        else:
            st.markdown('\n### Your flight will arrive %d minutes late.\n### The probability of cancellation is %.2f%%.' % (delay_pred, cancel_pred))
