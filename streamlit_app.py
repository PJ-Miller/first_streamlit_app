import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega-3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.dataframe(fruits_to_show)

# created repeatable code
def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())    
    return fruityvice_normalized

# new header
streamlit.header('Fruityvice Fruit Advise!')

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruitvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

# streamlit.write('The user entered ', fruit_choice)

# makes API request
# writes data on streamlit
# streamlit.text(fruityvice_response.json())

# take the json version of the response and normalize it

# https://firstappapp-efxxxxdckshlipczxc3xgx.streamlit.app/


streamlit.header("The fruit load list contains:")
# Snowflake-related functions 
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Select * from fruit_load_list")
        my_cur.fetchall()

# Add button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

streamlit.stop()

# Allow the end user to add a fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add','jackfruit')
my_cnx.cursor().execute(f"insert into fruit_load_list values ('{add_my_fruit}')")
streamlit.text('Thanks for adding ' + add_my_fruit)
