import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, State, Output
#from .Dash_fun import apply_layout_with_auth, load_object, save_object


"""tutorial of dash from  https://www.datacamp.com/community/tutorials/learn-build-dash-python"""

url_base = '/dash/app1/'


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
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
