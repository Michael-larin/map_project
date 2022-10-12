import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
import geopandas as gpd

st.set_page_config(layout="wide", page_title = 'World map')

# Perform @cache function to avoid reading data each time
@st.cache(allow_output_mutation=True)
def upload_countries():
    countries = pd.read_csv('data/Country.csv')
    countries = countries.drop(columns=['TableName', 'LongName', 'Alpha2Code', 'CurrencyUnit', 'SpecialNotes', 'Region', 'IncomeGroup', 'Wb2Code',
       'NationalAccountsBaseYear', 'NationalAccountsReferenceYear',
       'SnaPriceValuation', 'LendingCategory', 'OtherGroups',
       'SystemOfNationalAccounts', 'AlternativeConversionFactor',
       'PppSurveyYear', 'BalanceOfPaymentsManualInUse',
       'ExternalDebtReportingStatus', 'SystemOfTrade',
       'GovernmentAccountingConcept', 'ImfDataDisseminationStandard',
       'LatestPopulationCensus', 'LatestHouseholdSurvey',
       'SourceOfMostRecentIncomeAndExpenditureData',
       'VitalRegistrationComplete', 'LatestAgriculturalCensus',
       'LatestIndustrialData', 'LatestTradeData'])
    countries['Visited'] = 1
    return countries
countries_df = upload_countries()

# Perform @cache function to avoid reading data each time
@st.cache(allow_output_mutation=True)
def upload_world():
    world = gpd.read_file('data/world.geojson')
    world.loc[world['ADM0_A3'] == 'AND', 'ADM0_A3'] = 'ADO'
    world.loc[world['ADM0_A3'] == 'COD', 'ADM0_A3'] = 'ZAR'
    world.loc[world['ADM0_A3'] == 'IMN', 'ADM0_A3'] = 'IMY'
    world.loc[world['ADM0_A3'] == 'KOS', 'ADM0_A3'] = 'KSV'
    world.loc[world['ADM0_A3'] == 'PSX', 'ADM0_A3'] = 'WBG'
    world.loc[world['ADM0_A3'] == 'ROU', 'ADM0_A3'] = 'ROM'
    world.loc[world['ADM0_A3'] == 'SDS', 'ADM0_A3'] = 'SSD'
    world.loc[world['ADM0_A3'] == 'TLS', 'ADM0_A3'] = 'TMP'
    geo = gpd.GeoSeries(world.set_index('ADM0_A3')['geometry']).to_json()
    return geo
geo = upload_world()


header = st.container()
descrip = st.container()
map = st.container()
change = st.container()

# First container - introduction to the page
with header:
    st.title('World Scratch map')
    st.text("""It was always a dream to visit all countries, now We can track it online!
To get the idea of where data came from, please check the notebook with tha same name on Github.
GeoPandas parsing -> Data transformation and cleaning -> DF to JSON -> Testing""")

# Second container - data description
with descrip:
    st.header('Down below is the dataset used for the project ')
    st.text("""The dataset was created via Pandas and NumPy libriaries.
You can check the process of making this dataset using GitHub page of the project in the 'About' section.
Basically, the information was parsed using GeoPandas and and transformed to JSON.
The cahnges you make on the page will be reflected in the 'Visited' column.
The way coloring works is using numbers between 0 and 1. 1 is not visited  and yellow, others are random colored.""")
    st.write(countries_df.head(3))

# Third container - data changes to DF
with change:
    st.header('The best section - Changes')
    st.text("""Here you are making your own story!
Please, choose Wonders that you have already visited in the drop-down menu. These can be multiple places at a time.
After you are done, click the button that will appear below and see the magic!
    """)
    sel_col, reset_col = st.columns(2)
    add_visit = sel_col.multiselect(
        'Which Wonders did you visit?',
        countries_df['ShortName'],
        key="multiselect"
    )

    def to_add(visited):
        random.seed(30)
        for n in range(len(visited)):
            countries_df.loc[countries_df['ShortName'] == visited[n], 'Visited'] = random.uniform(0, 0.8)
        return
    with sel_col:
        if add_visit:
            nest_button = st.button('Press to add them on the map')
            if nest_button:
                to_add(add_visit)
    with reset_col: 
        st.text("""Now, when you are the explorer, you can download the file!
You can use this file further to show others where you have been to."""
#Just click 'Upload' on the left side and browse for your file. 
#Carefully check the restrictions!
    )
        @st.cache
        def convert_df(df):                     # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        csv = convert_df(countries_df)

        down_state = st.download_button(
            label = 'Download your dataset .csv', 
            data = csv, 
            file_name = 'Visited countries.csv', 
            mime='text/csv',
            )
        st.text("""Or, if you want to start from scratch,
simply click 'Reset' and enjoy the map again!
    """)
        reset_but = st.button('Reset')
        if reset_but:
            countries_df['Visited'] = 1

# Forth container - Map itself
with map:
    st.header('Please, enjoy the map')
    st.text("""You can explore this map on your own. If you haven't entered any countries, the map is purple.
After you input your first country, visited one will be colored other than yellow. Yellow are those which are unvisited.""")
    map = folium.Map(location=[30,150], zoom_start = 2, min_zoom=2)
    folium.Choropleth(
        geo_data = geo,
        data = countries_df,
        columns = ['CountryCode', 'Visited'],
        key_on='feature.id',
        fill_color='Set1',
        fill_opacity=0.5,
        line_opacity=0.8
        ).add_to(map)
    st_data = st_folium(map, width = 2000, height = 500)
