import streamlit as st
from introduction import intro
from visualization import vis
from prediction import pred

if __name__ == '__main__':
    nav = st.sidebar.radio("Navigation",
                     ("Introduction", "Visualization", "Prediction"))
    if nav == "Introduction":
        intro()
    elif nav == "Visualization":
        vis()
    else:
        pred()
