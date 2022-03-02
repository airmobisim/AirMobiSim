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
def load_Data():
    global df_position
    global flight_time_considered
    '''
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

    #x and y coordinate or waypoints
    x=[(df_position.loc[ids]['stateEstimate.x']) for ids in waypoint_index]
    y=[(df_position.loc[ids]['stateEstimate.y']) for ids in waypoint_index]
    # print(x)

    # print('whole story')
    # print(waypoint_index)
    # print(time)
    # print(x)
    # print(y)

#for fancy waypoints for two uavs
    #find distance of the mid point of one triangle side to the origin
    distance= math.sqrt(0.5 ** 2 + (math.sqrt(3) / 2) ** 2)
    #add radius
    distance += 1
    angle =math.atan((math.sqrt(3)/2)/0.5)
    x_cord= distance * math.cos(math.radians(45))
    y_cord= distance * math.sin(math.radians(45))
    # x_cord = distance * math.cos(angle)
    # y_cord = distance * math.sin(angle) # not better
    '''

    uavStartPos1=Point(0, math.sqrt(3), 1)
    uavEndPos1=Point(0, math.sqrt(3), 1)
    # time1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # x1=     [0, -0.5, -1, 0.0, 1, 0.5, 0, -x_cord, -1, 0, 1, x_cord, 0]    #equilateral triangle and semi circle
    # y1=     [math.sqrt(3), math.sqrt(3)/2, 0, 0, 0, math.sqrt(3)/2, math.sqrt(3), y_cord, 0, -1, 0, y_cord, math.sqrt(3)]
    # z1 = np.empty(13)  # numpy arrat size 12
    # z1.fill(2)    # list filled with 1
    time1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    x1 = np.linspace(-1.5, 1.5, num=10 )
    y1 = np.linspace(-1.5, 1.5, num=10 )
    z1=[1, 1.3, 1, 0.7, 1, 1.3, 1, 0.7, 1, 1.3]

    totalFlightTime1 = time1[-1]

    #waypoint for 2nd uav

    time2=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    x2= [-1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1]      #right ahnd grip shape
    y2= [0, 1, 0, -1, 0, 1, 0, -1, 0,  1, 0, -1, 0]
    z2=np.linspace(3, 0.5, num=13)
    # z2.fill(1)

    uavStartPos2 = Point(x2[0], y2[0], z2[0])
    uavEndPos2 = Point(x2[-1], y2[-1], z2[-1])

    totalFlightTime2=time2[-1]

    # x=np.add(x,3)
    # y=np.add(y,3)
    # print("printing x")
    # print(x)
    uavStartPos=[uavStartPos1, uavEndPos2]
    uavEndPos= [uavEndPos1, uavEndPos2]
    totalFlightTime=[totalFlightTime1, totalFlightTime2]
    time=[10, 10]
    x=[x1, x2]
    y=[y1,y2]
    z=[z1, z2]
    # print("hello")
    # print(time1)
    # print(z1)



    return time, x,y,z

def make_plot():
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_filename = os.path.join(current_file, '../examples/simpleSimulation/results/positionResults.csv')

    df_simulation = pd.read_csv(csv_filename, sep=r'\t', skipinitialspace=True, engine='python')
    # copy of df_simulation dataframe without affecting the df_simulation
    # df_simulation_trimmed = df_simulation.copy(deep=True)
    df_simulation_uav0 = df_simulation.loc[df_simulation['uid'] == 0]
    df_simulation_uav1 = df_simulation.loc[df_simulation['uid'] == 1]
    # print(df_simulation)
    # print('hello bhai')
    # print(df_simulation_trimmed.head)
    # print(flight_time_considered)
    # print(df_simulation_uav0.head())
    # print(df_simulation_uav1.head())

    # be careful with below line print the value of flight_time_considered and rethink.

    # df_simulation_trimmed = df_simulation_trimmed.drop(
    #     df_simulation_trimmed[df_simulation_trimmed.passedTime >= float(flight_time_considered)].index)


    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{'type': 'scene', 'rowspan': 3}, {'type': 'xy'}],
               [None, {'type': 'xy'}],
               [None, {'type': 'xy'}]
               ]
    )

    # print(df_position.columns)
    # fig.add_trace(
    #     go.Scatter3d(x=df_position['stateEstimate.x'].to_numpy(), y=df_position['stateEstimate.y'].to_numpy(),
    #                  z=df_position['stateEstimate.z'].to_numpy(), mode="lines",
    #                  line={"color": 'red'}, name='reference'), row=1, col=1
    #
    # )
    #uav 0
    fig.add_trace(
        go.Scatter3d(x=df_simulation_uav0['posX'].to_numpy(), y=df_simulation_uav0['posY'].to_numpy(),
                     z=df_simulation_uav0['posZ'].to_numpy(), mode="lines",
                     line={"color": 'blue'}, name='simulation uav0'), row=1, col=1
    )
    #uav1
    fig.add_trace(
        go.Scatter3d(x=df_simulation_uav1['posX'].to_numpy(), y=df_simulation_uav1['posY'].to_numpy(),
                     z=df_simulation_uav1['posZ'].to_numpy(), mode="lines",
                     line={"color": 'green'}, name='simulation uav1'), row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df_simulation_uav0['passedTime'].to_numpy(), y=df_simulation_uav0['posX'].to_numpy(),
                   mode="lines",
                   line={"color": 'blue'}, name='simulation', showlegend=False), row=1, col=2,

    )

    # fig.add_trace(
    #     go.Scatter(x=df_position['timestamp'].to_numpy(), y=df_position['stateEstimate.x'].to_numpy(), mode="lines",
    #                line={"color": 'red'}, name='simulation', showlegend=False), row=1, col=2
    # )
    fig.update_xaxes(title='t(s)', row=1, col=2)
    fig.update_yaxes(title='x(m)', row=1, col=2)

    fig.add_trace(
        go.Scatter(x=df_simulation_uav0['passedTime'].to_numpy(), y=df_simulation_uav0['posY'].to_numpy(),
                   mode="lines",
                   line={"color": 'blue'}, name='simulation uav0', showlegend=False), row=2, col=2
    )

    # fig.add_trace(
    #     go.Scatter(x=df_position['timestamp'].to_numpy(), y=df_position['stateEstimate.y'].to_numpy(), mode="lines",
    #                line={"color": 'red'}, name='simulation', showlegend=False), row=2, col=2
    # )

    fig.update_xaxes(title='t(s)', row=2, col=2)
    fig.update_yaxes(title='y(m)', row=2, col=2)

    fig.add_trace(
        go.Scatter(x=df_simulation_uav0['passedTime'].to_numpy(), y=df_simulation_uav0['posZ'].to_numpy(),
                   mode="lines",
                   line={"color": 'blue'}, name='simulation uav0', showlegend=False), row=3, col=2
    )

    # fig.add_trace(
    #     go.Scatter(x=df_position['timestamp'].to_numpy(), y=df_position['stateEstimate.z'].to_numpy(), mode="lines",
    #                line={"color": 'red'}, name='simulation', showlegend=False), row=3, col=2
    # )
    fig.update_xaxes(title='t(s)', row=3, col=2)
    fig.update_yaxes(title='z(m)', row=3, col=2)



    fig.update_layout(scene=dict(
        xaxis_title='X (m)',
        yaxis_title='Y (m)',
        zaxis_title='Z (m)',
        # aspectratio=dict(x=1, y=1, z=0.95),
        # xaxis_tickmode='linear',
         xaxis_nticks=10,
         yaxis_nticks=10,
        # xaxis_range=[0,-.4],
        # xaxis_range=[-.6,.5],
        # xaxis_range=[-.8,.8],
        # zaxis_range=[0.0, .33],
        #
        # xaxis_dtick=0.1,
    ),

    )

    fig.show()


