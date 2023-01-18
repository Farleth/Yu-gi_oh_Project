from dash import dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df_card = pd.read_csv("data/cards.csv")
df_mons = pd.read_csv("data/monsters.csv")
df_spells = pd.read_csv("data/spells.csv")
df_traps = pd.read_csv("data/traps.csv")

app = dash.Dash()

fig1 = px.histogram(df_spells, x='race')

df_cartes_spell = df_card[df_card['type'].str.contains('Spell', regex=True)]
df_spell = df_cartes_spell[['name','type','desc','race','archetype','image_url','views']]
fig2 = px.pie(df_spell, names='race')

fig3 = px.pie(df_traps, names='race')

row_summary_metrics = dbc.Row(
    [
        dbc.Col("", width=1),
        dbc.Col(dcc.Graph(figure=fig2)),
        dbc.Col(dcc.Graph(figure=fig3)),
        dbc.Col("", width=1),
    ],
)

app.layout = html.Div([

    html.H1(children="IT'S TIME TO DU-DU-DU-DU-DU-DUUUUEL"),

    dcc.Dropdown(['Monsters', 'Spells', 'Traps'], 'Monsters', id='dropdown'),

    row_summary_metrics,

    # dcc.Graph(
    #     id='yugraph2',
    #     figure=fig2
    # ),

    # dcc.Graph(
    #     id='yugraph3',
    #     figure=fig3
    # ),

    html.Div(id='dd-output-container'),

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_card.columns
        ],
        data=df_card.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        fixed_columns={ 'headers': True, 'data': 1 },
        style_table={'minWidth': '50%'},
        style_cell={
        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
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

    html.Div(id='datatable-interactivity-container'),

    html.A(html.Button('Refresh Data'),href='/')
])

if __name__ == '__main__':
    app.run_server(debug=True)
