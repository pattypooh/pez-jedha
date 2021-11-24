import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title='Kayak')

import pandas as pd
from src.models import predict_model

st.title('Kayak : Check the best city the next 7 days')
# Left Sidebar 
#st.sidebar.write('# Kayak')
st.markdown("Welcome to this in-depth introduction to [...].")
# Loading the image
main_img = Image.open('./kayak.png')
st.image(main_img, width=100)

cities_df = pd.read_csv('items2.csv')
st.subheader('Cities')
st.write(cities_df)
#st.sidebar.write('# Start using the app by checking how products we eat impact the environnement')

select_city = st.multiselect('Sélect a city where you would like to go', ['City 1','City 2', 'City 3', 'City 4'] )
st.write('You selected:', select_city)

st.subheader('Some graphics in seaborn')
plt.figure(figsize=(10, 8))
fig, ax = plt.subplots()
ax = sns.histplot(cities_df['item_category'])
plt.xlabel('Categories')
st.pyplot(fig)

st.subheader('Pie chart')
plt.figure(figsize=(10, 8))

options = st.sidebar.radio('Select a page:', 
    ['Home', 'Header Information', 'Data Information', 'Data Visualisation', 'Missing Data Visualisation'])


#Right Sidebar (main page)








