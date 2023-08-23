import streamlit as st
import fastf1 as ff1
import fastf1.plotting
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
        <h1 style="color: white;">Race History</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write('')

with st.expander('How to read this data?'):
   st.write("""
This section displays the position history of drivers during the race in a line chart. Violin plots depicts
the consistency and pace of the drivers. For every driver, their "violin" would be wider in the time range 
with the most laps made. Also you could see how some drivers chose to do some quick laps and then going back to
manage tyre life with slower laps. Finally, the tyre strategies chart display how different were the strategy 
for every driver. Some of them might overcut other drivers thanks to a great strategy and tyre managment skills,
but some other might got a really bad call.

""")


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


animation = load_lottiefile('assets/f1.json')


sidebar = st.sidebar

with sidebar:
    st.success("For a new session data, go back to Telemetry.")
    st.write('')
    st.write('')
    st.write('')
    st_lottie(animation)




session = 'R'

if 'gp' not in st.session_state:
    st.session_state.gp = '12 Hungary' 
if 'year' not in st.session_state:
    st.session_state.year = 2023
if 'sessions' not in st.session_state:
    st.session_state.sessions = 'R' 



gp = st.session_state.gp[2:]
year = st.session_state.year

# Loading race session---------
if 'get_session' not in st.session_state:
    try: 
        race = ff1.get_session(year, gp, session)
        race.load()
    except:
        st.warning('No data for this selection, choose another grand prix')

if st.session_state.sessions != session: 
    try:
        race = ff1.get_session(year,gp,session)
        race.load()
    except:
        st.warning('No data for this selection, choose another grand prix')
else: 
    try: 
        race = st.session_state.get_session
    except:
        st.warning('No data for this selection, choose another grand prix')
try:
    laps = race.laps
except: 
  st.warning('No data for this selection, choose another grand prix')

#Plotting position history

fig = go.Figure()
for drv in race.drivers:
    drv_laps = race.laps.pick_driver(drv)
    try:
        abb = drv_laps['Driver'].iloc[0]
    except:
        pass
    try: 
        color = fastf1.plotting.driver_color(abb)
    except:
        color = '#ffffff'
    fig.add_trace(go.Scatter(x=drv_laps['LapNumber'], y=drv_laps['Position'],
                    mode='lines',
                    name=abb,
                    line=dict(color=color, width=4),
                    hovertemplate =
                            f'<br><b>Driver: {abb}</b></br>' +
                            '<b>Position</b>: %{y} </br>' +
                            '<b>Lap</b>: %{x}<extra><br>' + abb +'</extra>'))
fig.update_layout(height = 300,margin=dict(l=10, r=10, t=10, b=10),
                  yaxis =dict(range=[len(race.drivers)+1,1]),
                    xaxis_title='Lap',
                   yaxis_title='Position',
                   template='plotly_dark',
                   legend=dict(
                    title= dict( 
                        text = 'Drivers (scroll)',
                        font = dict(size = 16)
                    ),
                    font=dict(
                    size=16,
                    )))
fig.update_xaxes(titlefont_size = 18)
fig.update_yaxes(titlefont_size = 18)
st.subheader(f'Positions history for the Race of {gp} Grand Prix {year}')

if st.session_state.showplots == True:
    st.plotly_chart(fig,use_container_width = True)
else: 
    st.warning('Click the button on the sidebar to get new data')

#Plotting point finishers 

def lap_distributions(drivers):
    driver_laps = race.laps.pick_drivers(drivers).pick_quicklaps()
    driver_laps = driver_laps.reset_index()
    finishing_order = [race.get_driver(i)["Abbreviation"] for i in drivers]

    driver_colors = {}
    for i in finishing_order:
        if i in fastf1.plotting.DRIVER_TRANSLATE:
            driver_colors[i] = fastf1.plotting.DRIVER_COLORS[fastf1.plotting.DRIVER_TRANSLATE[i]]
        else: 
            driver_colors[i] = ' #fffdff'


    driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

    fig = px.violin(driver_laps,
                    x="Driver",
                    y="LapTime(s)",
                    points='all',
                    box=True,
                    color="Driver",
                    violinmode='overlay',
                    color_discrete_map=driver_colors,
                    hover_data=driver_laps.columns,
                    template = "plotly_dark")

    fig.update_layout(title="Violin plot of Lap Times by Driver",
                    xaxis_title="Driver",
                    yaxis_title="Lap Time (s)",
                    legend=dict(
                    title='Drivers',
                    font=dict(
                    size=16,
                    )))
    fig.update_xaxes(titlefont_size = 16)
    fig.update_yaxes(titlefont_size = 16)

    return fig 
point_finishers = race.drivers[:10]
out_points = race.drivers[10:]
fig1 = lap_distributions(point_finishers)
fig2 = lap_distributions(out_points) 
st.subheader('Top Ten point finishers')
if st.session_state.showplots == True:
    st.plotly_chart(fig1,use_container_width = True)
    st.subheader('Out of points')
    st.plotly_chart(fig2,use_container_width = True)
else: 
    st.warning('Click the button on the sidebar to get new data')


#Strategies
stints = race.laps[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"])
stints = stints.count().reset_index()
stints = stints.rename(columns={"LapNumber": "StintLength"})
drivers = race.drivers
drivers = [race.get_driver(driver)["Abbreviation"] for driver in drivers]

fig = go.Figure()

for driver in drivers:
    driver_stints = stints.loc[stints["Driver"] == driver]

    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        # each row contains the compound name and stint length
        # we can use these information to draw horizontal bars
        fig.add_trace(go.Bar(
            y = [driver],
            x = [row["StintLength"]],
            orientation='h',
            name = row['Compound'],
             marker=dict(color = ff1.plotting.COMPOUND_COLORS[row["Compound"]]),
            hovertemplate = '<br><b>Driver</b>: %{y}</br>' +
                            '<b>Laps</b>: %{x}<extra><br>' + row['Compound'] +'</extra>'))
        fig.update_layout(barmode='stack',
                          height = 400,
                          margin=dict(l=10, r=10, t=10, b=10),
                          width = 400,
                          xaxis_title='Lap',
                          yaxis_title='Driver',
                          template = 'plotly_dark',
                          xaxis=dict(tickfont=dict(size=12)),
                          yaxis=dict(tickfont=dict(size=12))
                          )
        fig.update_xaxes(titlefont_size = 16)
        fig.update_yaxes(titlefont_size = 16)
                          
        previous_stint_end += row["StintLength"]
fig.update_traces(showlegend=False)
st.subheader('Tyre Strategies')
if st.session_state.showplots == True:
    st.plotly_chart(fig,use_container_width = True)
else: 
    st.warning('Click the button on the sidebar to get new data')

footer = st.container()

with footer:
    st.write("Created by Christian Álvarez")
    '''
    [![Repo](https://badgen.net/badge/icon/Linkedin?icon=in&label)](http://www.linkedin.com/in/christian-adri%C3%A1n-%C3%A1lvarez-b%C3%A1ez-264a8aa4)      [![Repo](https://badgen.net/badge/icon/Email/yellow?icon=in&label)](mailto:christian.alvarez813@gmail.com) [![Repo](https://badgen.net/badge/icon/Portfolio/orange?icon=in&label)](https://christianalvarezbaez.github.io/) [![Repo](https://badgen.net/badge/icon/ResearchGate/cyan?icon=in&label)](https://www.researchgate.net/profile/Christian-Alvarez-Baez)

    '''
