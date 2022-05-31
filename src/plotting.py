import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from shapely.geometry import Point
import math
import numpy as np
from random import randint

import logging

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
    time2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    x2 = [-1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1]      #right ahsnd grip shape
    y2 = [0, 1, 0, -1, 0, 1, 0, -1, 0,  1, 0, -1, 0]
    z2 = np.linspace(3, 0.5, num=13)
    # z2.fill(1)
    x2=np.add(x2,2)
    y2=np.add(y2,2)


    speed=[3, 3]

    x=[x1, x2]
    y=[y1,y2]
    z=[z1, z2]

    logging.debug('data')
    logging.debug(x)
    logging.debug(y)
    logging.debug(z)
    logging.debugs(speed)


    time1 = np.linspace(1,12,12)#[0, 15]
    x1 = np.linspace(1,12,12)#[1500,0]
    y1 = np.empty(12)#[1500,5]
    y1.fill(12)
    z1=np.empty(12)#[3,7]
    z1.fill(3)

    return speed, x, y, z

def make_plot():
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_filename = os.path.join(current_file, '../examples/simpleSimulation/results/positionResults.csv')

    df_simulation = pd.read_csv(csv_filename, sep=r'\t', skipinitialspace=True, engine='python')
    max_uav_index=max(df_simulation['uid'])
    df_simulation_uavs=[]


    for index in range(max_uav_index+1):
        df_simulation_uavs.append(df_simulation.loc[df_simulation['uid'] == index])

    # different colors for plot chosen randomly
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


    for index, df_uav in enumerate( df_simulation_uavs):
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


