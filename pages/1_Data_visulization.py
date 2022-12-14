import streamlit as st
import time
import numpy as np
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

PATH_WAREHOUSES = 'data/warehouses.csv'

st.set_page_config(
    page_title="Data visulization",
    layout="wide",
)

@st.experimental_memo
def load_data(path):
    df = pd.read_csv(path)
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    return df


def show_common_data(df):
    st.subheader('Locations of all warehouses')
    st.map(df)

    st.subheader('The number of types of sensors for each warehouse')
    filt = (df['time'] == df['time'][0])
    count_type_sensors = df[filt].groupby('name')['type_sensor'].value_counts().to_frame(name='count').reset_index(level=[0, 1])
    fig = px.bar(count_type_sensors, x='name', y='count', color="type_sensor",
                 title="The number of types of sensors for each warehouse",
                 labels={
                     "count": "Count",
                     "name": "Names of warehouses",
                     "type_sensor": "Type of sensor"
                 },)
    fig.update_layout(paper_bgcolor="#F9F9F9")
    st.plotly_chart(fig, use_container_width=True)



    print(df)



def date_picker(start, end):

    col1, col2 = st.columns(2)
    start_date = col1.date_input('Start date', start)
    start_time = col2.time_input('Start time', datetime.time(0, 0, 0))

    col3, col4 = st.columns(2)
    end_date = col3.date_input('End date', end)
    end_time = col4.time_input('End time', datetime.time(23, 59, 59))

    return (start_date, start_time), (end_date, end_time)

def show_warehouse_data(df, option):
    st.subheader(f'Location of {option}')
    st.map(df)

    st.subheader(f'The number of types of sensors for {option}')
    filt = (df['time'] == df['time'].iloc[0])
    count_type_sensors = df[filt]['type_sensor'].value_counts().to_frame(name='count').reset_index(level=[0])
    fig = px.bar(count_type_sensors, x='index', y='count',
                 title=f"The number of types of sensors for {option}",
                 labels={
                     "index": "Type of sensor",
                     "count": "Count",
                 },)
    fig.update_layout(paper_bgcolor="#F9F9F9")
    st.plotly_chart(fig, use_container_width=True)


    types_sensor = df['type_sensor'].unique().tolist()
    st.subheader(f'Data from devices')
    for type_sensor in types_sensor:
        #st.subheader(f'Graphics for {type_sensor}')

        #device_ids = df[df['type_sensor'] == type_sensor]['device_id'].unique().tolist()
        #for device_id in device_ids:
        #    st.write(f'Device id: {device_id}')


        #df = px.data.gapminder().query("continent=='Oceania'")
        
        device_df = df[df['type_sensor'] == type_sensor] #.groupby('device_id').value_counts().reset_index(name='count')
        fig = px.line(device_df, x="time", y="value", color='device_id',
                        title=f"{type_sensor.upper()}",
                        labels={
                            "device_id": "Device id",
                        },)
        average_line = device_df.groupby('time')['value'].mean().reset_index(level=[0])
        fig.add_trace(
            go.Scatter(
                x=average_line['time'],
                y=average_line['value'],
                mode="lines",
                line=go.scatter.Line(color="gray"),
                showlegend=True,
                name="Average")
        )
        fig.update_layout(paper_bgcolor="#F9F9F9")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(f'Processed data in the table format')
    st.checkbox("Use container width", value=True, key="use_container_width")
    st.dataframe(df, use_container_width=st.session_state.use_container_width)
    




    



df = load_data(PATH_WAREHOUSES)

st.title("Data visualization")
option = st.selectbox('Choose warehouse', [
                      "All"] + df['name'].unique().tolist())

if option == 'All':
    st.write('Show common data')
    show_common_data(df)
else:
    df = df[df['name'] == option]
    (start_date, start_time), (end_date, end_time) = date_picker(df['time'].iat[0], df['time'].iat[-1])
    if start_date > end_date:
        st.error("The start date must be earlier than the end date.")
    else:
        start = datetime.datetime.combine(start_date, start_time)
        end = datetime.datetime.combine(end_date, end_time)
        filt = (df['time'] >= start) & (df['time'] <= end)
        df = df[filt]
        if not df.empty:
            show_warehouse_data(df, option)
        else:
            st.warning(f'There are no data for time period: {start} -- {end}. Please choose another time period')
    
