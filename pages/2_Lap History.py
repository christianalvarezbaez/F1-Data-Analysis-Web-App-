import streamlit as st
import fastf1 as ff1
import fastf1.plotting
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="F1 Data Analisis Web",
    page_icon="assets/f1.png"
)

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
        <h1 style="color: white;">Lap Times History</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.write('')

with st.expander('How to read this data?'):
   st.write("""
**Lap Time and Compound History** gives the perspective of how tyres influence on lap time. A 
hard compound might be slower than a medium compound. However a Redbull might be 2 second quicker
while a Ferrari could be only 1 second quicker after changing from hard to soft compound. This means
that Ferrari might need a different strategy than Redbull. And this is why this kind of analysis
in practice sessions are crucial for delivering a good strategy on the race. 

""")
st.sidebar.success("Select a page above.")

if 'showplots' not in st.session_state:
    st.session_state.showplots = True 

def Notshowplots():
    st.session_state.showplots = False




race = st.session_state.get_session

try:
    laps = race.laps
except: 
   st.warning('No data for this selection')


# -----------SideBar
st.sidebar.subheader('Year')
years = [i for i in range(2018,2023+1)]
year = st.sidebar.selectbox('Select year',(years),st.session_state.yearid, on_change = Notshowplots)
st.session_state.year = year
st.session_state.yearid = years.index(year)


event_schedule = ff1.get_event_schedule(year)
gps = list(pd.DataFrame(event_schedule['Country'])['Country'])
numbers = [i for i in range(1,len(gps)+1)]
merged_list = [str(num) + ' ' + word for num, word in zip(numbers, gps)]
st.sidebar.subheader('Grand Prix')
gp = st.sidebar.selectbox('Select grand prix', range(len(merged_list)),index = st.session_state.gpindex, format_func=lambda x: merged_list[x],on_change = Notshowplots)

st.session_state.gp = merged_list[gp]
st.session_state.gpindex = gp


st.sidebar.subheader('Session')
sessions = ['Race','Qualifying','Practice 1', 'Practice 2', 'Practice 3']
sessionsid = ['R','Q','FP1','FP2','FP3']
session_ = st.sidebar.selectbox('Select session', (sessions),index = st.session_state.sessionsid, on_change = Notshowplots)
if session_ == 'Race':
    session = 'R'
elif session_ == 'Qualifying':
    session = 'Q'
elif session_ == 'Practice 1':
    session = 'FP1'
elif session_ == 'Practice 2':
    session = 'FP2'
elif session_ == 'Practice 3':
    session = 'FP3'

st.session_state.sessions = session
st.session_state.sessionsid = sessionsid.index(session)

session = st.session_state.sessions
gp = st.session_state.gp[2:]
year = st.session_state.year

# Saving race session---------
if 'get_session' not in st.session_state:
    race = ff1.get_session(year, gp, session)
    race.load()
    st.session_state.get_session = race
    laps = race.laps

def get_session():
    race = ff1.get_session(year, gp, session)
    race.load()
    st.session_state.get_session = race
    st.session_state.showplots = True 

   
race = st.session_state.get_session
try:
  laps = race.laps
except: 
  st.warning('No data for this selection, choose another session or grand prix')
st.sidebar.button('Get new data!',on_click = get_session, help = 'If you modify any parameter above, click this!')

drivers = list(race.results.FullName)
drivers_ = drivers[:]
drivers_.append('None')
drivers_abb = list(race.results.Abbreviation)
drivers_abb.append('None')

st.sidebar.subheader('First Driver')
driver1 = st.sidebar.selectbox('Select First Driver', (drivers), key=3, index = 0)
st.session_state.driver1 = driver1
st.session_state.driver1id = drivers.index(driver1)


st.sidebar.subheader('Second Driver')
driver2 = st.sidebar.selectbox('Select Second Driver', (drivers_),key=4,index = 1)
st.session_state.driver2 = driver2
st.session_state.driver2id = drivers.index(driver2)

drivers_dict = dict(zip(drivers, drivers_abb))

driver1_FN = driver1
driver2_FN = driver2
driver1 = drivers_dict[driver1]
driver2 = drivers_dict[driver2]

#PLOTS -----------
driver_laps = race.laps.pick_driver(driver1).pick_quicklaps().reset_index()
driver_laps2 = race.laps.pick_driver(driver2).pick_quicklaps().reset_index()

fig = go.Figure()

for compound in driver_laps["Compound"].unique():
    df = driver_laps[driver_laps["Compound"] == compound]

    fig.add_trace(go.Scatter(x=df["LapNumber"], y=df['LapTime'].dt.total_seconds(),
                             mode="markers",
                             name=f"{compound} {driver1}",
                             marker_size = 10,
                             marker_color=ff1.plotting.COMPOUND_COLORS[compound],
                             marker_line_width=2,
                             text = df["Compound"],
                             hovertemplate =
                            f'<br><b> {driver1}</b></br>' +
                            '<b>Lap Time (s)</b>: %{y}'+
                            '<br><b>Compound %{text}</b><extra><br>' + df['Compound'] +'</extra>'))
if len(driver_laps2) > 1:
   for compound in driver_laps2["Compound"].unique():
       df2 = driver_laps2[driver_laps2["Compound"] == compound]
       fig.add_trace(go.Scatter(x=df2["LapNumber"], y=df2['LapTime'].dt.total_seconds(),
                             mode="markers",
                             name=f"{compound} {driver2}",
                             marker_size = 10,
                             marker_color=ff1.plotting.COMPOUND_COLORS[compound],
                             marker_line_width=2,
                             marker_symbol = 'cross',
                            text = df["Compound"],
                             hovertemplate =
                            f'<br><b> {driver2}</b></br>' +
                            '<b>Lap Time (s)</b>: %{y}'+
                            '<br><b>Compound %{text}</b><extra><br>' + df['Compound'] +'</extra>'))


if len(driver2) > 0:
    title=f"""{driver1_FN} vs {driver2_FN} Laptimes in the {st.session_state.session_name} in the {st.session_state.gp[2:]} Grand Prix {st.session_state.year}"""
else:
    title=f"""{driver1_FN} vs {driver2_FN} Laptimes in the {st.session_state.session_name} in the {st.session_state.gp[2:]} Grand Prix {st.session_state.gp}"""

st.subheader(title)

fig.update_layout(title = title,
                  xaxis_title="Lap Number",
                  yaxis_title="Lap Time (s)",
                  template = 'plotly_dark',
                  width = 600,
                  legend=dict(
        title='Compound - Driver',
        font=dict(
            size=14,
        )))
fig.update_xaxes(titlefont_size = 16)
fig.update_yaxes(titlefont_size = 16)

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