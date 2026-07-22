# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Set app title with smoothie emojis
st.title("🥤Customize Your Smoothie!🥤")

# Add the subheader instruction text
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie:')
st.write( 'The name on your Smoothie will be:', name_on_order)

# Active session handling
# session = get_active_session()

# Pull the fruit options dataframe
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Fix: Convert the Snowpark DataFrame column to a clean list for Streamlit to display
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5  # This strictly enforces the "up to 5" rule!
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    
    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')

    # st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! ,{name_on_order}', icon="✅")
