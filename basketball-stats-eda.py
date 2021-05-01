import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as numpy
import time

#Title and other information
st.title('NBA Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

#User input on sidebar - Year Selection
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

#Scrape data
@st.cache
def load_data(year=2019):
	url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
	html = pd.read_html(url, header = 0)
	df = html[0]
	df.drop(df[df.Age == 'Age'].index, inplace=True)
	df.fillna(0, inplace=True)
	playerstats = df.drop(['Rk'], axis=1)
	time.sleep(5)
	return playerstats
playerstats = load_data(selected_year)

#Sidebar Team Selection
teams_sorted = sorted(playerstats['Tm'].unique())
team_selected = st.sidebar.multiselect('Team', teams_sorted, teams_sorted)

#Sidebar Position Selection
unique_pos = ['C','PF','SF','PG','SG', 'PF-SF', 'SF-SG', 'SG-PF', 'C-PF',
       'SG-SF']
pos_selected = st.sidebar.multiselect('Position', unique_pos, unique_pos)

#Filtering Data
filtered_df = playerstats[(playerstats['Tm'].isin(team_selected)) & (playerstats['Pos'].isin(pos_selected))]

# Display Data
st.header("Players Stats")
st.write('Data Dimension: ' + str(filtered_df.shape[0]) + ' rows and ' + str(filtered_df.shape[1]) + ' columns.')
st.dataframe(filtered_df)

# Download NBA player stats data as csv
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
#     href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
#     return href

# st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
# if st.button('Intercorrelation Heatmap'):
#     st.header('Intercorrelation Matrix Heatmap')
#     df_selected_team.to_csv('output.csv',index=False)
#     df = pd.read_csv('output.csv')

#     corr = df.corr()
#     mask = np.zeros_like(corr)
#     mask[np.triu_indices_from(mask)] = True
#     with sns.axes_style("white"):
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
#     st.pyplot()