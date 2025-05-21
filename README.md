# Product-Recommendation-System
A visually appealing product recommendation system built with Streamlit. Users can browse products by category, view detailed descriptions, and receive smart recommendations based on product descriptions using NLP techniques.
# Features
- Category-wise product browsing with image thumbnails
- Detailed view of selected product with stylized description
- Content-based recommendation using TF-IDF and cosine similarity
- Responsive UI with scrollable sections and custom CSS styling
# Recommendation Logic
This project uses:
- `TfidfVectorizer` to vectorize product descriptions
- `cosine_similarity` to compute similarity
- Shows top 3 most similar items in the same category
# Project Structure
- app.py # Main Streamlit app
- product_details.py # Contains product descriptions
- style.py # Custom CSS loader
- productdata.csv # Product data file
- requirements.txt
- README.md
