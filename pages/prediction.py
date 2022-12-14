import streamlit as st
import pickle
import pandas as pd
from constants import *
import datetime

transformer_filename = 'saved_models/data_transformer.sav'
delay_carrier_filename = 'saved_models/delay_carrier_lin_reg.sav'
delay_weather_filename = 'saved_models/delay_weather_lin_reg.sav'
delay_nas_filename = 'saved_models/delay_nas_lin_reg.sav'
delay_security_filename = 'saved_models/delay_security_lin_reg.sav'
delay_late_aircraft_filename = 'saved_models/delay_late_aircraft_lin_reg.sav'
cancel_filename = 'saved_models/cancel_log_reg.sav'

transformer = pickle.load(open(transformer_filename, 'rb'))
delay_carrier_lin_reg_model = pickle.load(open(delay_carrier_filename, 'rb'))
delay_weather_lin_reg_model = pickle.load(open(delay_weather_filename, 'rb'))
delay_nas_lin_reg_model = pickle.load(open(delay_nas_filename, 'rb'))
delay_security_lin_reg_model = pickle.load(open(delay_security_filename, 'rb'))
delay_late_aircraft_lin_reg_model = pickle.load(open(delay_late_aircraft_filename, 'rb'))
cancel_lin_reg_model = pickle.load(open(cancel_filename, 'rb'))


def pred():
    st.header("Flight Delay and Cancellation Prediction")
    st.markdown("Fill in the information about your flight below and we will predict how long the flight may be \
         delayed for (or arrive early) and the probability of the flight being cancelled.")
    with st.form("flight_details"):
        valid_input = True
        c1, c2 = st.columns(2)
        with c1:
            airline = st.selectbox("Airline",
                                    options=[key + ' : ' + value for key, value in airline_name.items()]).split(" : ")[0]
            date = st.date_input("Departure Date", value = datetime.date.today(), min_value = datetime.datetime(2021, 1, 1), max_value = datetime.datetime(2023, 12, 30))
            dpt_airport = st.selectbox("From Airport",
                                    options=airports, index = 236)
            dpt_time = int(st.time_input('Expected Departure Time', datetime.time(13,15)).strftime("%-H%M"))       
        with c2:
            flight_num = st.text_input('Flight Number', '1111')
            arr_date = st.date_input("Arrival Date", value = datetime.date.today(), min_value = datetime.datetime(2021, 1, 1), max_value = datetime.datetime(2023, 12, 30))
            arv_airport = st.selectbox("To Airport",
                                    options=airports, index = 39)
            arv_time = int(st.time_input('Expected Arrival Time', datetime.time(15,00)).strftime("%-H%M"))

        if not flight_num.isnumeric() or int(flight_num) < 0 or int(flight_num) > 9999:
            st.write('Please enter a valid flight number between 1 and 9999.')
            valid_input = False
        elif dpt_airport == arv_airport:
            st.write('Please select different departure and arrival airport.')
            valid_input = False
        else:
            valid_input = True

        month = date.month
        day = date.day
        weekday = date.weekday() + 1

        submitted = st.form_submit_button("Predict!")

    if valid_input and submitted:
        dummy_data = [[month, day, weekday, airline, int(flight_num), dpt_airport, arv_airport, dpt_time, arv_time]]
        dummy_df = pd.DataFrame(dummy_data, columns=['MONTH', 'DAY_OF_MONTH', 
                'DAY_OF_WEEK', 'OP_UNIQUE_CARRIER', 'OP_CARRIER_FL_NUM', 
                'ORIGIN', 'DEST', 'CRS_DEP_TIME', 
                'CRS_ARR_TIME'])
        input = transformer.transform(dummy_df)
        delay_carrier_pred = delay_carrier_lin_reg_model.predict(input)[0]
        delay_weather_pred = delay_weather_lin_reg_model.predict(input)[0]
        delay_nas_pred = delay_nas_lin_reg_model.predict(input)[0]
        delay_security_pred = delay_security_lin_reg_model.predict(input)[0]
        delay_late_aircraft_pred = delay_late_aircraft_lin_reg_model.predict(input)[0]


        cancel_pred = cancel_lin_reg_model.predict_proba(input)[0][1] * 100
        total_delay = delay_weather_pred + delay_carrier_pred + delay_nas_pred + delay_security_pred + delay_late_aircraft_pred


        m1, m2, = st.columns(2)
        with m1:
            st.metric(label=f"Your flight may be late for", value=f"{round(total_delay)} minutes")
            st.metric(label=f"Your flight may be late due to weather for", value=f"{round(delay_weather_pred)} minutes")
            st.metric(label=f"Your flight may be late due to nas for", value=f"{round(delay_nas_pred)} minutes")
            st.metric(label=f"Your flight may be late due to late aircraft for", value=f"{round(delay_late_aircraft_pred)} minutes")
        with m2:
            st.metric(label=f"The probability of your flight being cancelled is", value=f"{round(cancel_pred)}%")
            st.metric(label=f"Your flight may be late due to carrier for", value=f"{round(delay_carrier_pred)} minutes")
            st.metric(label=f"Your flight may be late due to security for", value=f"{round(delay_security_pred)} minutes")

pred()