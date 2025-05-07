# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie""")

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on your Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

ingredients_list=st.multiselect(
    label='Choose up to 5 ingredients:',
    options=my_dataframe,
    max_selections=5
)


ingredients_string=''
if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += f'{fruit_chosen} '
        st.subheader(f'{fruit_chosen} Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


my_insert_stmt = f"""
    insert into smoothies.public.orders(ingredients, name_on_order)
    values ('{ingredients_string}', '{name_on_order}')
    """
time_to_insert=st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f'{name_on_order}, your Smoothie is ordered!', icon="✅")

