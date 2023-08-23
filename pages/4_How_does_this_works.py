import streamlit as st
import fastf1 as ff1
import fastf1.plotting
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import requests
import json
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="F1 Data Analisis Web",
    page_icon="assets/f1.png"
)

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/F1_logo.svg/256px-F1_logo.svg.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
                margin-left: 0px;
                margin-right: 10px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "F1 Data Analysis";
                margin-left: 10px;
                margin-top: 10px;
                font-size: 20px;
                position: relative;
                top: 80px;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()

st.markdown(
"""
<style>
.css-nps9tx, .e1m3hlzs0, .css-1p0bytv, .e1m3hlzs1 {
   visibility: collapse;
   height: 0px;
}
</style>
""",
unsafe_allow_html=True
)
st.markdown(
    f"""
    <div style="
        background-color: red;
        padding: 10px;
        border-radius: 10px;
    ">
        <h1 style="color: white;">How does this works?</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.write('')
st.write('')
st.write("""
        
        **F1 Data Analysis** is a tool to check the last results statistics of the Formula 1 sessions as far as the data 
        is available. This includes telemetry, track status, weather, tyre conditions, etc... to get a deep dive 
        in the details of F1. 

        **Quick Guide:**

        * **Telemetry:** Head to head, you are able to compare not only lap times, but driving styles between 
        drivers. Who breaks later? Who likes to drive at high RPM? Who pushes the throttle in every corner? 
        This section gives you also a comparison between track conditions and weather, maybe that unexpected 
        pole position can be explained by comparing wind data or rainfall, among other variables, in Formula 1 
        everything counts. This in depth analysis can be done in every session and every lap of the grand prix as 
        long as the data is available. 

        * **Lap History:** You can compare stint performance between drivers in every session of the grand prix. 
        Tyre behaviour is complex, and drivers could be quicker or slower even with the same tyres. This section 
        is pretty interesting in practices, in which you could see the same driver improving his performance
        with the same tyre compound because of changes in the car setup. 

        * **Race History:** This section is focused in the race session of the grand prix. Displays the position 
        history of the drivers and also how consistent they were on their time laps. This depicts the pace managment 
        of the drivers and also the difficulties of being in high traffic. Tyres strategies are also 
        available to analyze, since it is the key for many races, risky tyre strategies could bring great rewards
        or terrible consequences! Here you can compare how good are some drivers in tyre managment.        
         
         
        This web app was built using python(libraries: streamlit, plotly, pandas, fastf1). [Fastf1](https://docs.fastf1.dev/) 
        is used to access to F1 official data. This is the first version, so it is expected to have some bugs that will be 
        fixed in the future.
         
         **This web app is still under development.**""")

st.write("""**Any ideas or comments:**""")
st.write("""Christian Álvarez""")

'''
    [![Repo](https://badgen.net/badge/icon/Linkedin?icon=in&label)](http://www.linkedin.com/in/christian-adri%C3%A1n-%C3%A1lvarez-b%C3%A1ez-264a8aa4)      [![Repo](https://badgen.net/badge/icon/Email/yellow?icon=in&label)](mailto:christian.alvarez813@gmail.com) [![Repo](https://badgen.net/badge/icon/Portfolio/orange?icon=in&label)](https://christianalvarezbaez.github.io/) [![Repo](https://badgen.net/badge/icon/ResearchGate/cyan?icon=in&label)](https://www.researchgate.net/profile/Christian-Alvarez-Baez)

'''
st.markdown("<br>",unsafe_allow_html=True)



st.write("""
        Disclaimer: This is an unofficial project and is not associated in any way with the Formula 1 companies. 
        F1, FORMULA ONE, FORMULA 1, FIA FORMULA ONE WORLD CHAMPIONSHIP, GRAND PRIX and related marks are trade 
        marks of Formula One Licensing B.V.

""")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


animation = load_lottiefile('assets/f1.json')

sidebar = st.sidebar

with sidebar:
    st.success("Select a page above.")
    st.write('')
    st.write('')
    st.write('')
    st_lottie(animation)
