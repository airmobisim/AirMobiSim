import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from pathlib import Path
from shapely.geometry import Point
from shapely.geometry import Point
import glob
import math
import re
import numpy as np
from os.path import abspath

from plotly.graph_objs import Layout


# loading position file

df_position = pd.DataFrame()
flight_time_considered = 0.0


# data being loaded to dataframe and variables to be passed to the simulator
def load_Data(path):
    global df_position
    global flight_time_considered

    folder_path = Path(path)
    csv_position = glob.glob(os.path.join(folder_path, "position*.csv"))
    csv_command = glob.glob(os.path.join(folder_path, "command*.csv"))

    # reading position data in dataframe
    df_position = pd.read_csv(
        csv_position[0],
        sep=r' ',
        skipinitialspace=True, engine='python')



    # reading comand data from command file to clean takeoff and landing data
    df_command = pd.read_csv(
        csv_command[0],
        sep=r'/t',
        skipinitialspace=True, engine='python')




    df_command.columns = ['timestamp_command']

    df_command = pd.DataFrame(df_command.timestamp_command.str.split(' ', 1).tolist(),
                              columns=['timestamp', 'command'])
    # all indexes for motion stop command
    idx = df_command.index[df_command['command'] == 'MotionStopCommand()'].tolist()

    # circular motion command -> str
    circle_command = (df_command[df_command['command'].str.contains('MotionCircleRightCommand')]).iloc[0, 1]

    # print(circle_command)
    # reading radius from command file
    radius_circle = float(re.findall(r'radius_m=\d+\.\d+', circle_command)[0].split('=')[1])

    # reading velocity from command file
    velocity_circle = float(re.findall(r'velocity=\d+\.\d+', circle_command)[0].split('=')[1])
    # if m:
    #     print(m.group(1))

# finding index for way points
    takeoff_index = idx[0]+1
    # index after 2nd stop comaand
    start_first_straight_index = idx[0] + 1
    end_first_straight_index=idx[1]

# start of circle should start at the same time when straight path ends
    start_circle_index= idx[1]+1
    end_circle_index= idx[2]
    start_second_straight_index = idx[0] + 1
    end_second_straight_index = idx[1]

    # landing_index = idx[1] + 1
    landing_index = idx[-1]-1

# recording time for straight path

    takeoff_time = float(df_command.loc[takeoff_index, 'timestamp'])
    landing_time = float(df_command.loc[landing_index, 'timestamp'])
    start_first_straight_time= float(df_command.loc[start_first_straight_index, 'timestamp'])
    end_first_straight_time= float(df_command.loc[end_first_straight_index, 'timestamp'])

    oneFourth_first_straight_time = start_first_straight_time + (end_first_straight_time - start_first_straight_time)/4
    half_first_straight_time= start_first_straight_time + (end_first_straight_time - start_first_straight_time)/2
    threeFourth_first_straight_time= start_first_straight_time + (end_first_straight_time - start_first_straight_time)*3/4

# record time for circular path

    start_circle_time= end_first_straight_time
    end_circle_time = float(df_command.loc[end_circle_index, 'timestamp'])

    oneFourth_circle_time = start_circle_time + (end_circle_time - start_circle_time) / 4
    half_circle_time = start_circle_time + (end_circle_time - start_circle_time) / 2
    threeFourth_circle_time = start_circle_time + (end_circle_time - start_circle_time) * 3 / 4

    flight_time_considered = float(landing_time) - float(takeoff_time)

    # dropping data on a separate dataframe preserving for future
    df_exp = df_position.copy(deep=True)
    # converting timestamp column to float for comparing and dropping
    df_exp['timestamp'] = pd.to_numeric(df_exp['timestamp'], downcast="float")
    # dropping rows from start to takeoff time and from start of landing to the end
    # df_exp = df_exp.drop(df_exp[df_exp.timestamp <= float(takeoff_time)].index)
    # df_exp = df_exp.drop(df_exp[df_exp.timestamp >= float(landing_time)].index)
    df_exp = df_exp.drop(df_exp[df_exp.timestamp < float(df_command.loc[start_first_straight_index, 'timestamp'])].index)
    df_exp = df_exp.drop(df_exp[df_exp.timestamp > float(df_command.loc[end_circle_index, 'timestamp'])].index)

    # transfer back for now (pass by reference)
    df_position = df_exp.copy(deep=False)
    # print(df_exp.head())

    # for linear mobility
    uavStartPos = Point(df_position.iloc[0]['stateEstimate.x'], df_position.iloc[0]['stateEstimate.y'],
                        df_position.iloc[0]['stateEstimate.z'])
    uavEndPos = Point(df_position.iloc[-1]['stateEstimate.x'], df_position.iloc[-1]['stateEstimate.y'],
                      df_position.iloc[-1]['stateEstimate.z'])
    totalFlightTime = df_position.iloc[-1]['timestamp'] - df_position.iloc[0]['timestamp']





    # making position data time start from 0 to compare time axis with simulation data and plotting
    # df_position.timestamp = np.subtract(df_position['timestamp'], float(takeoff_time))
    # print(df_position.head())
    df_position['timestamp'] = [x - float(takeoff_time) for x in df_position['timestamp']]
    # print(df_position)

# time list start, 1/4, 1/2, 3/4, end, 1/4, 1/2. 3/4, end
#     print(['start', '1/4', '1/2', '3/4', 'end', '1/4', '1/2', '3/4', 'end'])
    time=[start_first_straight_time, oneFourth_first_straight_time, half_first_straight_time, threeFourth_first_straight_time,
          end_first_straight_time, oneFourth_circle_time, half_circle_time, threeFourth_circle_time, end_circle_time]
    # print(time)
    time=np.subtract(time, takeoff_time)
    # print(time)
    totalFlightTime=time[-1] #last time element

    waypoint_index=[df_position.index[abs(df_position['timestamp'] - times) <= 0.005 ].tolist()[0] for times in time]

    #x coordinate or waypoints
    x=[(df_position.loc[ids]['stateEstimate.x']) for ids in waypoint_index]
    y=[(df_position.loc[ids]['stateEstimate.y']) for ids in waypoint_index]
    # print(x)

    # print('whole story')
    # print(waypoint_index)
    # print(time)
    # print(x)
    # print(y)


    return uavStartPos, uavEndPos, totalFlightTime, time, x,y

def make_plot():
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_filename = os.path.join(current_file, '../examples/simpleSimulation/results/positionResults.csv')

    df_simulation = pd.read_csv(csv_filename, sep=r'\t', skipinitialspace=True, engine='python')
    # copy of df_simulation dataframe without affecting the df_simulation
    df_simulation_trimmed = df_simulation.copy(deep=True)
    # print(df_simulation)
    # print('hello bhai')
    # print(df_simulation_trimmed.head)
    df_simulation_trimmed = df_simulation_trimmed.drop(
        df_simulation_trimmed[df_simulation_trimmed.passedTime >= float(flight_time_considered)].index)


    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{'type': 'scene', 'rowspan': 3}, {'type': 'xy'}],
               [None, {'type': 'xy'}],
               [None, {'type': 'xy'}]
               ]
    )

    # print(df_position.columns)
    fig.add_trace(
        go.Scatter3d(x=df_position['stateEstimate.x'].to_numpy(), y=df_position['stateEstimate.y'].to_numpy(),
                     z=df_position['stateEstimate.z'].to_numpy(), mode="lines",
                     line={"color": 'red'}, name='reference'), row=1, col=1

    )
    fig.add_trace(
        go.Scatter3d(x=df_simulation['posX'].to_numpy(), y=df_simulation['posY'].to_numpy(),
                     z=df_simulation['posZ'].to_numpy(), mode="lines",
                     line={"color": 'blue'}, name='simulation'), row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df_simulation_trimmed['passedTime'].to_numpy(), y=df_simulation_trimmed['posX'].to_numpy(),
                   mode="lines",
                   line={"color": 'blue'}, name='simulation', showlegend=False), row=1, col=2,

    )

    fig.add_trace(
        go.Scatter(x=df_position['timestamp'].to_numpy(), y=df_position['stateEstimate.x'].to_numpy(), mode="lines",
                   line={"color": 'red'}, name='simulation', showlegend=False), row=1, col=2
    )
    fig.update_xaxes(title='t(s)', row=1, col=2)
    fig.update_yaxes(title='x(m)', row=1, col=2)

    fig.add_trace(
        go.Scatter(x=df_simulation_trimmed['passedTime'].to_numpy(), y=df_simulation_trimmed['posY'].to_numpy(),
                   mode="lines",
                   line={"color": 'blue'}, name='simulation', showlegend=False), row=2, col=2
    )

    fig.add_trace(
        go.Scatter(x=df_position['timestamp'].to_numpy(), y=df_position['stateEstimate.y'].to_numpy(), mode="lines",
                   line={"color": 'red'}, name='simulation', showlegend=False), row=2, col=2
    )

    fig.update_xaxes(title='t(s)', row=2, col=2)
    fig.update_yaxes(title='y(m)', row=2, col=2)

    fig.add_trace(
        go.Scatter(x=df_simulation_trimmed['passedTime'].to_numpy(), y=df_simulation_trimmed['posZ'].to_numpy(),
                   mode="lines",
                   line={"color": 'blue'}, name='simulation', showlegend=False), row=3, col=2
    )

    fig.add_trace(
        go.Scatter(x=df_position['timestamp'].to_numpy(), y=df_position['stateEstimate.z'].to_numpy(), mode="lines",
                   line={"color": 'red'}, name='simulation', showlegend=False), row=3, col=2
    )
    fig.update_xaxes(title='t(s)', row=3, col=2)
    fig.update_yaxes(title='z(m)', row=3, col=2)



    fig.update_layout(scene=dict(
        xaxis_title='X (m)',
        yaxis_title='Y (m)',
        zaxis_title='Z (m)',
        # aspectratio=dict(x=1, y=1, z=0.95),
        # xaxis_tickmode='linear',
        # xaxis_nticks=5,
        # xaxis_range=[0,-.4],
        # xaxis_range=[-.6,.6],
        xaxis_range=[-.8,.8],
        zaxis_range=[0.0, .33],
        #
        # xaxis_dtick=0.1,
    ),

    )

    fig.show()


