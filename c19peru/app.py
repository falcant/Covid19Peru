import plotly.express as px
import json  # python integrated package
import dash
import dash_html_components as html
import pandas as pd
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output
from collections import OrderedDict 

Deptdf = pd.read_csv('CasesbyDepartment.csv', encoding = "ISO-8859-1", engine='python')
Distdf = pd.read_csv('CasesbyDistrict.csv', encoding = "ISO-8859-1", engine='python')

with open('peru_departamental_simple.geojson') as response:
    peru_department = json.load(response)  
    
fig2 = px.choropleth_mapbox(Deptdf, geojson=peru_department, color="Active Cases",
                           locations="Department", featureidkey="properties.NOMBDEP",
                           center={"lat": -10.151093, "lon": -75.311132},range_color= (0,10000),
                           mapbox_style='open-street-map',color_continuous_scale=["green","yellow","red"],
			   opacity= 0.4,
                           hover_data= ["Active Cases","Deaths"],zoom=4)


fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text = 'COVID-19 en el Peru',
                  hoverlabel=dict(
        bgcolor="darkblue", 
        font_size=16, 
        font_family="ComicSand"
    )) 
#fig2.show()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.title = "COVID-19 in Peru"
app.layout = html.Div([
    html.H2("Number of COVID-19 Cases in Peru by Department", style={'text-align': 'center'}),
    html.H6("Created by: Felix Alcantara", style={'text-align': 'center'}),
    
     html.Div(children='''
        The Following information shows the number of active cases and Deaths in the different Departments and Districs in Peru.
        The Data was obtained from the Ministerio de Salud (MINSA) from Peru. This Dashboard gets updated daily.
        
    '''),
    
    ### DROPDOWN ###
    html.Label('Departament'),
    dcc.Dropdown(id = 'Department',
        options=[
            {'label': i, 'value': i}
            for i in Deptdf['Department'].unique()
        ],
        value='LIMA'
     ) ,  
    #############
    
    
    ################
    dash_table.DataTable(
        id='table-dropdown',
        #data=Distdf.to_dict('records'),
        
        columns=[{'id': c, 'name': c} for c in Distdf[['District','Active Cases','Deaths','Total']].columns.values],
        
        #page_action='none',
        style_table={'height': '300px', 'overflowY': 'auto'},
        
        filter_action='native',
         style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left',
            'width': '{}%'.format(len(Distdf.columns)),
        } for c in ['Department', 'District','Active Cases','Deaths', 'Total']
    ]
        ,
       style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ] 
        ,
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }    
        ,editable=True,
        dropdown={
            'DISTRITO': {
                 'options': [
                    {'label': i, 'value': i}
                    for i in Distdf['District'].unique()
                ]
            }
        }
    ),
    ################         
    html.Div([
        html.Div([
            html.H4('Location of the Department'),
            dcc.Graph(id='graph-map')
        ], className="six columns"),

        html.Div([
            html.H4('Number of Cases/Deaths Overall'),
            dcc.Graph(figure=fig2)
        ], className="six columns"),
    ], className="row")
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@app.callback(
    [Output("graph-map", 'figure'),Output("table-dropdown",'data')],
   #Output("graph-map", 'figure'),
    [Input("Department", 'value')])

def update_figure(selected_Department):
    
    filtered_df = Deptdf[Deptdf.Department == selected_Department]
    dist = Distdf[Distdf.Department == selected_Department]
    fig = px.choropleth_mapbox(filtered_df, geojson=peru_department, color="Active Cases",
                           locations="Department", featureidkey="properties.NOMBDEP",
                           center={"lat": -10.151093, "lon": -75.311132},range_color= (0,10000),
                           mapbox_style='open-street-map',color_continuous_scale=["green","yellow","red"],
			   opacity= 0.4,
                           hover_data= ["Active Cases","Deaths"],zoom=4)


    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text = 'COVID-19 en el Peru',
                  hoverlabel=dict(
        bgcolor="darkblue", 
        font_size=16, 
        font_family="ComicSand"
        )) 

    #return fig,cols.to_dict('records')
    return fig,dist.to_dict("records")


if __name__ == '__main__':
    app.run_server(debug=False)