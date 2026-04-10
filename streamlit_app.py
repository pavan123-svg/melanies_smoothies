import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# ✅ Correct connection (SniS)
cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# ✅ Input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# ❌ REMOVE get_active_session() (WRONG)
# session = get_active_session()

# ✅ Fetch data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')) \
    .select(col('FRUIT_NAME')) \
    .to_pandas()

pd_df = my_dataframe.to_pandas()
search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)

# ✅ Show data
st.dataframe(data=my_dataframe, use_container_width=True)

# ✅ Multiselect needs list
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

# ✅ Process selection
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # ✅ Button
    if st.button('Submit Order'):

        # ✅ SAFE INSERT (parameterized query)
        session.sql(
            "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)",
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


# New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
