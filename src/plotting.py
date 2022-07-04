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
from random import randint
from os.path import abspath

from plotly.graph_objs import Layout


# loading position file

df_position = pd.DataFrame()
flight_time_considered = 0.0


# data being loaded to dataframe and variables to be passed to the simulator
def load_Data():
    global df_position
    global flight_time_considered
  
    uavStartPos1=Point(0, math.sqrt(3), 1)
    uavEndPos1=Point(0, math.sqrt(3), 1)
    time1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    x1 = np.linspace(1.5, 2.5, num=10 )
    y1 = np.linspace(1.5, 2.5, num=10 )
    z1=[1, 1.3, 1, 0.7, 1, 1.3, 1, 0.7, 1, 1.3]


    totalFlightTime1 = time1[-1]

    #waypoint for 2nd uav
    time2=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    x2= [-1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1]      #right ahnd grip shape
    y2= [0, 1, 0, -1, 0, 1, 0, -1, 0,  1, 0, -1, 0]
    z2=np.linspace(3, 0.5, num=13)
    x2=np.add(x2,2)
    y2=np.add(y2,2)


    uavStartPos2 = Point(x2[0], y2[0], z2[0])
    uavEndPos2 = Point(x2[-1], y2[-1], z2[-1])

    totalFlightTime2=time2[-1]

    ################# usual##############
    uavStartPos=[uavStartPos1, uavEndPos2]
    uavEndPos= [uavEndPos1, uavEndPos2]
    totalFlightTime=[totalFlightTime1, totalFlightTime2]

    speed=[3, 3]

    x=[x1, x2]
    y=[y1,y2]
    z=[z1, z2]
    print('data')
    print(x)
    print(y)
    print(z)
    print(speed)


    time1 = np.linspace(1,12,12)#[0, 15]
    x1 = np.linspace(1,12,12)#[1500,0]
    y1 = np.empty(12)#[1500,5]
    y1.fill(12)
    z1=np.empty(12)#[3,7]
    z1.fill(3)
    uavStartPos1 = Point(x1[0], y1[0], z1[0])
    uavEndPos1 = Point(x1[-1],y1[-1],z1[-1])

    totalFlightTime1 = time1[-1]

    uavStartPos=[uavStartPos1]
    uavEndPos= [uavEndPos1]
    totalFlightTime=[totalFlightTime1]
    time=[time1]
    x=[x1]
    y=[y1]
    z=[z1]
    return speed, x,y,z

def make_plot():
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_filename = os.path.join(current_file, '../examples/simpleSimulation/results/positionResults.csv')

    df_simulation = pd.read_csv(csv_filename, sep=r'\t', skipinitialspace=True, engine='python')
    # copy of df_simulation dataframe without affecting the df_simulation
    # df_simulation_trimmed = df_simulation.copy(deep=True)
    max_uav_index=max(df_simulation['uid'])

    df_simulation_uavs=[]


    for index in range(max_uav_index+1):
        df_simulation_uavs.append(df_simulation.loc[df_simulation['uid'] == index])

    # diffeerent colors for plot chosen randomly
    color = []
    n = max_uav_index+1
    if n<=3:
        color=['red', 'green', 'blue']
    else:
        for i in range(n):
            color.append('#%06X' % randint(0, 0xFFFFFF))

    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{'type': 'scene', 'rowspan': 3}, {'type': 'xy'}],
               [None, {'type': 'xy'}],
               [None, {'type': 'xy'}]
               ]
    )

    for index,df_uav in enumerate( df_simulation_uavs):
        fig.add_trace(
            go.Scatter3d(x=df_uav['posX'].to_numpy(), y=df_uav['posY'].to_numpy(),
                         z=df_uav['posZ'].to_numpy(), mode="lines",
                         line={"color": color[index]}, name='simulation uav'+str(index)), row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=df_uav['passedTime'].to_numpy(), y=df_uav['posX'].to_numpy(),
                       mode="lines",
                       line={"color": color[index]}, name='simulation', showlegend=False), row=1, col=2,

        )

        fig.update_xaxes(title='t(s)', row=1, col=2)
        fig.update_yaxes(title='x(m)', row=1, col=2)

        fig.add_trace(
            go.Scatter(x=df_uav['passedTime'].to_numpy(), y=df_uav['posY'].to_numpy(),
                       mode="lines",
                       line={"color": color[index]}, name='simulation uav0', showlegend=False), row=2, col=2
        )

        fig.update_xaxes(title='t(s)', row=2, col=2)
        fig.update_yaxes(title='y(m)', row=2, col=2)

        fig.add_trace(
            go.Scatter(x=df_uav['passedTime'].to_numpy(), y=df_uav['posZ'].to_numpy(),
                       mode="lines",
                       line={"color": color[index]}, name='simulation uav0', showlegend=False), row=3, col=2
        )
        fig.update_xaxes(title='t(s)', row=3, col=2)
        fig.update_yaxes(title='z(m)', row=3, col=2)

    fig.update_layout(scene=dict(
        xaxis_title='X (m)',
        yaxis_title='Y (m)',
        zaxis_title='Z (m)',
         xaxis_nticks=10,
         yaxis_nticks=10,
    ),
    )
    fig.show()