import streamlit as st
from snowflake.snowpark.functions import col


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
my_dataframe = session.table("smoothies.public.fruit_options") \
    .select(col('FRUIT_NAME')) \
    .to_pandas()

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
