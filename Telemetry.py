import streamlit as st
import fastf1 as ff1
import fastf1.plotting
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="F1 Data Analisis Web",
    page_icon="/home/chris/PythonProjects/F1/assets/f1.png"
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
        <h1 style="color: white;">Telemetry - Head to head</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write('')

with st.expander('How to read this data?'):
   st.write("""
**Telemetry** is one of the most important data for F1 drivers and engineers. It displays the drivers 
talent, their style and strategies. Some might break meters later than others and push the throttle sooner 
than others or driving at high RPM. Comparing two drivers would show not only their own driving style, but
also how much of them they have to put on a lap. For example, while a driver in a good car does not have to 
be pushing every meter of the lap to get a good time, you might find other drivers on slower cars giving 
everything they have, breaking later than others and pushing earlier on every corner exit just to get a 
decent laptime.

""")


if 'showplots' not in st.session_state:
    st.session_state.showplots = True 

if 'change' not in st.session_state:
    st.session_state.change = False

def Notshowplots():
    st.session_state.showplots = False
    st.session_state.change = True



st.sidebar.success("Select a page above.")

st.sidebar.subheader('Year')
years = [i for i in range(2018,2023+1)]

if 'year' not in st.session_state:
    st.session_state.year = 2023

if 'yearid' not in st.session_state:
    st.session_state.yearid = len(years)-1


year = st.sidebar.selectbox('Select year',(years),len(years)-1, on_change = Notshowplots)
st.session_state.year = year
st.session_state.yearid = years.index(year)

#add flags

event_schedule = ff1.get_event_schedule(year)
gps = list(pd.DataFrame(event_schedule['Country'])['Country'])
numbers = [i for i in range(1,len(gps)+1)]
merged_list = [str(num) + ' ' + word for num, word in zip(numbers, gps)]
st.sidebar.subheader('Grand Prix')

if 'gp' not in st.session_state: 
   st.session_state.gp = 'value'
if 'gpindex' not in st.session_state: 
   st.session_state.gpindex = 11



gp = st.sidebar.selectbox('Select grand prix', range(len(merged_list)),index = 11, format_func=lambda x: merged_list[x], on_change = Notshowplots)

st.session_state.gp = merged_list[gp]
st.session_state.gpindex = gp

st.sidebar.subheader('Session')
sessions = ['Race','Qualifying','Practice 1', 'Practice 2', 'Practice 3']
sessionsid = ['R','Q','FP1','FP2','FP3']
if 'sessions' not in st.session_state:
    st.session_state.sessions = 'Q'

if 'sessionsid' not in st.session_state:
    st.session_state.sessionsid = 1

if 'session_name' not in st.session_state:
    st.session_state.session_name = 'Qualifying'

session = st.sidebar.selectbox('Select session', (sessions),index = 1, on_change = Notshowplots)
st.session_state.session_name = session

if session == 'Race':
    session = 'R'
elif session == 'Qualifying':
    session = 'Q'
elif session == 'Practice 1':
    session = 'FP1'
elif session == 'Practice 2':
    session = 'FP2'
elif session == 'Practice 3':
    session = 'FP3'

st.session_state.sessions = session
st.session_state.sessionsid = sessionsid.index(session)



gp = st.session_state.gp[2:]
session = st.session_state.sessions

# Saving race session---------
def get_session():
    race = ff1.get_session(year, gp, session)
    race.load()
    st.session_state.get_session = race
    st.session_state.showplots = True 


if 'get_session' not in st.session_state:
    race = ff1.get_session(year, gp, session)
    race.load()
    st.session_state.get_session = race
    laps = race.laps



   
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

if 'driver1' not in st.session_state:
    st.session_state.driver1 = 'Max Verstappen'
if 'driver1id' not in st.session_state:
    st.session_state.driver1id = 0
if 'driver2' not in st.session_state:
    st.session_state.driver2 = 'Lewis Hamilton'
if 'driver2id' not in st.session_state:
    st.session_state.driver2id = 1

st.sidebar.subheader('Drivers')
driver1 = st.sidebar.selectbox('Select First Driver', (drivers), key=1, index = 0)
st.session_state.driver1 = driver1
st.session_state.driver1id = drivers.index(driver1)
driver2 = st.sidebar.selectbox('Select Second Driver', (drivers_),key=2,index = 1)
st.session_state.driver2 = driver2
st.session_state.driver2id = drivers.index(driver2)


drivers_dict = dict(zip(drivers, drivers_abb))

#Saving drivers sessions--------------
driver1_FN = driver1
driver2_FN = driver2
driver1 = drivers_dict[driver1]
driver2 = drivers_dict[driver2]






laps1_options = [int(i) for i in laps.pick_driver(driver1).LapNumber.unique()]
laps2_options = [int(i) for i in laps.pick_driver(driver2).LapNumber.unique()]
laps1_options.insert(0,'quickest lap')
laps2_options.insert(0,'quickest lap')

st.sidebar.subheader('Laps')
lap1 = st.sidebar.selectbox('Select First Driver Lap', laps1_options, key=3)

lap2 = st.sidebar.selectbox('Select Second Driver Lap', laps2_options,key=4)








#Some functions

def break_plot(fig,lap,drivername,driver1or2):
  """ Takes the driver lap array, wether is the driver 1 or 2, calculates start and ending
  and plots for the driver"""
  if driver1or2 == 1:
    start = 15
    end = 45
    y = np.full(99,end)
    y = np.append(start, y)
    y = np.append(y, start)
    y = np.append(y, start)
  else:
    start = 65
    end = 95
    y = np.full(99,end)
    y = np.append(start, y)
    y = np.append(y, start)
    y = np.append(y, start)

  brake = list(lap['Brake'])
  distance = list(lap['Distance'])
  start = []
  end = []

  for i in range(0,len(brake)):
    if i > 0:
      if (brake[i] == True) and (brake[i-1] == False):
          start.append(distance[i])
      if (i != (len(brake)-1)) and (brake [i] == True) and (brake[i+1] == False):
          end.append(distance[i])
      if (i == len(brake)-1) and (brake [i] == True):
          end.append(distance[i])
  for i in range(0,len(start)):
    x = np.linspace(start[i], end[i], num=100)
    x = np.append(start[i], x)
    x = np.append(x, start[i])
    fig.add_trace(
          go.Scatter(
              x=x,
              y=y,
              fill="toself",
              mode='lines',
              name=f'Breaking {drivername}',
              line_color='red',
              opacity=0.5,
              showlegend = False
          ),row = 2,col = 1)
    if driver1or2 == 1:
      fig.add_annotation(
      showarrow=False,
      text=f"Brake <br> {drivername}",
      font=dict(size=10, color = 'red'),
      xref='paper',
      x=1.05,
      yref='paper',
      y=0.56
      )
    else:
      fig.add_annotation(
      showarrow=False,
      text=f"Brake <br> {drivername}",
      font=dict(size=10, color = 'red'),
      xref='paper',
      x=1.05,
      yref='paper',
      y=0.74
      )
  return brake, fig

def get_laptime(driver_df,lap):
  if lap == 'quickest lap':
    time = driver_df.LapTime[driver_df['LapTime'] == driver_df['LapTime'].min()].dt.total_seconds()
  else:
    time = driver_df.LapTime[driver_df.LapNumber == lap].dt.total_seconds()
  if np.asarray(np.isnan(time))[0]:
    time = 'No time for this lap'
  else:
    minutes = int(float(time/60))
    seconds = round(float(time-(60*minutes)),3)
    time1 = f'{minutes}:{seconds}'
  return time, time1

def tyre(driver_df,lap):
  if lap == 'quickest lap':
    compound = driver_df.sort_values(by = 'LapTime').Compound.iloc[0]
    life = driver_1.sort_values(by = 'LapTime').TyreLife.iloc[0]
    return compound, life
  else:
    compound = driver_df.Compound[driver_df.LapNumber == lap]
    life = driver_df.TyreLife[driver_df.LapNumber == lap]
    return np.asarray(compound)[0],np.asarray(life)[0]

# Track status
def trackstatus(driver_df,lap):
  status_dict = {
    1: 'Track clear',
    2: 'Yellow flag',
    3: 'Unknown',
    4: 'Safety Car',
    5: 'Red Flag',
    6: 'Virtual Safety Car deployed',
    7: 'Virtual Safety Car ending'
  }
  if lap == 'quickest lap':
     trackstatus = driver_df.sort_values(by = 'LapTime').TrackStatus.iloc[0]
     trackstatus = status_dict[int(np.asarray(trackstatus))]
     return trackstatus
  else:
     trackstatus = (driver_df.TrackStatus[driver_df.LapNumber == lap])
     trackstatus = status_dict[int(np.asarray(trackstatus))]
     return trackstatus

 #Pit Lap Status

def pitlaps(drivername,driver_df,lap):
  if lap == 'quickest lap':
    return f'No pitting this lap for {drivername}'
  elif str(np.asarray(driver_df.PitInTime[driver_df.LapNumber == lap])[0]) != 'NaT':
    return f'{drivername} was on Pit in Lap'
  elif str(np.asarray(driver_df.PitOutTime[driver_df.LapNumber == lap])[0]) != 'NaT':
    return f'{drivername} was on Pit in Lap'
  else:
    return f'No pitting this lap for {drivername}'

#Plot-------------------------------------------------------------------------------------------------------- 

if driver2 != 'None':

  driver_1 = laps.pick_driver(driver1)
  driver_2 = laps.pick_driver(driver2)

  if lap1 == 'quickest lap':
    fast_d1 = laps.pick_driver(driver1).pick_fastest().get_car_data().add_distance()
    weather_d1 = laps.pick_driver(driver1).pick_fastest().get_weather_data()

  else:
    fast_d1 = driver_1.loc[driver_1.LapNumber==lap1].get_car_data().add_distance()
    weather_d1 = driver_1.loc[driver_1.LapNumber==lap1].get_weather_data()

  if lap2 == 'quickest lap':
    fast_d2 = laps.pick_driver(driver2).pick_fastest().get_car_data().add_distance()
    weather_d2 = laps.pick_driver(driver2).pick_fastest().get_weather_data()

  else:
    fast_d2 = driver_2.loc[driver_2.LapNumber==lap2].get_car_data().add_distance()
    weather_d2 = driver_2.loc[driver_2.LapNumber==lap2].get_weather_data()

  if lap1 != 'quickest lap' and lap2 != 'quickest lap':
      title = f'{driver1_FN} on lap {lap1} vs {driver2_FN} on lap {lap2}'
  if lap1 == 'quickest lap' and lap2 != 'quickest lap':
      title = f'{driver1_FN} on {lap1} vs {driver2_FN} on lap {lap2}'
  if lap1 != 'quickest lap' and lap2 == 'quickest lap':
      title = f'{driver1_FN} on lap {lap1} vs {driver2_FN} on {lap2}'
  if lap1 == 'quickest lap' and lap2 == 'quickest lap':
      title = f'{driver1_FN} on {lap1} vs {driver2_FN} on {lap2}'

  st.subheader(title)

  #plots--------------------------------------------------------------------------------------------------
  try:
      color1 = ff1.plotting.driver_color(driver1)
  except KeyError:
      color1 = 'white'
  try:
    color2 = ff1.plotting.driver_color(driver2)
  except KeyError:
    color2 = 'yellow'

  fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                      vertical_spacing=0.05, x_title = 'Distance (m)', specs=[[{"secondary_y": True}], [{"secondary_y": False}],
                            [{"secondary_y": True}], [{"secondary_y": True}]])

  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.Speed,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Speed (km/hr)</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=1,col=1)
  fig.add_trace(go.Scatter(x=fast_d2.Distance, y=fast_d2.Speed,
                      mode='lines',
                      name=driver2,
                      line=dict(color=color2, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver2}</b></br>' +
                              '<b>Speed (km/hr)</b>: %{y} </br><extra><br>' + driver2 +'</extra>'),row=1,col=1)
  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.Throttle,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Throttle (%)</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=2,col=1)

  fig.add_trace(go.Scatter(x=fast_d2.Distance, y=fast_d2.Throttle,
                      mode='lines',
                      name=driver2,
                      line=dict(color=color2, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver2}</b></br>' +
                              '<b>Throttle (%)</b>: %{y} </br><extra><br>' + driver2 +'</extra>'),row=2,col=1)
  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.nGear,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Gear</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=3,col=1)
  fig.add_trace(go.Scatter(x=fast_d2.Distance, y=fast_d2.nGear,
                      mode='lines',
                      name=driver2,
                      line=dict(color=color2, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver2}</b></br>' +
                              '<b>Gear</b>: %{y} </br><extra><br>' + driver2 +'</extra>'),row=3,col=1)
  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.RPM,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Gear</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=4,col=1)
  fig.add_trace(go.Scatter(x=fast_d2.Distance, y=fast_d2.RPM,
                      mode='lines',
                      name=driver2,
                      line=dict(color=color2, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver2}</b></br>' +
                              '<b>Gear</b>: %{y} </br><extra><br>' + driver2 +'</extra>'),row=4,col=1)

  break_1, fig = break_plot(fig,fast_d1,driver1,1)
  break_2, fig = break_plot(fig,fast_d2,driver2,2)


  fig.update_layout(hovermode="x unified", template = 'plotly_dark', width = 940, height=940, margin=dict(l=10, r=10, t=20, b=10))
  fig.update_yaxes(title_text="<b>Speed (km/hr)</b>",row=1,col=1)
  fig.update_yaxes(title_text="<b>Throttle (%)</b>",row=2,col=1)
  fig.update_yaxes(title_text="<b>Gear</b>",row=3,col=1)
  fig.update_yaxes(title_text="<b>RPM</b>",row=4,col=1)
  fig.update_traces(showlegend=False)
  fig.update_traces(showlegend=True,row=1,col=1)

  seconds1,time_1 = get_laptime(driver_1,lap1)
  seconds2,time_2 = get_laptime(driver_2,lap2)
  delta1 = float(seconds1) - float(seconds2)
  delta2 = float(seconds2) - float(seconds1)
  #Metrics
  col1, col2 = st.columns(2)
  col1.markdown("""
  <style>
  div[data-testid="metric-container"] {
     background-color: rgba(28, 131, 225, 0.1);
     border: 1px solid rgba(28, 131, 225, 0.1);
     padding: 5% 5% 5% 10%;
     border-radius: 5px;
     color: rgb(30, 103, 119);
     overflow-wrap: break-word;
    }

  /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
      overflow-wrap: break-word;
      white-space: break-spaces;
      color: white;
    }
  </style>
  """, unsafe_allow_html=True)
  col2.markdown("""
  <style>
  div[data-testid="metric-container"] {
     background-color: rgba(28, 131, 225, 0.1);
     border: 1px solid rgba(28, 131, 225, 0.1);
     padding: 5% 5% 5% 10%;
     border-radius: 5px;
     color: rgb(30, 103, 119);
     overflow-wrap: break-word;
   }

  /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
      overflow-wrap: break-word;
      white-space: break-spaces;
      color: white;
    }
  </style>
  """, unsafe_allow_html=True)
  col1.metric(label = driver1_FN, value = time_1, delta = round(delta1,3),delta_color = 'inverse')
  col2.metric(label = driver2_FN, value = time_2, delta = round(delta2,3),delta_color = 'inverse')


  #Plot
  if st.session_state.showplots == True:
    st.plotly_chart(fig)  
  else: 
    st.warning('Click the button on the sidebar to get new data')
  #Stats

  percentage_break_1 = sum(1 for x in break_1 if x) / len(break_1) * 100
  percentage_break_2 = sum(1 for x in break_2 if x) / len(break_2) * 100

  mean_speed_1 = round(fast_d1.Speed.mean(),2)
  mean_speed_2 = round(fast_d2.Speed.mean(),2)

  mean_RPM_1 = round(fast_d1.RPM.mean(),2)
  mean_RPM_2 = round(fast_d2.RPM.mean(),2)

  throttle_1 = [True if x > 0 else False for x in fast_d1.Throttle]
  throttle_1 = round(sum(1 for x in throttle_1 if x) / len(throttle_1) * 100,2)
  throttle_2 = [True if x > 0 else False for x in fast_d2.Throttle]
  throttle_2 = round(sum(1 for x in throttle_2 if x) / len(throttle_2) * 100,2)

  with st.expander('Quick Stats'):
    st.write(f'While {driver1} brakes', round(percentage_break_1,2), f'% of the lap, {driver2} brakes ', round(percentage_break_2,2),' %')
    st.write(f'While {driver1} pushes the throttle during', throttle_1, f'% of the lap, {driver2} does it', throttle_2,' %')
    st.write(f'{driver1} mean speed: ',mean_speed_1,f' km/hr and {driver2} mean speed: ',mean_speed_2, 'km/hr during this lap')
    st.write(f'{driver1} mean RPM: ',mean_RPM_1,f' and {driver2} mean rpm: ',mean_RPM_2, ' during this lap')
    st.write(f"{driver1} laptime",time_1,f"{driver2} laptime",time_2)

  # Tyre conditions
  compound_1, life_1 = tyre(driver_1,lap1)
  compound_2, life_2 = tyre(driver_2,lap2)
  with st.expander('Tyre Conditions'):
    st.write(f"{driver1} compound: ",compound_1,'with a life of ',life_1,' laps' )
    st.write(f"{driver2} compound: ",compound_2,'with a life of ',life_2,' laps' )
  
  #Track Conditions
  trackstatus1 = trackstatus(driver_1,lap1)
  trackstatus2 = trackstatus(driver_2,lap2)
    # Pit Lap?
  pit1 = pitlaps(driver1,driver_1,lap1)
  pit2 = pitlaps(driver2,driver_2,lap2)

  with st.expander('Track Conditions'):
   st.write(f'Track Status for {driver1} lap: ', trackstatus1)
   st.write(f'Track Status for {driver2} lap: ', trackstatus2)
   st.write(pit1)
   st.write(pit2)

  #Weather data
  weather_d1 = pd.DataFrame(weather_d1.T)
  weather_d1.columns = [driver1]

  weather_d2 = pd.DataFrame(weather_d2.T)
  weather_d2.columns = [driver2]

  weather = weather_d1
  weather[driver2] = weather_d2[driver2]
  weather.drop(index = ['Time'],inplace = True)
  weather.index.name = 'Variable'

  table = go.Figure(data=[go.Table(
      header=dict(values=['<b>Variables<b>', f'<b>{driver1}<b>',f'<b>{driver2}<b>'],
                  fill_color='red',
                  align='left',
                  font=dict(color='white', size=16)),
      cells=dict(values=[weather.index, # 1st column
                        weather[driver1],weather[driver2]], # 2nd column
               # fill_color='lightcyan',
                align='left',
                font=dict(color = 'white',size=14), height= 30))
  ])

  table.update_layout(width=350, height=350, margin=dict(l=20, r=30, t=10, b=10), template = 'plotly_dark')
  with st.expander('Weather Conditions'):
    st.plotly_chart(table,use_container_width=True)  
else:
  driver_1 = laps.pick_driver(driver1)

  if lap1 == 'quickest lap':
    fast_d1 = laps.pick_driver(driver1).pick_fastest().get_car_data().add_distance()
    weather_d1 = laps.pick_driver(driver1).pick_fastest().get_weather_data()

  else:
    fast_d1 = driver_1.loc[driver_1.LapNumber==lap1].get_car_data().add_distance()
    weather_d1 = driver_1.loc[driver_1.LapNumber==lap1].get_weather_data()

  if lap1 != 'quickest lap':
      title = f'{driver1_FN} on lap {lap1}'
  else:
      title = f'{driver1_FN} on {lap1}'
  st.subheader(title)  

  #plots-----
  try:
    color1 = ff1.plotting.driver_color(driver1)
  except KeyError:
    color1 = 'white'

  fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                      vertical_spacing=0.05, x_title = 'Distance (m)', specs=[[{"secondary_y": True}], [{"secondary_y": False}],
                            [{"secondary_y": True}], [{"secondary_y": True}]])

  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.Speed,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Speed (km/hr)</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=1,col=1)
  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.Throttle,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Throttle (%)</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=2,col=1)
  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.nGear,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Gear</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=3,col=1)
  fig.add_trace(go.Scatter(x=fast_d1.Distance, y=fast_d1.RPM,
                      mode='lines',
                      name=driver1,
                      line=dict(color=color1, width=2),
                      hovertemplate =
                              f'<br><b>Driver: {driver1}</b></br>' +
                              '<b>Gear</b>: %{y} </br><extra><br>' + driver1 +'</extra>'),row=4,col=1)
  break_1, fig = break_plot(fig,fast_d1,driver1,1)


  fig.update_layout(hovermode="x unified", template = 'plotly_dark', width = 940, height=940, margin=dict(l=10, r=10, t=20, b=10))
  fig.update_yaxes(title_text="<b>Speed (km/hr)</b>",row=1,col=1)
  fig.update_yaxes(title_text="<b>Throttle (%)</b>",row=2,col=1)
  fig.update_yaxes(title_text="<b>Gear</b>",row=3,col=1)
  fig.update_yaxes(title_text="<b>RPM</b>",row=4,col=1)
  fig.update_traces(showlegend=False)
  fig.update_traces(showlegend=True,row=1,col=1)

  #Lap times 
  seconds1,time_1 = get_laptime(driver_1,lap1)

  col1, col2 = st.columns(2)
  col1.markdown("""
  <style>
  div[data-testid="metric-container"] {
     background-color: rgba(28, 131, 225, 0.1);
     border: 1px solid rgba(28, 131, 225, 0.1);
     padding: 5% 5% 5% 10%;
     border-radius: 5px;
     color: rgb(30, 103, 119);
     overflow-wrap: break-word;
    }

  /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
      overflow-wrap: break-word;
      white-space: break-spaces;
      color: white;
    }
  </style>
  """, unsafe_allow_html=True)
  col1.metric(label = driver1_FN, value = time_1)

  if st.session_state.showplots == True:
    st.plotly_chart(fig)  
  else: 
    st.warning('Click the button on the sidebar to get new data')
  #Stats
  
  percentage_break_1 = sum(1 for x in break_1 if x) / len(break_1) * 100
  mean_speed_1 = round(fast_d1.Speed.mean(),2)
  mean_RPM_1 = round(fast_d1.RPM.mean(),2)
  throttle_1 = [True if x > 0 else False for x in fast_d1.Throttle]
  throttle_1 = round(sum(1 for x in throttle_1 if x) / len(throttle_1) * 100,2)
  time_1 = get_laptime(driver_1,lap1)

  with st.expander('Quick Stats'):
    st.write(f'{driver1} brakes ',round(percentage_break_1,2),' % of the lap')
    st.write(f'{driver1} pushes the throttle during', throttle_1,'% of the lap')
    st.write(f'{driver1} mean speed: ',mean_speed_1,f' km/hr during this lap')
    st.write(f'{driver1} mean RPM: ',mean_RPM_1, 'during this lap')
    st.write(f"{driver1} laptime",time_1)

  # Tyre conditions
  compound_1, life_1 = tyre(driver_1,lap1)
  with st.expander('Tyre Conditions'):
    st.write(f"{driver1} compound: ",compound_1,'with a life of ',life_1,' laps' )

  #Track Status
  trackstatus1 = trackstatus(driver_1,lap1)
  # Pit Lap?
  pit1 = pitlaps(driver1,driver_1,lap1)
  with st.expander('Track Conditions'):  
    st.write(f'Track Status for {driver1_FN} lap: ', trackstatus1)
    st.write(pit1)

  #Weather data
  weather_d1 = pd.DataFrame(weather_d1.T)
  weather_d1.columns = [driver1]
  weather = weather_d1
  weather.drop(index = ['Time'],inplace = True)
  weather.index.name = 'Variable'

  table = go.Figure(data=[go.Table(
      header=dict(values=['<b>Variables<b>', f'<b>{driver1}<b>'],
                  fill_color='red',
                  align='left',
                  font=dict(color='white', size=16)),
      cells=dict(values=[weather.index, # 1st column
                        weather[driver1]], # 2nd column
                align='left',
                font=dict(color = 'white',size=14)))
  ])

  table.update_layout(width=330, height=250, margin=dict(l=10, r=10, t=10, b=10), template = 'plotly_dark')
  with st.expander('Weather Conditions'):
    st.plotly_chart(table, use_container_width=True)  

footer = st.container()

with footer:
    st.write("Created by Christian Álvarez")
    '''
    [![Repo](https://badgen.net/badge/icon/Linkedin?icon=in&label)](http://www.linkedin.com/in/christian-adri%C3%A1n-%C3%A1lvarez-b%C3%A1ez-264a8aa4)      [![Repo](https://badgen.net/badge/icon/Email/yellow?icon=in&label)](mailto:christian.alvarez813@gmail.com) [![Repo](https://badgen.net/badge/icon/Portfolio/orange?icon=in&label)](https://christianalvarezbaez.github.io/) [![Repo](https://badgen.net/badge/icon/ResearchGate/cyan?icon=in&label)](https://www.researchgate.net/profile/Christian-Alvarez-Baez)

    '''