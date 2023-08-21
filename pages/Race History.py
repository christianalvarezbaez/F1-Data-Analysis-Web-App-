import streamlit as st
import fastf1 as ff1
import fastf1.plotting
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="F1 Ultimate Analisis Web",
    page_icon=":racing_car:",
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
        <h1 style="color: white;">Race History</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.success("Select a page above.")

session = 'R'
gp = st.session_state.gp[2:]
year = st.session_state.year

if 'showplots' not in st.session_state:
    st.session_state.showplots = True 

def Notshowplots():
    st.session_state.showplots = False

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
gp = st.sidebar.selectbox('Select grand prix', range(len(merged_list)),index = st.session_state.gpindex, format_func=lambda x: merged_list[x], on_change = Notshowplots)

st.session_state.gp = merged_list[gp]
st.session_state.gpindex = gp

gp = st.session_state.gp[2:]
year = st.session_state.year

# Saving race session---------
if 'reload' not in st.session_state: 
    st.session_state.reload = False


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

   
st.sidebar.button('Get new data!',on_click = get_session, help = 'If you modify any parameter above, click this!')

if st.session_state.sessions != session and st.session_state.reload is False: 
    race = ff1.get_session(year,gp,session)
    race.load()
    st.session_state.reload = True
elif st.session_state.sessions != session and st.session_state.change == True: 
    race = ff1.get_session(year,gp,session)
    race.load()
    st.session_state.change = False
else: 
    race = st.session_state.get_session
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


