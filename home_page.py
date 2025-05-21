import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Config
st.set_page_config(page_title="Product Recommendation System", layout="wide", page_icon="🛍️")

# other files for run this project
from product_details import get_product_description
from style import load_custom_css


df = pd.read_csv("productdata.csv")

# for all the image resize
def display_resized_image(image_url, size="300px"):
    if isinstance(image_url, str) and image_url.strip().lower().startswith("http"):
        st.markdown(
            f"""
            <img src="{image_url}" style="width: {size}; height: {size}; object-fit: cover; border-radius: 12px;" />
            """,
            unsafe_allow_html=True,
        )


# query parameters
query = st.query_params
selected_product_name = query.get("product", None)


st.markdown(load_custom_css(), unsafe_allow_html=True)


# ----------------- It's Show One Product Per Category -----------------
if not selected_product_name:

    st.markdown("### 🔍 Browse Products by Category")
    if 'scroll_indices' not in st.session_state:
        st.session_state.scroll_indices = {}

    max_items = 4 # shows four products on home page
    for category in sorted(df['Category'].dropna().unique()):
        st.markdown(f"### 🗂️ {category}")
        cat_df = df[df['Category'] == category].reset_index(drop=True)
        total_items = len(cat_df)
        cat_key = f"scroll_{category}"
        current_index = st.session_state.scroll_indices.get(cat_key, 0)

        left_col, prod_col, right_col = st.columns([1, 10, 1])

        with left_col:
            if st.button("◀", key=f"left_{category}"):
                st.session_state.scroll_indices[cat_key] = max(0, current_index - 1)

        with prod_col:
            cols = st.columns(max_items)
            for i in range(current_index, min(current_index + max_items, total_items)):
                with cols[i - current_index]:
                    row = cat_df.iloc[i]
                    st.markdown(f"""
                                <form action="" method="get">
                                    <input type="hidden" name="product" value="{row['Product']}">
                                    <button type="submit" style="all: unset; cursor: pointer;">
                                        <div class="product-card">
                                            <img src="{row['image']}" class="product-card-img" />
                                            <div class="product-title">{row['Product']}</div>
                                        </div>
                                    </button>
                                </form>
                            """, unsafe_allow_html=True)

        with right_col:
            if st.button("▶", key=f"right_{category}"):
                st.session_state.scroll_indices[cat_key] = min(total_items - max_items, current_index + 1)
# -------------------------- Up to Here -------------------------------



# ----------------- Show Selected Product and Recommendations -----------------
else:
    selected_df = df[df['Product'] == selected_product_name]
    if selected_df.empty:
        st.error("Product not found.")
        st.stop()

    selected_product = selected_df.iloc[0]

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown("### 🎯 Selected Product")
        if isinstance(selected_product['image'], str) and selected_product['image'].strip().lower().startswith("http"):
            st.image(selected_product['image'], width=300)
        st.markdown(f"#### {selected_product['Product']}")
        st.markdown(f"**Category:** {selected_product['Category']}")
        if st.button("🔙 Back to Products"):
            del st.query_params["product"]
            st.rerun()

    with right_col:
        st.markdown("### 📋 Product Description")
        description = get_product_description(selected_product['Product'])

        # -------------------- for selected product detailed description-----------------
        st.markdown("""
        <style>
        .bullet-box {
            background-color: #f0f8ff;
            padding: 20px;
            border-left: 5px solid #007acc;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .bullet-box ul {
            list-style-type: none;
            padding-left: 0;
        }
        .bullet-box li {
            position: relative;
            padding-left: 28px;
            margin-bottom: 12px;
            font-size: 16px;
            line-height: 1.6;
            color: #2c3e50;
        }
        .bullet-box li::before {
            content: " ";
            position: absolute;
            left: 0;
            top: 0;
            color: #007acc;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        # -------------- up to Here -------------------


        if isinstance(description, list):
            html = "<div class='bullet-box'><ul>"
            for point in description:
                html += f"<li>{point}</li>"
            html += "</ul></div>"
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bullet-box'>{description}</div>", unsafe_allow_html=True)

    # ---------------- Code for Recommendations ----------------
    st.markdown("---")
    st.markdown("### 🔁 You May Also Like")
    same_cat_df = df[df['Category'] == selected_product['Category']].reset_index(drop=True)
    recommended = pd.DataFrame()

    if len(same_cat_df) > 1:
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(same_cat_df['Description'])
        selected_vector = vectorizer.transform([selected_product['Description']])
        cosine_sim = cosine_similarity(selected_vector, tfidf_matrix).flatten()
        selected_idx = same_cat_df[same_cat_df['Product'] == selected_product['Product']].index[0]
        similar_idx = cosine_sim.argsort()[::-1]
        similar_idx = [i for i in similar_idx if i != selected_idx][:3]
        recommended = same_cat_df.iloc[similar_idx]


    if recommended.empty:
        st.info("🤔 No similar products found in this category.")
    else:
        rec_cols = st.columns(3)
        for i, (_, rec) in enumerate(recommended.iterrows()):
            with rec_cols[i % 3]:
                st.markdown(f"""
                    <form action="" method="get">
                        <input type="hidden" name="product" value="{rec['Product']}">
                        <button type="submit" style="all: unset; cursor: pointer;">
                            <div class="product-card">
                                <img src="{rec['image']}" class="product-card-img" />
                                <div class="product-title">{rec['Product']}</div>
                            </div>
                        </button>
                    </form>
                """, unsafe_allow_html=True)
