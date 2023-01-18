from dash import dash, html, dcc, dash_table
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("data/cards.csv", delimiter=",")

app = dash.Dash()

fig = px.histogram(df,x=df['type'])

app.layout = html.Div([

    html.H1(children="IT'S TIME TO DU-DU-DU-DU-DU-DUUUUEL"),

    html.Div(children='graph of type'),

    dcc.Graph(
        id='yugraph',
        figure=fig
    ),

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
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

# callbacks

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["country"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
    ]

if __name__ == '__main__':
    app.run_server(debug=True)

#old layout

# app.layout = html.Div(children=[

#     html.H1(children="IT'S TIME TO DU-DU-DU-DU-DU-DUUUUEL"),

#     html.Div(children='graph of type'),

#     dcc.Graph(
#         id='yugraph',
#         figure=fig
#     ),
#     dash_table.DataTable(
#     data=df.to_dict('records'),
#     filter_action='native',
#     columns=[{'id': c, 'name': c} for c in df.columns],
#     fixed_columns={ 'headers': True, 'data': 2 },
#     style_table={'minWidth': '50%'},
#     style_cell={
#         'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
#         'overflow': 'hidden',
#         'textOverflow': 'ellipsis',
#     },
#     page_size=10,
#     ),

#     html.A(html.Button('Refresh Data'),href='/')
# ])
