import streamlit as st
import time
import numpy as np
import pandas as pd
import datetime
import plotly.express as px
import random

PATH_WAREHOUSES = 'data/warehouses.csv'

st.set_page_config(
    page_title="Real time",
    layout="wide",
)

@st.experimental_memo
def load_data(path):
    df = pd.read_csv(path)
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    return df



def real_time(df):
    columns = ['device_id', 'type_sensor', 'value', 'time']
    df_real_time = pd.DataFrame(columns=columns)
    device_ids = df.groupby(['type_sensor', 'device_id'])['value'].size().to_frame().reset_index(level=[0, 1])

    placeholder = st.empty()
    row_index = 0
    for seconds in range(200):
        with placeholder.container():
            current_time = datetime.datetime.now()
            for i in range(len(device_ids)):
                row = device_ids.iloc[i]
                type_sensor = row['type_sensor']
                device_id = row['device_id']
                match type_sensor:
                    case "motion sensor":
                        value = random.uniform(0.25, 0.6)
                    case "load sensor":
                        value = random.uniform(45.0, 65.0)
                    case "fire sensor":
                        value = random.uniform(0.02, 0.05)
                    case "smoke sensor":
                        value = random.uniform(0.05, 0.1)
                    case _:
                        print("WRONG TYPE OF SENSORS", type_sensor)
                        quit()
                #current_df = pd.DataFrame([device_id, motion_sensor, load_sensor, fire_sensor, smoke_sensor], columns=columns)
                df_real_time.loc[row_index] = [device_id, type_sensor, value, current_time]
                row_index += 1

            types_sensor = df_real_time['type_sensor'].unique().tolist()
            for type_sensor in types_sensor:
                fig = px.line(df_real_time[df_real_time['type_sensor'] == type_sensor], x="time", y="value", color='device_id',
                                title=f"{type_sensor.upper()}",
                                labels={
                                    "index": "Type of sensor",
                                    "count": "Count",
                                },)
                fig.update_layout(paper_bgcolor="#F9F9F9")
                st.plotly_chart(fig, use_container_width=True)
        time.sleep(1)


df = load_data(PATH_WAREHOUSES)

with st.container():
    st.title("Real time")
    option = st.selectbox('Choose warehouse', df['name'].unique().tolist())
    df = df[df['name'] == option]
    real_time(df)
