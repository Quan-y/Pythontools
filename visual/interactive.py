# -*- coding: utf-8 -*-
"""
===============================================================================
===================== PYTHON SQLITE API BASED ON DATAFRAME ====================
===============================================================================
@author: QUAN YUAN
"""
import plotly as py
import plotly.graph_objs as go
pyplt = py.offline.plot

# only support two y-axes dynamic plot with plotly
class Two_y:
    '''
    INPUT: DATAFRAME AND COLUMNS WHICH YOU WANT TO PLOT
    OUTPUT: TWO_Y.HTML
    '''
    def __init__(self, data, xcol, ycol):
        # data: dataframe structure
        self.data = data
        # ycol: list(sting)
        self.ycol = ycol
        # xcol: list(sting)
        self.xcol = xcol
        
    def plot(self, title = 'TWO Y GRAPH', name_y1 = 'y1', \
             name_y2 = 'y2', kind = 'line', save = 'TWO_Y.html'):
        
        trace1 = go.Scatter(
            x = self.data[self.xcol[0]],
            y = self.data[self.ycol[0]],
            name = 'y1'
        )
        trace2 = go.Scatter(
            x = self.data[self.xcol[1]],
            y = self.data[self.ycol[1]],
            name = name_y2,
            yaxis = 'y2'
        )
        data = [trace1, trace2]
        layout = go.Layout(
            title = title,
            yaxis = dict(
                title = name_y1,
            ),
            yaxis2 = dict(
                title = name_y2,
                titlefont = dict(
                    color = 'rgb(148, 103, 189)'
                ),
                tickfont = dict(
                    color='rgb(148, 103, 189)'
                ),
                overlaying = 'y',
                side = 'right'
            )
        )
        fig = dict(data = data, layout = layout)
        pyplt(fig, filename = save)
        