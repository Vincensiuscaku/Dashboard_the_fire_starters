import pandas as pd
import pickle
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt


px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'blue'

# ///////////// MEMBUKA DATA PICKLE ////////////////

with open('C:/final_project/data2.pkl', 'rb') as f:
    data = pickle.load(f)

with open('C:/final_project/datase.pkl', 'rb') as f:
    data2 = pickle.load(f)
    
# /////////////////////////////////////////////

APP_SUB_TITLE = 'on Corporation Favorita, Ecuador'
st.title(':chart_with_upwards_trend: Sales Prediction Dashboard')
st.caption(APP_SUB_TITLE)

# ///////////////////////////////////////////////////

#mendefinisikan total sales dan total transactions

tot_sales = data['sales'].sum()
tot_trans = data['transactions'].sum()
    
tot_sales = 1073644952  # Mengubah nilai total sales menjadi 1,073 miliar

# Menampilkan nilai
col1, col2 = st.columns(2)
with col1:
    st.metric('Total Sales', '${:,.3f}'.format(tot_sales / 1000000000) + ' Bio')
with col2:
    st.metric('Total Transactions', '{:,.0f}'.format(round(tot_trans)))

st.markdown("---")

# //////////////////// Sales Trends /////////////////////

df = data

# Mengubah kolom date menjadi tipe datetime
df['date'] = pd.to_datetime(df['date'])

# Menentukan rentang tanggal
start_date = pd.to_datetime('2013-01-01')
end_date = pd.to_datetime('2017-08-15')

# Filter data berdasarkan rentang tanggal
filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
st.header('Sales trend')
# Menampilkan filter menggunakan tombol
selected_filter = st.radio('Filter', ['Week', 'Month', 'Year'])

# Filter data berdasarkan pilihan filter
if selected_filter == 'Week':
    filtered_data = filtered_data.groupby(pd.Grouper(key='date', freq='W'))['sales'].mean().reset_index()
elif selected_filter == 'Month':
    filtered_data = filtered_data.groupby(pd.Grouper(key='date', freq='M'))['sales'].mean().reset_index()
elif selected_filter == 'Year':
    filtered_data = filtered_data.groupby(pd.Grouper(key='date', freq='Y'))['sales'].mean().reset_index()

fig = px.line(filtered_data, x='date', y='sales')
st.plotly_chart(fig)

st.markdown("---")

# ////////////////////////////// Sales by Feast Day //////////////

df = data
st.header('Sales Chart by Type of Day')
# Menampilkan filter
selected_hari_raya = st.multiselect('Select Type of Day', df['desc'].unique())
# Filter data berdasarkan hari raya yang dipilih
filtered_data = df[df['desc'].isin(selected_hari_raya)]

# Menampilkan plot
fig = px.bar(filtered_data, x='desc', y='sales')
fig.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig)

st.markdown("---")

# ////////////////////// Sales by Family Product ( Populer / Not Populer) //////////////////


family_sales = data.groupby('family')['sales'].sum().reset_index()

threshold = family_sales['sales'].quantile(0.8)
family_sales['popularity'] = ['Popular' if x >= threshold else 'Not Popular' for x in family_sales['sales']]

# Membuat filter untuk memilih popularitas
st.header('Sales by Family Product ( Popular / Not popular )')
selected_popularity = st.selectbox('Select an option', ['Choose an option', 'Popular', 'Not Popular'])

# Filter berdasarkan popularitas yang dipilih
if selected_popularity != 'All':
    filtered_data = family_sales[family_sales['popularity'] == selected_popularity]
else:
    filtered_data = family_sales

fig = px.bar(filtered_data, x='family', y='sales', color='popularity')
st.plotly_chart(fig)

st.markdown("---")
# *----------------------*---------------------------*

# ////////////////////// Total Sales by Store Type /////////////////

# Membuat filter berdasarkan store_type
filtered_data = data.groupby('store_type')['sales'].sum().reset_index()

# Menampilkan filter
st.header('Total Sales by Store Type')
selected_types = st.multiselect('Choose Store Type', filtered_data['store_type'].unique())
filtered_sales = filtered_data[filtered_data['store_type'].isin(selected_types)]

# Menampilkan plot dengan Plotly
fig = px.bar(filtered_sales, x='store_type', y='sales', labels={'store_type': 'Store Type', 'sales': 'Total Sales'})
st.plotly_chart(fig)
st.markdown("---")
# *-----------------------*----------------------------*
# ////////////////////// Total Sales by Cluster /////////////////

# Membuat filter berdasarkan cluster
filtered_data = data.groupby('cluster')['sales'].sum().reset_index()

# Menampilkan filter
st.header('Total Sales by Cluster')
selected_clusters = st.multiselect('Choose Cluster', filtered_data['cluster'].unique())
filtered_sales = filtered_data[filtered_data['cluster'].isin(selected_clusters)]

# Menampilkan plot dengan Plotly
fig = px.bar(filtered_sales, x='cluster', y='sales', labels={'cluster': 'Cluster', 'sales': 'Total Sales'})
st.plotly_chart(fig)
st.markdown("---")
# *-----------------------*----------------------------*

# ////////////////////// Total Sales by City /////////////////

# Membuat filter berdasarkan city
filtered_data = data.groupby('city')['sales'].sum().reset_index()

# Menampilkan 
st.header('Total Sales by City')
selected_cities = st.multiselect('Choose City', filtered_data['city'].unique())
filtered_sales = filtered_data[filtered_data['city'].isin(selected_cities)]

# Menampilkan plot dengan Plotly
fig = px.bar(filtered_sales, x='city', y='sales', labels={'city': 'City', 'sales': 'Total Sales'})
st.plotly_chart(fig)
st.markdown("---")
# *-----------------------*----------------------------*

# ////////////////////// Total Sales by State /////////////////
# Membuat filter berdasarkan state
filtered_data = data.groupby('state')['sales'].sum().reset_index()

# Menampilkan filter
st.header('Total Sales by State')
selected_states = st.multiselect('Choose State', filtered_data['state'].unique())
filtered_sales = filtered_data[filtered_data['state'].isin(selected_states)]

# Menampilkan plot dengan Plotly
fig = px.bar(filtered_sales, x='state', y='sales', labels={'state': 'State', 'sales': 'Total Sales'})
fig.update_layout(title='Total Sales by State')
st.plotly_chart(fig)
st.markdown("---")
# *-----------------------*----------------------------*

# ////////////////// Prediction //////////////////////

st.header('Prediction for one year ahead')

# Filter berdasarkan 'store_nbr' dan 'family_encode'
selected_store_nbr = st.selectbox('Select Store_nbr', data2['store_nbr'].unique())
selected_family_encode = st.selectbox('Select Family Encode', data2['family_encode'].unique())
filtered_data = data2[(data2['store_nbr'] == selected_store_nbr) & (data2['family_encode'] == selected_family_encode)]

# Menampilkan nilai prediction dengan menggunakan kolom Month
st.dataframe(filtered_data[['store_nbr','family_encode','Month', 'prediction']])
st.markdown("---")
# *-----------------------*----------------------------*
