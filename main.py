import streamlit as st
import resturent_name_menu_gen

st.title("Restaurant Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Pakistani", "Italian", "Mexican", "Arabic", "American"))

if cuisine:
    response = resturent_name_menu_gen.generate_rest_name_item(cuisine)
    st.header(response['restaurant_name'].strip())
    menu_items = response['menu_items'].strip().split(",")
    st.write("**Menu Items**")
    for item in menu_items:
        st.write("-", item)