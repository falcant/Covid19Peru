import plotly.express as px
import json  # python integrated package
import dash
import dash_html_components as html
import pandas as pd
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output
from collections import OrderedDict 

import time

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import numpy as np
from sklearn.linear_model import LinearRegression
#plt.style.use('ggplot')



# Getting the data
ActiveDeptdf = pd.read_csv('ActivebyDept_with_Date.csv', encoding = "ISO-8859-1", engine='python')
DeadDeptdf = pd.read_csv('Deaths_byDept_with_date.csv', encoding = "ISO-8859-1", engine='python')
Deptdf = pd.read_csv('CasesbyDepartment.csv', encoding = "ISO-8859-1", engine='python')

# Geojson Data
with open('peru_departamental_simple.geojson') as response:
    peru_department = json.load(response)  

# Uploading map by Department

##Defining the colors the the fig2 legend
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}   

fig2 = px.choropleth_mapbox(Deptdf, geojson=peru_department, 
                            color=Deptdf["Active Cases"],
                           locations=Deptdf["Department"], featureidkey="properties.NOMBDEP",
                           center={"lat": -10.151093, "lon": -75.311132},range_color= (0,10000),
                           mapbox_style= "carto-positron",
                           color_continuous_scale=["green","yellow","red"],
                           opacity= 0.4,
                           hover_data= ["Active Cases","Deaths"]
                            ,zoom=4.0)


fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text = 'COVID-19 en el Peru',
                  hoverlabel=dict(
        bgcolor="#111111", 
        font_size=16, 
        font_family="ComicSand",
        font_color = '#7FDBFF'
    ),
                   
    plot_bgcolor=colors['background'],
                     paper_bgcolor=colors['background'],
                     font_color=colors['text']
            
                  ) 
#fig2.show()

# DASH

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.title = "COVID-19 in Peru"
app.layout = html.Div(style={'backgroundColor': colors['background']},
            children =[html.H2("COVID-19 IN PERU", 
                      style={'text-align': 'center', 'color': colors['text']}),
            html.H6("Created by: Felix Alcantara", style={'text-align': 'center', 'color': colors['text']}),
    
     html.Div(children='''
        The Following information shows the number of active cases and Deaths in the different Departments and Districs in Peru.
        The Data was obtained from the Ministerio de Salud (MINSA) from Peru. This Dashboard gets updated daily.
        
    ''',style={'text-align': 'center', 'color': colors['text']} ),
    
    ####
    
    ####
    ### DROPDOWN ###
    html.Label('Department',style={'backgroundColor': colors['background'], 'color': colors['text']}),
    dcc.Dropdown(id = 'Department',
        options=[
            {'label': i, 'value': i}
            for i in ActiveDeptdf['Department'].unique()

        ],
        style = dict(width = '40%',
                     #display = 'inline-block',
                    verticalAlign = "middle"),         
        value="LIMA",
        clearable=False       
     ) ,  
    #############
    
    
    ################

    ################         
 html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children = [
        html.Div([
        html.H4('Monthly Distribution of Active Cases and Deaths',style={'text-align': 'center'}),
        dcc.Loading(dcc.Graph(id='graph-bar'),type='default')
        ], className="six columns"),

        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},children = [
            html.H4('Number of Cases/Deaths Overall'),
            dcc.Graph(figure=fig2)
        ], className="six columns"),
    ], className="row")

])

@app.callback(
    Output("graph-bar", 'figure'),
   #Output("graph-map", 'figure'),
    [Input("Department", 'value')])

def update_figure(selected_Department):
    
    time.sleep(1)
    ##############
    Active = ActiveDeptdf[ActiveDeptdf.Department==selected_Department]
    Dead= DeadDeptdf[DeadDeptdf.Department== selected_Department]
    #dist = Distdf[Distdf.Department == selected_Department]
    
    ################# REGRESSOR ################################
    # Data prep for Active regressor
    #Adf = ActiveDeptdf[ActiveDeptdf['Department']==variable]
    AX = Active.reset_index(drop=True).index
    Ay = Active['Active Cases']

    #regressor = LinearRegression()
    #regressor.fit([X],y)

    # regression for Active
    Areg = LinearRegression().fit(np.vstack(AX), Ay)
    Active['Best Fit'] = Areg.predict(np.vstack(AX))
    #ActiveDeptdf[ActiveDeptdf['Department']==variable]['Best Fit'] = reg.predict(X)

    #################################
    # Data prep for Deaths Regressor

    #Ddf = DeadDeptdf[DeadDeptdf['Department']==variable]
    DX = Dead.reset_index(drop=True).index
    Dy = Dead['Deaths']

    # regression for Deaths

    Dreg = LinearRegression().fit(np.vstack(DX), Dy)
    Dead['Best Fit'] = Dreg.predict(np.vstack(DX))

    #####################################################
    
    fig = make_subplots(rows=2, cols=1, subplot_titles=("Active Cases","Deaths"))

    fig.add_trace(
    go.Bar(x=Active['Date'], y=Active['Active Cases']),
    row=1, col=1
    )
    
    fig.add_trace(go.Scatter(name = 'Line of Best Fit', x=Active['Date'], 
                         y=Active['Best Fit'], mode='lines'),row=1,col=1
    )
    
    fig.add_trace(go.Bar(x=Dead['Date'], y=Dead['Deaths'],marker_color='grey'),
    row=2, col=1
    )
    
    fig.add_trace(go.Scatter(name = 'Line of Best Fit', x=Dead['Date'], 
                         y=Dead['Best Fit'], mode='lines',marker_color='red'),row=2,col=1
    )

    fig.update_layout(showlegend = False,
                     plot_bgcolor=colors['background'],
                     paper_bgcolor=colors['background'],
                     font_color=colors['text'])
    
    #fig.update_xaxes(
    #dtick="M1",
    #tickformat="%b\n%Y")

    
    ##############
    
    #filtered_df = Deptdf[Deptdf.Department == selected_Department]
    #dist = Distdf[Distdf.Department == selected_Department]
    #########################################
    #fig = px.choropleth_mapbox(filtered_df, geojson=peru_department, color="Active Cases",
     #                      locations="Department", featureidkey="properties.NOMBDEP",
     #                      center={"lat": -10.151093, "lon": -75.311132},range_color= (0,10000),
     #                      mapbox_style='open-street-map',color_continuous_scale=["green","yellow","red"],
     #                      opacity= 0.4,
     #                      hover_data= ["Active Cases","Deaths"],zoom=4)


    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text = 'COVID-19 en el Peru',
     #             hoverlabel=dict(
     #   bgcolor="darkblue", 
     #   font_size=16, 
     #   font_family="ComicSand"
     #   ), transition_duration=500) 
    ########################################
    
    
    
    
    #return fig,cols.to_dict('records')
    #return fig3,dist.to_dict("records")
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)