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


# Reading the geo Location Data
Dept_Popualtion_Geo = pd.read_csv('Geo_Location_Population.csv', encoding = "ISO-8859-1", engine='python')

# adding population
ActiveDeptdf = pd.merge(ActiveDeptdf, Dept_Popualtion_Geo, how='inner', on='Department')

DeadDeptdf = pd.merge(DeadDeptdf, Dept_Popualtion_Geo, how='inner', on='Department')


#Parameter to calculate the last 3 months

import datetime
today = datetime.date.today()
last3Months = today - pd.offsets.MonthBegin(3)
last3Months =  last3Months.strftime("%Y-%m")

# creating the cumulative values for Active/Deaths

ActiveDeptdfL3 = ActiveDeptdf[ActiveDeptdf['Date']>=last3Months]
ActiveDeptdfL3['Cumulative'] = ActiveDeptdfL3.groupby(['Department'])['Active Cases'].apply(lambda x: x.cumsum())

DeadDeptdfL3 = DeadDeptdf[DeadDeptdf['Date']>=last3Months]
DeadDeptdfL3['Cumulative'] = DeadDeptdfL3.groupby(['Department'])['Deaths'].apply(lambda x: x.cumsum())



#Combining LIMA and LIMA REGION into one
# sum of the 2 values LIMA + LIMA REGION
LIMA_DEPT = Deptdf[ (Deptdf['Department'] =='LIMA') | (Deptdf['Department'] =='LIMA REGION') ][['Active Cases','Deaths']].sum()
# Dropping LIMA and LIMA REGION from Deptdf
Deptdf.drop([14,15],axis = 0, inplace = True)
#Adding a the sum of LIMA and LIMA REGION to Dept
Deptdf.loc[len(Deptdf.index)] = ['LIMA', LIMA_DEPT[0], LIMA_DEPT[1]]


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
                            ,zoom=3.89)


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

## fig 3 (active cases) ##########

fig3 = px.scatter(ActiveDeptdfL3, x="Cumulative", y="Active Cases",
           animation_frame="Date", animation_group="Department",
            title = 'Active Cases',
           size="Population", color="Geo Region", hover_name="Department",
          log_x= True, log_y=True, range_x=[1,1000000], range_y=[1,4000], size_max =45)

fig3.update_layout(  title={'x':0.5,'xanchor':'center','font':{'size':20}},
                      yaxis={'title':{'text':'Active Cases per Day'}},
                       xaxis={'title':{'text': 'Total Number of Cases'}},
                     plot_bgcolor=colors['background'],
                     paper_bgcolor=colors['background'],
                     font_color=colors['text'])
fig3.update_xaxes(showgrid=False)
fig3.update_yaxes(showgrid=False)
#fig3.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 600
#fig3.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 600
#fig3.layout.updatemenus[0].buttons[0].method = 'animate'
#fig3.show()

##############################

## fig 4 (deaths) ##########
# Doing the same scatter plot for the number of Dead
fig4 = px.scatter(DeadDeptdfL3, x="Cumulative", y="Deaths",
           animation_frame="Date", animation_group="Department",
            title = 'Deaths',
           size="Population", color="Geo Region", hover_name="Department",
          log_x= True, log_y=True, range_x=[1,5000], range_y=[1,200], size_max =45)

fig4.update_layout(  title={'x':0.5,'xanchor':'center','font':{'size':20}},
                      yaxis={'title':{'text':'Deaths per Day'}},
                       xaxis={'title':{'text': 'Total Deaths'}},
                     plot_bgcolor=colors['background'],
                     paper_bgcolor=colors['background'],
                     font_color=colors['text'])
fig4.update_xaxes(showgrid=False)
fig4.update_yaxes(showgrid=False)
#fig3.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 600
#fig3.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 600
#fig3.layout.updatemenus[0].buttons[0].method = 'animate'
#fig4.show()


######################


### DASH ###################

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
    
     html.Div('''
        The Following information shows the number of active cases and Deaths in the different Departments and Districs in Peru.
        The Data was obtained from the Ministerio de Salud (MINSA) from Peru. This Dashboard gets updated daily.
        
    ''',style={'text-align': 'center', 'color': colors['text']} ),
    
    ####
    
    ####
    ### DROPDOWN ###
    html.Label('Departament',style={'backgroundColor': colors['background'], 'color': colors['text']}),
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

html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}
             
            ,children = 
         
         [html.H4('Number of Cases/Deaths Overall'),
            
            dcc.Graph(figure=fig2)
        ], className="six columns"),
    ], className="row")

     ,
 html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children = [
        html.Div([
        html.H4('Activity in the Last 3 Months by Region',style={'text-align': 'center'}),
        html.H6('Peru is divided by 3 geographical regions; the coast, the highlands and the jungle. \
               Lima, the capital, is located on the coast.'
                ,style={'text-align': 'center'}),
        dcc.Graph(figure= fig3), dcc.Graph(figure= fig4)
        ], className="row")
     
     
                      
                      
                      ])
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

    fig.update_layout( showlegend = False,
                     plot_bgcolor=colors['background'],
                     paper_bgcolor=colors['background'],
                     font_color=colors['text'])
    fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    showgrid=False)
    fig.update_yaxes(showgrid=False)

    
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