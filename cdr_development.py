# importing the libraries
import pandas as pd
import webbrowser
# !pip install dash
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import plotly.express as px

import dash_bootstrap_components as dbc
import dash_table as dt
import re


# Declaring the Global Variables
# This variable be default is global variable
project_name = None 
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) # [dbc.themes.BOOTSTRAP]


# Declaring multiple function for project
def load_data():
    print("Start of the load_data function")

    # by default local variables
    call_dataset_name = "Call_data.csv" 
    service_dataset_name = "Service_data.csv"
    device_dataset_name = "Device_data.csv"
    
    global call_data, service_data, device_data
    
    call_data = pd.read_csv(call_dataset_name)
    service_data = pd.read_csv(service_dataset_name)
    device_data = pd.read_csv(device_dataset_name)
    
    global start_date_list
    temp_list = sorted (  call_data["date"].dropna().unique().tolist()  )
    start_date_list = [ { "label":str(i)    , "value":str(i)  }    for i in temp_list   ]
    
    global end_date_list
    temp_list = sorted (  call_data["date"].dropna().unique().tolist()  )
    end_date_list = [ { "label":str(i)    , "value":str(i)  }    for i in temp_list   ]
    
    global report_type
    temp_list = [ "Hourly", "Daywise", "Weekly"  ]
    report_type = [ { "label":str(i)    , "value":str(i)  }  for i in temp_list ]
    
    
    
    print("End of the load_data function")

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def create_app_ui_1():
    # css part for tabs
    
    
    tabs_styles = {
    'height': '44px'
}
    tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

    tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
    main_layout = html.Div(
    [
    html.H1(id='Main_title', children = 'CDR Analysis with Insights',style={"color":'black','textAlign':'center',"backgroundColor":'#3498db'}),
    html.Br(),
    
    dcc.Tabs(id='Tabs',value="tab-1",children=[
        
        dcc.Tab(label="Call Analytics Tool",id="Call Analytics tool",value="tab-1",children="call_layout",style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label="Device Analytics Tool",id="Device Analytics tool",value="tab-2",children='device_layout',style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label="Service Analytics Tool",id="Service Analytics tool",value="tab-3",children='service_layout',style=tab_style, selected_style=tab_selected_style)    ], style=tabs_styles) 
   
   
    ])
    return main_layout






@app.callback(
    
    Output('Call Analytics tool','children'),
    [Input("Call Analytics tool","value"),
     
    ]
    
 )
def update_tab_1(tab1):
    if tab1=="tab-1":
        call_layout=html.Div(id='dropdowns',children=[
        dcc.Dropdown(
        id='start-date-dropdown', 
        options = start_date_list,
        placeholder='Select Starting Date Here', value='2019-06-20',style={"backgroundColor":' #ecf0f1  '}
        ),
    
    
    dcc.Dropdown(
        id='end-date-dropdown',
        options = end_date_list,
        placeholder='Select Ending Date Here',value='2019-06-25',style={"backgroundColor":' #ecf0f1 '}
        ),
    
    dcc.Dropdown(
        id='group-dropdown',
        multi=True,
        placeholder='Select Group Here',style={"backgroundColor":'  #ecf0f1 '}
        ),
    
    dcc.Dropdown(
        id='Report-type-dropdown',
        options = report_type,
        placeholder='Select Report Type Here', value = 'Hourly',style={"backgroundColor":'#ecf0f1  '}
        ),
    
    html.Br(),
    
    dcc.Loading(
    html.Div(id='visualization-object', children='Graph, Card, Data Table')
    )
    
  
    
    
    ] 
    )
    
    return call_layout
   
        



def create_card(title, content, color):
    card=dbc.Card(
        dbc.CardBody(
            [
                html.H4(title),
                html.Br(),
                html.Br(),
                html.H2(content),
                html.Br(),
                
                
                
                ]
            
            
            ),

            color=color,inverse=True      
    )
    
    return(card)


@app.callback(
    Output( 'visualization-object', 'children'),
    [
    Input('start-date-dropdown', 'value'  ),
    Input('end-date-dropdown',   'value' ),
    Input('group-dropdown',   'value' ),
    Input('Report-type-dropdown',  'value'  )
    ]
    )

def update_app_ui(start_date, end_date, group, report_type):
    
    print("data type",  str(type(start_date)))
    print("data value", str(start_date))
    
    print("data type",  str(type(end_date)))
    print("data value", str(end_date))

    print("data type",  str(type(group)))
    print("data value", str(group))

    print("data type",  str(type(report_type)))
    print("data value", str(report_type))


    # Write logic to create a Graph, Card and Data Table
    
    #filtering the call data
    call_data_analytics=call_data[(call_data['date']>=start_date)&(call_data['date']<=end_date)]
    
    if (group==[] or group==None):
        pass
    else:
        call_data_analytics=call_data_analytics[call_data_analytics['Group'].isin(group)]
        
    graph_data=call_data_analytics
    
    if(report_type == 'Hourly'):
        graph_data=graph_data.groupby('hourly_range')['Call_Direction'].value_counts().reset_index(name="count")
        x='hourly_range'
        content=call_data_analytics['hourly_range'].value_counts().idxmax()
        title="Bussiest Hour"
        
        
    elif(report_type == 'Daywise'):
        graph_data=graph_data.groupby('date')['Call_Direction'].value_counts().reset_index(name="count")
        x='date'
        content=call_data_analytics['date'].value_counts().idxmax()
        title="Bussiest Day"
    else:
        graph_data=graph_data.groupby('weekly_range')['Call_Direction'].value_counts().reset_index(name="count")
        x='weekly_range'
        content=call_data_analytics['weekly_range'].value_counts().idxmax()
        title="Bussiest Weekday"
        
    graph_figure=px.area(graph_data,
                         x = x,
                         y= 'count',
                         color="Call_Direction",
                         hover_data=["Call_Direction","count"],
                         template="plotly_dark")
    
    
    
    
    
 # Card section   
    
    
    # Card Section
    total_calls = call_data_analytics["Call_Direction"].count()
    card_1 = create_card("Total Calls",total_calls, "success")
      
    incoming_calls = call_data_analytics["Call_Direction"][call_data_analytics["Call_Direction"]=="Incoming"].count()
    card_2 = create_card("Incoming Calls", incoming_calls, "primary")
      
    outgoing_calls = call_data_analytics["Call_Direction"][call_data_analytics["Call_Direction"]=="Outgoing"].count()
    card_3 = create_card("Outgoing Calls", outgoing_calls, "primary")
      
    missed_calls = call_data_analytics["Missed Calls"][call_data_analytics["Missed Calls"] == 3].count()
    card_4 = create_card("Missed Calls", missed_calls, "danger")
  
    max_duration = call_data_analytics["duration"].max()
  
    card_5 = create_card("Max Duration", f'{max_duration} min', "dark")
    
    card_6 = create_card(title, content, "primary")
         
  
    #  md = 4 indicating that on a 'medium' sized
    graphRow0 = dbc.Row([dbc.Col(id='card1', children=[card_1], md=3), dbc.Col(id='card2', children=[card_2], md=3)])
    graphRow1 = dbc.Row([dbc.Col(id='card3', children=[card_3], md=3), dbc.Col(id='card4', children=[card_4], md=3)])
    graphRow2 = dbc.Row([dbc.Col(id='card5', children=[card_5], md=3), dbc.Col(id='card6', children=[card_6], md=3)])
 
    cardDiv = html.Div([graphRow0,html.Br(), graphRow1,html.Br(), graphRow2])
    #data table section
    datatable_data = call_data_analytics.groupby(['Group','UserID','UserDeviceType'])['Call_Direction'].value_counts().unstack(fill_value=0).reset_index()
    if call_data_analytics['Missed Calls'][call_data_analytics['Missed Calls']==19].count()!=0:
        datatable_data['Missed Calls']=call_data_analytics.groupby(['Group','UserId','UserDeviceType'])['Missed Calls'].value_counts().unstack()[3]
    else:
        datatable_data['Missed Calls']=0

    datatable_data['Total_call_duration']= call_data_analytics.groupby(["Group","UserID","UserDeviceType"])["duration"].sum().tolist()
    
    
    datatable=dt.DataTable(
        
        id='table',
        columns=[{"name":i,"id":i} for i in datatable_data.columns],
        data=datatable_data.to_dict('records'),
        page_current=0,
        page_size=20,
        page_action='native',
        style_header={'backgroundColor':'rgb(30,30,30'},
        style_cell={
            
            'backgroundColor':'rgb(50,50,50)',
            'color':'white'
            
            
            }
        
            )
    
    
    
    
    
    
    
    
  
    
    


    return [
            dcc.Graph(figure = graph_figure), html.Br(),
            cardDiv, html.Br(),
            datatable    
        ]


@app.callback(
    Output('group-dropdown', 'options'),
    [
    Input('start-date-dropdown', 'value'),
    Input('end-date-dropdown',  'value')
    ]
    )

def update_groups(start_date, end_date ):
    
    print("data type = ",  str(type(start_date)))
    print("data value = ", str(start_date))
    
    print("data type = ",  str(type(end_date)))
    print("data value = ", str(end_date))
    
    temp_data = call_data [ (  call_data["date"] >= start_date)  & ( call_data["date"]<= end_date)]
    group_list = temp_data["Group"].unique().tolist()
    
    group_list = [ {"label":m, "value":m }      for m in group_list] 

    return group_list

#device tab section
    
@app.callback(
    
    Output('Device Analytics tool','children'),
    [Input("Device Analytics tool","value"),
     
    ]
    
 )
def update_tab_2(tab2):
    print("data type = ",  str(type(tab2)))
    print("data value = ", str(tab2))
    if tab2=="tab-2":
        
       
        device_layout=html.Div(id='dropdown',children=[
        dcc.Dropdown(
        id='date_dropdown', 
        options = start_date_list,
        placeholder='Select Date Here',multi=True,style={"backgroundColor":' #ecf0f1  '}
        ),html.Div(id="device_chart",children="device_layout")] )
        
        return device_layout
    

# function to count the usage of each device.
def count_devices(data):
    device_dict={
        "Polycom":0,
        "Windows":0,
        "iphone":0,
        "Android":0,
        "Mac":0,
        "Yealink":0,
        "Aastra":0,
        "Others":0 }
    reformed_data = data['UserDeviceType'].dropna().reset_index()
    for var in reformed_data['UserDeviceType']:
        if re.search("Polycom",var):
            device_dict["Polycom"]+=1
        elif re.search("Yealink",var):
            device_dict["Yealink"]+=1
        
        elif re.search("Aastra",var):
            device_dict["Aastra"]+=1
        
        elif re.search("Windows",var):
            device_dict["Windows"]+=1
        
        elif re.search("iPhone|ios",var):
            device_dict["iphone"]+=1
        
        elif re.search("Mac",var):
            device_dict["Mac"]+=1
        
        elif re.search("Android",var):
            device_dict["Android"]+=1
        else:
            device_dict["Others"]+=1
            
    final_data=pd.DataFrame()
    final_data["Device"]=device_dict.keys()
    final_data['Count']=device_dict.values()
    return final_data

@app.callback(
    
    Output('device_chart','children'),
    [
     
     Input('date_dropdown','value')
     
     
     ]
    
    
    
    )

def update_date_dropdown(device_date_list):
    
    print("data type = ",  str(type(device_date_list)))
    print("data value = ", str(device_date_list))
    
    if device_date_list==[] or device_date_list==None:
        device_data_analytics=count_devices(device_data)
    else:
        device_data_analytics=count_devices(device_data[device_data['DeviceEventDate'].isin(device_date_list)])
    
    fig=px.pie(device_data_analytics,names="Device",values="Count",color="Device",hole=.3)
   # fig.update_layout(autosize=True,color="",margin=dict(l=0,r=0,t=25,b=20))
    return dcc.Graph(figure=fig)
        







    

#service tab section
    
@app.callback(
    
    Output('Service Analytics tool','children'),
    [Input("Service Analytics tool","value"),
     
    ]
    
 )
def update_tab_3(tab3):
    print("data type = ",  str(type(tab3)))
    print("data value = ", str(tab3))
    if tab3=="tab-3":
        
       
        service_layout=html.Div(id='service_dropdown',children=[
        dcc.Dropdown(
        id='service_date_dropdown', 
        options = start_date_list,
        placeholder='Select Date Here',multi=True,style={"backgroundColor":' #ecf0f1  '}
        ),html.Div(id="service_chart",children="service_layout")] )
        
        return service_layout
    

@app.callback(
    
    Output('service_chart','children'),
    [
     
     Input('service_date_dropdown','value')
     
     
     ]
    
    
    
    )

def update_service_date_dropdown(service_date_list):
    print("data type = ",  str(type(service_date_list)))
    print("data value = ", str(service_date_list))
    
   
    if service_date_list is None or service_date_list == []:
        service_data_analytics = service_data["FeatureName"].value_counts().reset_index(name = "Count")
    else:
        service_data_analytics = service_data["FeatureName"][service_data["FeatureEventDate"].isin(service_date_list)].value_counts().reset_index(name = "Count")
    fig = px.pie(service_data_analytics, names = "index", values = "Count",color = "index")
        
    fig.update_layout(autosize=True,
                          margin=dict(l=0, r=0, t=25, b=20),
                          )
    return dcc.Graph(figure = fig)



# Declaring the main function 
def main():
    print("Start of the main function")

    global project_name
    project_name = "CDR Analysis with Insights" 
    
    load_data()
    open_browser()

    
    
    global app
    app.title = project_name
    app.layout = create_app_ui_1()
    app.run_server()
    

    print("End of the main function")
    app = None
    project_name = None
    
    global call_data, service_data, device_data, start_date_list,end_date_list,report_type
    call_data = None
    service_data = None
    device_data = None
    start_date_list = None
    end_date_list = None
    report_type = None
    

# Calling the main function
if (__name__ == '__main__'):
    main()
    
    


