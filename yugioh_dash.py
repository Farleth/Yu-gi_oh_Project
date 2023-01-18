from dash import dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df_card = pd.read_csv("data/cards.csv")
df_mons = pd.read_csv("data/monsters.csv")
df_spells = pd.read_csv("data/spells.csv")
df_traps = pd.read_csv("data/traps.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

fig1 = px.histogram(df_spells, x='race')

df_cartes_spell = df_card[df_card['type'].str.contains('Spell', regex=True)]
df_spell = df_cartes_spell[['name','type','desc','race','archetype','image_url','views']]
fig2 = px.pie(df_spell, names='race')

fig3 = px.pie(df_traps, names='race')

row_summary_metrics = dbc.Row(
    [
        dbc.Col("",width=1),
        dbc.Col(html.H4("spell graph"),width=1),
        dbc.Col(html.Div(dcc.Graph(figure=fig2))),
        dbc.Col(html.H4("trap graph"),width=1),
        dbc.Col(html.Div(dcc.Graph(figure=fig3))),
        dbc.Col("",width=1),
    ],
)


app.layout = html.Div([

    html.H1(children="IT'S TIME TO DU-DU-DU-DU-DU-DUUUUEL",
            style={
                "color": "black",
                "text-align": "center",
                'margin-top': '50px',
                'margin-bottom': '50px',
            },
            ),

    dcc.Dropdown(['Monsters', 'Spells', 'Traps'], 'Monsters',
                 id='dropdown',
                 style={
                "color": "black",
                "text-align": "center",
                'margin-bottom': '30px',
                'width': '50%',
                },

                ),

    html.H1("graphs",
            style={
                "color": "black",
                'margin-bottom': '50px',
                }
            ),

    row_summary_metrics,

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_mons.columns
        ],
        data=df_mons.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        fixed_columns={ 'headers': True, 'data': 1 },
        style_table={'minWidth': '80%'},
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
        },
        style_cell={
        'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        },
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),

    html.Div(
            id='table-paging-with-graph-container',
            className="five columns"
        ),

    html.A(html.Button('Refresh Data'),href='/')

])

if __name__ == '__main__':
    app.run_server(debug=True)
