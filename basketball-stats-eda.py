import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as numpy
from scrape_data import *
from datetime import date
from PIL import Image

title_container = st.beta_container()
col1, col2 = st.beta_columns([1, 5])
image = Image.open('assets/logo.jpg')
with title_container:
    with col1:
        st.image(image)
    with col2:
        st.write('# NBA Stats Explorer\n' + 'by Mayur Machhi')

#Title and other information
st.markdown("""
This app shows NBA player stats data!\n
**Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

#User input on sidebar - Year Selection
st.sidebar.header('User Input Features')
current_year = date.today().year
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,current_year+1))))

playerstats = scrape_data(selected_year)

#Sidebar Team Selection
teams_sorted = sorted(playerstats['Tm'].unique())
team_selected = st.sidebar.multiselect('Team', teams_sorted, teams_sorted)

#Sidebar Position Selection
unique_pos = ['C','PF','SF','PG','SG', 'PF-SF', 'SF-SG', 'SG-PF', 'C-PF',
       'SG-SF']
pos_selected = st.sidebar.multiselect('Position', unique_pos, unique_pos)



#Filtering Data
filtered_df = playerstats[(playerstats['Tm'].isin(team_selected)) & (playerstats['Pos'].isin(pos_selected))]
# Download NBA player stats data as csv
st.sidebar.markdown(filedownload(filtered_df), unsafe_allow_html=True)

# Display Data
st.header("Players Stats")
st.write('Data Dimension: ' + str(filtered_df.shape[0]) + ' rows and ' + str(filtered_df.shape[1]) + ' columns.')
# Download NBA player stats data as csv
st.markdown(filedownload(filtered_df), unsafe_allow_html=True)

st.dataframe(filtered_df)



# Show Acronyms table in expander
my_expander = st.beta_expander('Data Acronyms')
with my_expander:
	st.write("""
Acronym | Description
---|---
Rk | Rank
Pos | Position
Age | Player's age on February 1 of the season
Tm | Team
G | Games
GS | Games Started
MP | Minutes Played Per Game
FG | Field Goals Per Game
FGA | Field Goal Attempts Per Game
FG% | Field Goal Percentage
3P | 3-Point Field Goals Per Game
3PA | 3-Point Field Goal Attempts Per Game
3P% | FG% on 3-Pt FGAs.
2P | 2-Point Field Goals Per Game
2PA | 2-Point Field Goal Attempts Per Game
2P% | FG% on 2-Pt FGAs.
eFG% | Effective Field Goal Percentage 
&nbsp | (Note: This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal.)
FT | Free Throws Per Game
FTA | Free Throw Attempts Per Game
FT% | Free Throw Percentage
ORB | Offensive Rebounds Per Game
DRB | Defensive Rebounds Per Game
TRB | Total Rebounds Per Game
AST | Assists Per Game
STL | Steals Per Game
BLK | Blocks Per Game
TOV | Turnovers Per Game
PF | Personal Fouls Per Game
PTS | Points Per Game
	""")

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