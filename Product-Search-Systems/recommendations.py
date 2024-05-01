import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz, process
import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

# Load and preprocess data
data = pd.read_csv(r"C:\Users\tejva\PycharmProjects\pythonProject\Amazon-Products.csv")

# Fill NaN values in 'ratings' and 'no_of_ratings' columns with zeros
data['ratings'].fillna(0, inplace=True)
data['no_of_ratings'].fillna(0, inplace=True)

# Convert 'ratings' column to numeric
data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')

# Convert 'name' and 'sub_category' columns to strings
data['name'] = data['name'].astype(str)
data['sub_category'] = data['sub_category'].astype(str)

# Pivot the data to create the ratings utility matrix
ratings_matrix = data.pivot_table(values='ratings', index='name', columns='sub_category', fill_value=0)

# Calculate the cosine similarity between items (sub_categories)
item_similarity = cosine_similarity(ratings_matrix.T)

# Create a DataFrame with item similarity
item_similarity_df = pd.DataFrame(item_similarity, index=ratings_matrix.columns, columns=ratings_matrix.columns)


# Define the get_recommendations function
def get_recommendations(product_name, num_recommendations=5, num_products=10):
    # Handle spelling mistakes using fuzzy matching
    best_match, score = process.extractOne(product_name, item_similarity_df.index)

    similar_scores = item_similarity_df[best_match]
    similar_sub_categories = similar_scores.sort_values(ascending=False).index.tolist()

    # Get the exact sub-category that the input product belongs to
    exact_sub_category = process.extractOne(product_name, item_similarity_df.index)[0]

    # Display some products from the exact sub-category
    sub_category_products = data[data['sub_category'] == exact_sub_category].nlargest(num_products, 'ratings')
    st.write(f"Best rated products from '{exact_sub_category}':")
    for j, row in sub_category_products.iterrows():
        st.write(f"->: {row['name']}")

        image_url = row['image']

        # Check if the image URL is valid and handle potential issues when opening the image
        try:
            response = requests.get(image_url)
            # Verify that the request was successful and the content is an image
            if response.status_code == 200 and "image" in response.headers["content-type"]:
                img = Image.open(BytesIO(response.content))

                st.image(img, use_column_width=True)
            else:
                raise Exception("Invalid image URL or response.")
        except Exception as e:
            st.write(f"Error loading image: {e}")
            img = Image.new("RGB", (100, 100))  # Create a default image

    # Display top recommended sub-categories
    st.write(f"\nTop Recommended Sub-Categories for '{product_name}':")
    for i, sub_category in enumerate(similar_sub_categories[:num_recommendations]):
        st.write(f"{i + 1}: {sub_category}")


# Set up Streamlit UI components
st.title("Amazon Product Recommendation System")
product_name_input = st.text_input("Enter a product name:")
if st.button("Get Recommendations"):
    get_recommendations(product_name_input)