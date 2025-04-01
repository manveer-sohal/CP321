import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

#so much work
data = [
    {"Year": 2018, "Winner": "France", "Runner-Up": "Croatia"},
    {"Year": 2014, "Winner": "Germany", "Runner-Up": "Argentina"},
    {"Year": 2010, "Winner": "Spain", "Runner-Up": "Netherlands"},
    {"Year": 2006, "Winner": "Italy", "Runner-Up": "France"},
    {"Year": 2002, "Winner": "Brazil", "Runner-Up": "Germany"},
    {"Year": 1998, "Winner": "France", "Runner-Up": "Brazil"},
    {"Year": 1994, "Winner": "Brazil", "Runner-Up": "Italy"},
    {"Year": 1990, "Winner": "Germany", "Runner-Up": "Argentina"},
    {"Year": 1986, "Winner": "Argentina", "Runner-Up": "Germany"},
    {"Year": 1982, "Winner": "Italy", "Runner-Up": "Germany"},
    {"Year": 1978, "Winner": "Argentina", "Runner-Up": "Netherlands"},
    {"Year": 1974, "Winner": "Germany", "Runner-Up": "Netherlands"},
    {"Year": 1970, "Winner": "Brazil", "Runner-Up": "Italy"},
    {"Year": 1966, "Winner": "England", "Runner-Up": "Germany"},
    {"Year": 1962, "Winner": "Brazil", "Runner-Up": "Czechoslovakia"},
    {"Year": 1958, "Winner": "Brazil", "Runner-Up": "Sweden"},
    {"Year": 1954, "Winner": "Germany", "Runner-Up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner-Up": "Brazil"},
    {"Year": 1938, "Winner": "Italy", "Runner-Up": "Hungary"},
    {"Year": 1934, "Winner": "Italy", "Runner-Up": "Czechoslovakia"},
    {"Year": 1930, "Winner": "Uruguay", "Runner-Up": "Argentina"}
]


df = pd.DataFrame(data)

wins = df["Winner"].value_counts().reset_index()
wins.columns = ["Country", "Wins"]

iso_map = {
    "Brazil": "BRA",
    "Germany": "DEU",
    "Italy": "ITA",
    "Argentina": "ARG",
    "France": "FRA",
    "Uruguay": "URY",
    "England": "GBR",
    "Spain": "ESP",
    "Netherlands": "NLD",
    "Croatia": "HRV",
    "Sweden": "SWE",
    "Hungary": "HUN",
    "Czechoslovakia": "CZE"
}

wins["Code"] = wins["Country"].map(iso_map)

app = Dash(__name__)
server = app.server

app.title = "FIFA Soccer World Cup winners"

app.layout = html.Div([
    html.H1("FIFA Soccer World Cup winners Dashboard", style={"textAlign": "center", 'color': 'black'}),

    dcc.Graph(id="map"),

    html.Label("Select a Country:", style={"marginTop": "30px", 'color': 'black'}),
    dcc.Dropdown(
        options=[{"label": country, "value": country} for country in sorted(wins["Country"])],
        id="country-dropdown",
        placeholder="Select a country"
    ),
    html.Div(id="country-output", style={"marginTop": "20px"}),

    html.Label("Select a Year:", style={"marginTop": "20px",'color': 'black'}),
    dcc.Dropdown(
        options=[{"label": year, "value": year} for year in sorted(df["Year"], reverse=True)],
        id="years-dropdown",
        placeholder="Select a year"
    ),
    html.Div(id="year-output", style={"marginTop": "20px"})
])

@app.callback(
    Output("map", "figure"),
    Input("country-dropdown", "value")
)
def update_map(selected_country):
    fig = px.choropleth(
        wins,
        locations="Code",
        color="Wins",
        hover_name="Country",
        color_continuous_scale="Greens",
        title="World Cup Wins by Country"
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=False))
    return fig

@app.callback(
    Output("country-output", "children"),
    Input("country-dropdown", "value")
)
def display_country_wins(country):
    if not country:
        return ""
    num_wins = wins.loc[wins["Country"] == country, "Wins"].values[0]
    return html.Div([
        html.Span(f"{country}", style={'color': 'blue', 'font-weight': 'bold'}),
        html.Span(" has won the FIFA World Cup ", style={'color': 'black'}),
        html.Span(f"{num_wins}", style={'color': 'gold', 'font-weight': 'bold'}),
        html.Span(" time(s).", style={'color': 'black'})
    ])

@app.callback(
    Output("year-output", "children"),
    Input("years-dropdown", "value")
)
def display_year_results(year):
    if not year:
        return ""
    row = df[df["Year"] == year].iloc[0]
    return html.Div([
        html.Span(f"In {year}, the Winner was ", style={'color': 'black'}),
        html.Span(row['Winner'], style={'color': 'green', 'font-weight': 'bold'}),
        html.Span(" and the Runner-Up was ", style={'color': 'black'}),
        html.Span(row['Runner-Up'], style={'color': 'red', 'font-weight': 'bold'}),
        html.Span(".", style={'color': 'black'}),
    ])
if __name__ == "__main__":
    app.run(debug=True)
