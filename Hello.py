import streamlit as st

st.set_page_config(layout="wide", page_title = 'Welcome page')

header = st.container()
descrip = st.container()
about = st.container()

with header:
    st.title('Welcome to my Maps project')
    st.text("""The main goal of the project is to apply obtained knoweledge and most recent technologies.
The project consists of two map. Each of them represents passion of me and my friends.
Each page is made using different techniques described down below.
To navigate around the project, please, use pages in the sidebar menu.
Enjoy your time!""")

with descrip:
    st.header('Description of the project')
    st.text("""Map project is made up of two separate maps. The goal is to make maps stay alive and interactive:
    1) A world map with pointed World Wonders from Civilazation 5 game
    2) A world map with countries painted in different colors based on conditions aka World Scratch map
The second goal of the project is to use as many tools of getting data and techniques of transforming it as possible.
The whole website is based on Python and here is the list of libriaries used to accomplish the task:
    1) Pandas - used for complex math nad work with Dataframes. The base of the project
    2) NumPy - coputational functions of some data
    3) GeoPandas - used for Dataframes with geological meaning which include latitude and longitude params
    4) Folium - drawing of maps in real time
    5) Altair - drawing Data charts
    6) Random - randomizing values
    7) Streamlit - the main engine for web visualazation of the project
Data sources:
    1) HTML parsing for World Wonders from Civilazation 5
    2) CSV uploading for both maps
    3) JSON analizing for World Scratch map
    4) GEOJSON parsing for World Scratch map
All data transformation and testing is done through Jupyter. You can check all the notebooks on Github.
There are also some ways of overcoming issues raised during accomplishment of the project.""")
    
with about:
    st.header('About the creator')
    st.text('My name is Michael.')
    link1 = '[Link to GitHub](https://github.com/Michael-larin)'
    st.markdown(link1,unsafe_allow_html=True)
    link2 = '[Link to the project on GitHub](https://github.com/Michael-larin/map_project)'
    st.markdown(link2,unsafe_allow_html=True)