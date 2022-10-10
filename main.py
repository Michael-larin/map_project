import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import altair as alt

st.set_page_config(layout="wide")
header = st.container()
descrip = st.container()
map = st.container()
change = st.container()

@st.cache(allow_output_mutation=True)
def upload_wonders():
    wonders = pd.read_csv('data/Wonders.csv')
    return wonders
curr_wonders = upload_wonders()

with header:
    st.title('Welcome to my project of Civ5 Wonders on the world map')
    st.text("""The main goal of the project is to allow everyone to track which Wonders of the favourite game they visited.
Everything is shown using Pandas df and Folium maps. 
You can explore the map, check some information about the places and update it with your personal.""")

with descrip:
    st.header('Down below is the dataset used for the project ')
    st.text("""The dataset was created via Pandas and NumPy libriaries.
You can check the process of making this dataset using GitHub page of the project in the 'About' section.
Basically, the information was parsed from web-sites, transformed and then saved as .csv file (simple ETL).
The cahnges you make on the page will be reflected in the 'Visited' column.""")
    st.write(curr_wonders.head())
    show_col, text_col = st.columns(2)
    with show_col:
        "Wonders by Countries"
        bar_chart = alt.Chart(curr_wonders).mark_bar().encode(
        x=alt.X('count(Country):N'),
        y = alt.Y('Country', sort='-x'),
        opacity=alt.value(0.2),
        color=alt.value('blue')
    )
        st.altair_chart(bar_chart, use_container_width=True)
    with text_col:
        st.text("""On the graph to the left there are all the countries that      
you need to visit in order to achive 'Mission complete' badge 
for making the whole map green.
You can start from those which have more Wonders at a time.""")

with change:
    st.header('The best section - Changes')
    st.text("""Here you are making your own story!
Please, choose Wonders that you have already visited in the drop-down menu. These can be multiple places at a time.
After you are done, click the button that will appear below and see the magic!
    """)
    sel_col, reset_col = st.columns(2)
    add_visit = sel_col.multiselect(
    'Which Wonders did you visit?',
    curr_wonders['Wonder'],
    key="multiselect"
    )
    def to_add(visited):
        for n in range(len(visited)):
            curr_wonders.loc[curr_wonders['Wonder'] == visited[n], 'Visited'] = 'Yes'
        return
    with sel_col:
        if add_visit:
            nest_button = st.button('Press to add them on the map')
            if nest_button:
                to_add(add_visit)
    with reset_col: 
        st.text("""Now, when you are the explorer, you can download the file!
You can use this file further to show others where you have been to.
Just click 'Upload' on the left side and browse for your file. 
Carefully check the restrictions!
    """)
        @st.cache
        def convert_df(df):                     # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        csv = convert_df(curr_wonders)
        down_state = st.download_button(
            label = 'Download your dataset .csv', 
            data = csv, 
            file_name = 'Visited Wonders from Civ5.csv', 
            mime='text/csv',
            )
        st.text("""Or, if you want to start from scratch,
simply click 'Reset' and enjoy the map again!
    """)
        reset_but = st.button('Reset')
        if reset_but:
            curr_wonders['Visited'] = 'No'



with map:
    st.header('Please, enjoy the map')
    st.text("""You can explore this map on your own. Each marker has some information regarding the Wonder.""")
    lat = curr_wonders['Latitude']
    lon = curr_wonders['Longitude']
    name = curr_wonders['Address']
    dest = curr_wonders['Destroyed']
    visit = curr_wonders['Visited']
    def color_change(dest, visit):
        if((dest == 'Yes') & (visit == 'No')):
            return('gray')
        elif((visit == 'No') & (dest == 'No')):
            return('red')
        elif(visit == 'Yes'):
            return('green')
    map = folium.Map(location=[30,150], zoom_start = 2, title = 'Stamen', min_zoom=2)
    for lat, lon, name, dest, visit in zip(lat, lon, name, dest, visit):
        folium.Marker(location=[lat, lon], popup=str(name), icon=folium.Icon(color = color_change(dest, visit))).add_to(map) 
    st_data = st_folium(map, width = 2000, height = 500)

