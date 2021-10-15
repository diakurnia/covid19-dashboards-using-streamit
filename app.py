import pandas as pd
import streamlit as st
# import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import graph_objs as go

st.title('Indonesia Covid-19 Dashboard')

def get_data_from_csv():
    df = pd.read_csv('data/covid19.csv')
    return df

df = get_data_from_csv()

# ---sidebar---
st.sidebar.write('Pilih Jenis Data:')
option_1 = st.sidebar.checkbox('Total Kasus')
option_2 = st.sidebar.checkbox('Kasus Harian')
option_3 = st.sidebar.checkbox('Total Sembuh')
option_4 = st.sidebar.checkbox('Sembuh Harian')
option_5 = st.sidebar.checkbox('Total Meninggal')
option_6 = st.sidebar.checkbox('Meninggal Harian')

nums = st.sidebar.slider('Pilih jumlah provinsi', 5,35,15)

def plot_raw_data():
    fig = go.Figure()
    if option_1:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['total_kasus'], name='Total Kasus'))
    if option_2:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['kasus_harian'], name='Kasus Harian'))
    if option_3:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Sembuh'], name='Total Sembuh'))
    if option_4:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['sembuh_baru'], name='Sembuh Harian'))
    if option_5:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Meninggal'], name='Total Meninggal'))
    if option_6:
        fig.add_trace(go.Scatter(x=df['Date'], y=df['meninggal_baru'], name='Meninggal Harian'))
    fig.layout.update(title_text='Dynamic of Indonesia Covid-19', xaxis_rangeslider_visible=True, hovermode='x')
    st.plotly_chart(fig)

plot_raw_data()

## Vaccination
df_vaccinated = df[['Date', 'dosis_pertama', 'dosis_kedua', 'total_kasus']].loc[304:]

graph1 = go.Scatter(
               hoverinfo='skip', 
               x=df_vaccinated['Date'], 
               y=df_vaccinated['dosis_pertama'],  
               fill ='tozeroy',
               hovertemplate='<b>%{x}</b><br>' + '<b>Total Vaksin Pertama: </b>'+'%{y}<extra></extra>', 
               marker_color='#DC143C', 
               name='Total Vaksin Pertama'
    ) 

graph2 = go.Scatter(
               hoverinfo='skip', 
               x=df_vaccinated['Date'], 
               y=df_vaccinated['dosis_kedua'], 
               fill ='tozeroy',
               hovertemplate='<b>%{x}</b><br><b>Total Vaksin Kedua: </b>%{y}<extra></extra>', 
               marker_color='#0d8c68', 
               name='Total Vaksin Kedua'
    ) 

data = [graph1, graph2]
fig = go.Figure(data)

# Updating the chart settings when displaying
fig.update_layout(
    title='Total Kumulatif Vaksinasi Covid-19 in Indonesia', 
    xaxis_title='Time Periode', 
    yaxis_title='Count', 
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x', 
    legend_orientation='h',
    width=700,
    height=500,
)

# Displaying the graph
st.plotly_chart(fig)

# handling province plot
df_profince = df.iloc[:,1:35]
def top_province(sort, n_province=15):
    top = df_profince.sum().reset_index().rename(columns={
                       'index': 'Provinsi',
                       0:'Total Kasus'}).sort_values(by='Total Kasus', ascending=sort).head(n_province)
    ### Generate a Barplot
    fig = plt.figure(figsize=(15,10))
    plot = sns.barplot(top['Total Kasus'], top['Provinsi'])
    for i,(value,name) in enumerate(zip(top['Total Kasus'],top['Provinsi'])):
        plot.text(value,i-0.05,f'{value:,.0f}',size=15)
    plt.title('Jumlah Kasus Covid-19 Per-provinsi')
    st.pyplot(fig)

top_province(False, nums)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)