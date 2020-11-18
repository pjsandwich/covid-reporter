# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 00:19:25 2020

@author: Patrick
"""

import dash
import dash_html_components as html
import pandas as pd
import dash_table as dt
from datetime import datetime as datetm
import mysql.connector

app = dash.Dash(__name__)

def generate_table():
    cnx = mysql.connector.connect(host='database-maui.ct7yl5rjhgtx.us-east-1.rds.amazonaws.com',
                                  database='mauidb',
                                  user='admin',
                                  password='Adminpass')
    query = "select date, location, result from TestTable3"
    cursor = cnx.cursor()
    cursor.execute(query)
    
    data_date = []
    data_location = []
    data_result = []
    
    for data in cursor:
        data_date.append(data[0])
        data_location.append(data[1])
        data_result.append(data[2])
    data_frame = pd.DataFrame({'date':data_date,
                               'location':data_location,
                               'result':data_result})
    #data_frame['date'] = data_frame['date'].apply(lambda x: datetm.strptime(x, '%Y-%m-%d'))
    table = dt.DataTable(data=data_frame.to_dict('records'),
                         columns=[{"name": i, "id": i} for i in data_frame.columns],
                         id='table')
    return table


app.layout = html.Div(children=[html.H1(children='SU COVID-19 MEWPUL Trials',
                                        style={'textAlign': 'center'}),
                                html.Div(children='Brought to you by SU iSchool; SUNY ESF; County of Maui, HI.',
                                         style={'textAlign': 'center'}),
                                html.Div(children=[html.H4(children=''),generate_table()],
                                         style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'})])

# Run the server
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080)