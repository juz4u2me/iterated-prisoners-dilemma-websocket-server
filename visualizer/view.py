import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

def parse_data(filename):
    df = pd.read_csv(filename, comment='#')

    return df

app = dash.Dash(__name__)

df = parse_data('tournaments/cfd41202-53aa-4c6d-a327-cd7fcf281fb2.csv')

# Initialize global variables
team_a_name = df.columns[0]
team_b_name = df.columns[1]
team_a_score = 0
team_b_score = 0
team_a_value = df.iloc[0, 0]
team_b_value = df.iloc[0, 1]
current_round = 1
figure = None

app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column'}, children=[
    html.Header(
        html.H1("Prisoner's Dilemma Coding Championship", style={'textAlign': 'center'}),
        style={'backgroundColor': '#87CEFA', 'padding': '10px'}
    ),
    html.Div(style={'flex-grow': 1, 'display': 'flex'}, children=[
        html.Div([
            html.H3(id='team-a-name', style={'textAlign': 'center'}),
            html.H2(id='team-a-score', style={'textAlign': 'center'}),
            html.Div(id='team-a-value', style={'fontSize': 100, 'textAlign': 'center', 'color': 'green', 'height': '100%'})
        ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
        html.Div([
            html.H3(id='team-b-name', style={'textAlign': 'center'}),
            html.H2(id='team-b-score', style={'textAlign': 'center'}),
            html.Div(id='team-b-value', style={'fontSize': 100, 'textAlign': 'center', 'color': 'red', 'height': '100%'})
        ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
    ]),
    # html.Div(id='round-display', style={'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)', 'width': '100px', 'height': '100px', 'borderRadius': '50%', 'backgroundColor': 'rgba(0, 0, 0, 0.5)', 'color': 'white', 'fontSize': '48px', 'textAlign': 'center', 'lineHeight': '100px', 'zIndex': '10'}),
    html.Div(id='round-display', style={'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)', 'width': '100px', 'height': '100px', 'borderRadius': '50%', 'backgroundColor': 'rgba(0, 0, 0, 0.5)', 'color': 'white', 'fontSize': '48px', 'textAlign': 'center', 'lineHeight': '100px', 'zIndex': 1}),
    dcc.Graph(id='score-chart', style={'height': '300px'}),
    dcc.Interval(
        id='interval-component',
        interval=200,  # Update every 1 second
        n_intervals=0
    )
])

@app.callback(
    [Output('team-a-name', 'children'), Output('team-a-score', 'children'), Output('team-a-value', 'children'),
     Output('team-b-name', 'children'), Output('team-b-score', 'children'), Output('team-b-value', 'children'),
     Output('score-chart', 'figure'), Output('round-display', 'children'), Output('interval-component', 'disabled')],     
    [Input('interval-component', 'n_intervals')]
)
def update_values(n):
    global team_a_name, team_b_name, team_a_score, team_b_score, team_a_value, team_b_value, current_round, figure

    print("round: ", f'{n}')
    if n >= len(df) - 1:
        # Disable the interval
        return team_a_name, f"Total Score: {team_a_score}", team_a_value, team_b_name, f"Total Score: {team_b_score}", team_b_value, figure, f"{current_round+1}", True
    
    team_a_name = df.columns[0]
    team_b_name = df.columns[1]

    # Scoring matrix
    scoring_matrix = [
        [(3, 3), (5, 0)],  # C vs C, C vs B
        [(0, 5), (1, 1)]   # B vs C, B vs B
    ]

    # Calculate cumulative scores
    team_a_score = 0
    team_b_score = 0
    for i in range(n):
        team_a_current_value = df.iloc[i, 0]
        team_b_current_value = df.iloc[i, 1]
        row = 0 if team_a_current_value == 'C' else 1
        col = 0 if team_b_current_value == 'C' else 1
        team_a_score += scoring_matrix[row][col][0]
        team_b_score += scoring_matrix[row][col][1]

    # Get the current value for each team
    team_a_value = df.iloc[n % len(df), 0]
    team_b_value = df.iloc[n % len(df), 1]

        # Create data for the bar chart
    chart_data = [
        go.Bar(x=[team_a_score], y=[team_a_name], orientation='h', marker=dict(color='green')),
        go.Bar(x=[team_b_score], y=[team_b_name], orientation='h', marker=dict(color='blue'))
    ]

    figure = {
        'data': chart_data,
        'layout': {
            'title': 'Cumulative Score',
            'xaxis': {'title': 'Score', 'range': [0, 300]},
            'yaxis': {'title': 'Team'}
        }
    }

    current_round = n
    team_a_value_colored = html.Span(team_a_value, style={'color': 'green' if team_a_value == 'C' else 'red'})
    team_b_value_colored = html.Span(team_b_value, style={'color': 'green' if team_b_value == 'C' else 'red'})
    return team_a_name, f"Total Score: {team_a_score}", team_a_value_colored, team_b_name, f"Total Score: {team_b_score}", team_b_value_colored, figure, f"{current_round + 1}", False

if __name__ == '__main__':
    app.run_server(debug=True)