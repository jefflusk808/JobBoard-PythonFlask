import sqlite3
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, State, Output

#from .Dash_fun import apply_layout_with_auth, load_object, save_object

"""tutorial of dash from  https://www.datacamp.com/community/tutorials/learn-build-dash-python
& a git repo https://github.com/jimmybow/Flask_template_auth_with_Dash
https://dash.plot.ly/interactive-graphing"""

PATH = "db/jobs.sqlite"
url_base = '/dash/app1/'


con = sqlite3.connect(PATH)
df = pd.read_sql_query(
    'SELECT employer.name, job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id'
    , con)

#creating a data frame aggregated to get num_jobs
df1 = df.groupby(['name']).size().reset_index(name='num_jobs')

#creating figure diagram below
fig = px.bar(df1, x="name", y="num_jobs", color= "num_jobs")


colors = {
    'background': 'white',
    'text': 'black'
}

layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Number of Jobs by Employer',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Placeholder title', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='num-of-jobs',
        figure= fig
    )
])

def Add_Dash(server):
    app = dash.Dash(server=server, url_base_pathname=url_base)
    app.layout = layout

    """
    apply_layout_with_auth(app, layout)
    @app.callback(
        Output('target', 'children'),
        [Input('input_text', 'value')])
    def callback_fun(value):
        return 'your input is {}'.format(value)
    """
    return app.server

#if __name__ == '__main__':
#    app.run_server(debug=True)
