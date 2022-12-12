import streamlit as st
import time
import numpy as np
import pandas as pd
import datetime
import plotly.figure_factory as ff
import plotly.express as px


PATH_WAREHOUSES = 'data/warehouses.csv'

@st.cache
def get_data(path):
    print("=======read_data=======")
    df = pd.read_csv(path)
    # 2022-10-01 00:00:00
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    return df



def show_common_data(df):
    st.subheader('Locations of all warehouses')
    st.map(df)

    print('time', type(df['time'][0]))
    st.subheader('The number of types of sensors for each warehouse')
    filt = (df['time'] == df['time'][0])
    print("nunique", df['type_sensor'].nunique())
    print(df[filt].groupby(['name']).get_group('Warehouse#2'))
    #fig = px.bar(df, x="name", y=["motion sensor", "load sensors", "fire sensor", "smoke sensor"], title="Wide-Form Input")
    #st.plotly_chart(fig, use_container_width=True)



df = get_data(PATH_WAREHOUSES)


option = st.selectbox('Choose warehouse', ["All"] + df['name'].unique().tolist())

st.write('You selected:', option)

if option == 'All':
    st.write('Show common data')
    show_common_data(df)
else:
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = st.date_input('Start date', today)
    end_date = st.date_input('End date', tomorrow)
    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')



#df.set_index("name", inplace = True)
print("="*100)
#print(df.index)
#print(df)
