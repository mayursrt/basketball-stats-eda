import pandas as pd
import streamlit as st
import time
import base64
from datetime import date

current_year = date.today().year

#Scrape data
@st.cache
def scrape_data(year=current_year):
	url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
	html = pd.read_html(url, header = 0)
	df = html[0]
	df.drop(df[df.Age == 'Age'].index, inplace=True)
	df.fillna(0, inplace=True)
	playerstats = df.drop(['Rk'], axis=1)
	time.sleep(5)
	return playerstats

# Download data as .csv file
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download as .csv</a>'
    return href