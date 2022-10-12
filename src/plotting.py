#
# Copyright (C) 2022 Touhid Hossain Pritom <pritom@campus.uni-paderborn.de>
#
# Documentation for these modules is at http://veins.car2x.org/
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
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

def make_plot():
    current_file = os.path.abspath(os.path.dirname(__file__))
    csv_filename = os.path.join(current_file, '../examples/simpleSimulation/results/positionResults_0.csv')

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