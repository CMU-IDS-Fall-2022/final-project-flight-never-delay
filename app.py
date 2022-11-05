import streamlit as st
from introduction import intro
from visualization import vis_airline_company, vis_flight_time, vis_flight_distance, vis_flight_destination
from prediction import model, predict

if __name__ == '__main__':
    st.sidebar.header("Introduction")
    button1 = st.sidebar.button("Flight delay problem")
    st.sidebar.header("Visualization")
    st.sidebar.write("How are these factors related to flight delay?")
    button2 = st.sidebar.button("Airline company")
    button3 = st.sidebar.button("Flight time")
    button4 = st.sidebar.button("Flight distance")
    button5 = st.sidebar.button("Flight destination")
    st.sidebar.header("Prediction")
    button6 = st.sidebar.button("Model training")
    button7 = st.sidebar.button("Let's predict for a flight!")
    if button1:
        intro()
    elif button2:
        vis_airline_company()
    elif button3:
        vis_flight_time()
    elif button4:
        vis_flight_distance()
    elif button5:
        vis_flight_destination()
    elif button6:
        model()
    elif button7:
        predict()
    else:
        intro()
