from io import DEFAULT_BUFFER_SIZE
import streamlit as st
    # importing numpy and pandas for to work with sample data.
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import altair as alt
import time
import datetime


st.title('Vizualisation')
st.caption('Cette application  permet de visualiser **les deux premiers dataset du lab 1** ')
def decorateur(function):
        def modified_function(df):
                time_ = time.time()
                res = function(df)
                time_ = time.time()-time_
                with open(f"{function.__name__}_exec_time.txt","w") as f:
                 f.write(f"{time_}")
                return res
        return modified_function

@st.cache
def download(fichier_csv):
         df = pd.read_csv(fichier_csv)[:100]
         return df
@decorateur
@st.cache
def uber_transform(dataf):
        df=dataf.copy()
        df['Date/Time']=pd.to_datetime(df['Date/Time'])
        df['Day']=df['Date/Time'].map(get_dom)
        df['Week']= df['Date/Time'].map(get_weekday)
        df['hour']= df['Date/Time'].map(get_hour)
        return df
@st.cache     
def get_dom(dt):
        return dt.day
@st.cache
def get_weekday(dt):
        return dt.weekday()
@st.cache
def get_hour(dt):
        return dt.hour
@st.cache
def count_rows(rows):
        return len(rows)
@st.cache
def dataformap1(df):
        df3= df[['Lat','Lon']]
        df3.columns=['lat','lon']
        return df3


@decorateur
@st.cache
def trips_transform(dataf):
        df4=dataf.copy()
        df4['tpep_pickup_datetime']=pd.to_datetime(df4['tpep_pickup_datetime'])
        df4['tpep_dropoff_datetime']=pd.to_datetime(df4['tpep_dropoff_datetime'])
        df4['hour_pick']=df4['tpep_pickup_datetime'].map(get_hour)
        df4['hour_drop']=df4['tpep_dropoff_datetime'].map(get_hour)
        return df4
@st.cache
def dataformapdrop(df):
        gps_drop=df[['dropoff_longitude','dropoff_latitude']]
        gps_drop.columns=['lon','lat']
        return gps_drop
@st.cache
def dataformappick(df):
        gps_pick=df[['pickup_longitude','pickup_latitude']]
        gps_pick.columns=['lon','lat']
        return gps_pick
@st.cache
def groupbyvendor(df):
        res= df.groupby('VendorID').agg('sum')
        return res
#uber
df=download('uber_raw_data_apr14.csv')
df2=uber_transform(df)
df3= dataformap1(df)

#trips
df4= download('ny-trips-data.csv')
df5=trips_transform(df4)


vendor=df4[['VendorID','passenger_count','fare_amount','tip_amount','total_amount']]
vendor1=vendor[df4['VendorID']==1]
vendor2=vendor[df4['VendorID']==2]


res= groupbyvendor(vendor)
res1= groupbyvendor(vendor1)
res2= groupbyvendor(vendor2)


option=st.selectbox('Choose one visualisation',['uber','trips'])
if option=='uber':
    st.map(df3)
   
    st.caption("Frequency by DoM - Uber - April 2014")
    st.bar_chart(df2[["Day", "Lat", "Lon"]])

elif option=='trips':
    st.sidebar.title("menu")

   

   
    expander = st.expander("Pick up area")
    expander.write('**Pick up area**')
    expander.map(dataformappick(df4))
    
    expander1 = st.expander("Drop off area")
    expander1.write('**Pick up area**')
    expander1.map(dataformapdrop(df4))
    
    
    st.caption('**Nombre de passager par vendeur**')
    st.bar_chart(res['passenger_count'])

    st.caption('**Total des ventes de billets par vendeur**')
    st.bar_chart(res['fare_amount'])

    st.caption('**Total des pourboires par vendeur**')
    st.bar_chart(res['tip_amount'])

    st.caption('**Total des pourboires par vendeur**')
    st.bar_chart(res['total_amount'])


    st.caption('**proportions pourboire par vendeur**')
    st.bar_chart(res[['fare_amount','tip_amount']])
   
    labels = 'fare_amount','tip_amount'
    ex1=(0,0.1)
    
    fig1, ax1=plt.subplots()
    fig2, ax2=plt.subplots()
    ax1.pie(vendor1[['fare_amount','tip_amount']].apply(np.sum,axis=0), explode=ex1, labels=labels, autopct='%1.1f%%',
       shadow=True, startangle=90)
    ax2.pie(vendor2[['fare_amount','tip_amount']].apply(np.sum,axis=0), explode=ex1, labels=labels, autopct='%1.1f%%',
       shadow=True, startangle=90)
    ax1.axis('equal') 
    ax2.axis('equal') 
    ax1.set_title("vendeur 1")
    ax2.set_title("vendeur2")

    st.pyplot(fig1)
    st.pyplot(fig2)

    st.bar_chart(df5[['hour_pick','passenger_count']].groupby('hour_pick').agg('sum'))
    st.bar_chart(df5[['hour_drop','passenger_count']].groupby('hour_drop').agg('sum'))
    st.line_chart(df5[['hour_pick','trip_distance']].groupby('hour_pick').mean())



st.components.v1.html("<body bgcolor='pink' style='display: flex; justify-content:center'><h1>MON COMPOSANT</h1></body>")