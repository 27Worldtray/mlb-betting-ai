import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon of the page
st.set_page_config(
    page_title='MLB Betting AI',
    page_icon=':earth_americas:',
)

# ------------------------------------------------------------
# Declare useful functions
@st.cache_data
def get_mlb_data():
    """Load MLB game data from a CSV or API."""
    DATA_FILENAME = Path(__file__).parent / 'data' / 'mlb_data.csv'

    try:
        df = pd.read_csv(DATA_FILENAME)
    except FileNotFoundError:
        st.error("MLB data file not found.")
        return pd.DataFrame()

    return df


# ------------------------------------------------------------
# Draw the actual page

# Set the main title and intro text
st.markdown("""
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD).
Notice, the data only goes to 2022 right now, but it's otherwise a great (and did I mention free?) resource!
""")

st.markdown("")

# Load the data
gdp_df = get_mlb_data()

if gdp_df.empty:
    st.stop()

# Year slider
min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=(min_value, max_value)
)

# Country selector
countries = gdp_df['Country Code'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
)

# Optional: Filter the data based on user input
filtered_df = gdp_df[
    (gdp_df['Year'] >= from_year) &
    (gdp_df['Year'] <= to_year) &
    (gdp_df['Country Code'].isin(selected_countries))
]

st.dataframe(filtered_df)