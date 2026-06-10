import streamlit as st
import pandas as pd
import pickle

from utils.recommender import hybrid_recommendations
st.set_page_config(
    page_title="SmartBuy Recommender Engine",
    layout="wide"
)

st.markdown("""
<style>

h1{
    color:#14B8A6;
}

h2,h3{
    color:#2DD4BF;
}

</style>
""", unsafe_allow_html=True)

st.title("🛒 SmartBuy Recommender Engine")

recommendation_df = pd.read_csv(
    "data/recommendation_dataset.csv"
)
with open(
    "models/cosine_sim.pkl",
    "rb"
) as f:
    cosine_sim = pickle.load(f)

with open(
    "models/indices.pkl",
    "rb"
) as f:
    indices = pickle.load(f)

st.sidebar.markdown(
    "## 🛒 SmartBuy Recommender"
)

st.sidebar.markdown(
    "## 📊 Dataset Stats"
)

st.sidebar.metric(
    "Products",
    recommendation_df['product_id'].nunique()
)

st.sidebar.metric(
    "Categories",
    recommendation_df['category'].nunique()
)

selected_product = st.selectbox(
    "Select Product",
    recommendation_df['product_name'],
    index=None,
    placeholder="🔍 Search and select a product..."
)
if selected_product:
    product_info = recommendation_df[
        recommendation_df['product_name']
        ==
        selected_product
    ].iloc[0]

    st.markdown(
        f"### 📦 {selected_product}"
    )

    st.subheader("Selected Product")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⭐ Rating",
            round(product_info['rating'],1)
        )

    with col2:
        st.metric(
            "📝 Reviews",
            f"{int(product_info['rating_count']):,}"
        )

    with col3:
        st.metric(
            "💸 Discount",
            f"{int(product_info['discount_percentage'])}%"
        )

    st.info(
        f"Category: {product_info['category']}"
    )

    if st.button("🚀 Get Recommendations"):

        with st.spinner(
        "🔍 Finding similar products..."
    ):

          recommendations = hybrid_recommendations(
            selected_product,
            recommendation_df,
            cosine_sim,
            indices
        )

        # Sort recommendations
        recommendations = recommendations.sort_values(
            by='hybrid_score',
            ascending=False
        )

        # Top recommendation
        best_product = recommendations.iloc[0]

        st.success(
            f"🏆 Top Recommendation: {best_product['product_name']}"
        )

        # Create display dataframe
        display_df = recommendations.copy()

        # Shorten long names
        display_df['product_name'] = (
            display_df['product_name']
            .str.slice(0, 60)
        )

        # Round scores
        display_df['hybrid_score'] = (
            display_df['hybrid_score']
            .round(2)
        )

        # Rename columns
        display_df = display_df.rename(
            columns={
                'product_name': 'Product',
                'rating': 'Rating',
                'hybrid_score': 'Recommendation Score'
            }
        )

        st.subheader("📋 Recommended Products")

        # Hide dataframe index
        st.dataframe(
            display_df[
                [
                    'Product',
                    'Rating',
                    'Recommendation Score'
                ]
            ],
            use_container_width=True,
            hide_index=True
        )
    st.markdown("---")
