import pickle
import streamlit as st
from recommendations import get_recommendations


with open('item_similarity.pkl', 'rb') as f:
    item_similarity_df = pickle.load(f)
with open('ratings_matrix.pkl', 'rb') as f:
    ratings_matrix = pickle.load(f)



st.set_page_config(page_title="Product Recommendation Pro", page_icon="🛍")
st.title("Product Recommendation Pro")


#------------------------------------------------------------------------------------------------
# Choose a product name to get recommendations for

user_input = st.text_input("Enter any product")

if st.button("Get Recommendations"):
     get_recommendations(user_input, num_recommendations=10, num_products=10)