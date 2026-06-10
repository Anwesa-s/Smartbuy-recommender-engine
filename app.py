import html
from pathlib import Path

import streamlit as st
import pandas as pd
import pickle

from utils.recommender import hybrid_recommendations

CSS_PATH = Path(__file__).parent / "assets" / "style.css"


@st.cache_data
def load_css() -> str:
    return CSS_PATH.read_text(encoding="utf-8")


def inject_css() -> None:
    st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)


def render_rec_card(row, rank, max_score):
    score_pct = min(100, (row["hybrid_score"] / max_score) * 100)
    rank_class = "rec-rank rec-rank-gold" if rank == 1 else "rec-rank"
    name = html.escape(str(row["product_name"]))
    return f"""
<div class="rec-card">
    <div class="{rank_class}">{rank}</div>
    <div class="rec-name">{name}</div>
    <div class="rec-meta">
        <span>⭐ {row['rating']:.1f}</span>
        <span>{int(row['rating_count']):,} reviews</span>
    </div>
    <div class="rec-score-label">Match score · {row['hybrid_score']:.2f}</div>
    <div class="rec-score-bar">
        <div class="rec-score-fill" style="width: {score_pct:.0f}%;"></div>
    </div>
</div>
"""

st.set_page_config(
    page_title="SmartBuy Recommender Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

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

# --- Sidebar ---
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <p class="sidebar-brand-title">SmartBuy</p>
            <p class="sidebar-brand-tagline">Hybrid recommendation engine</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="sidebar-section-label">Dataset Overview</p>',
        unsafe_allow_html=True,
    )

    product_count = recommendation_df["product_id"].nunique()
    category_count = recommendation_df["category"].nunique()

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Products</div>
            <div class="stat-value">{product_count:,}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Categories</div>
            <div class="stat-value">{category_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="font-size:0.78rem; color:#64748b; line-height:1.5; margin-top:1rem;">
            Recommendations blend content similarity (70%) with popularity (30%).
        </p>
        """,
        unsafe_allow_html=True,
    )

# --- Main content ---
st.markdown(
    '<h1 class="hero-title">SmartBuy Recommender Engine</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-subtitle">Discover products tailored to your selection using our hybrid recommendation model.</p>',
    unsafe_allow_html=True,
)

selected_product = st.selectbox(
    "Select Product",
    recommendation_df["product_name"],
    index=None,
    placeholder="Search and select a product...",
)

if selected_product:
    product_info = recommendation_df[
        recommendation_df["product_name"] == selected_product
    ].iloc[0]

    st.markdown(
        f"""
        <div class="product-card">
            <p class="product-card-title">{selected_product}</p>
            <span class="product-card-category">{product_info['category']}</span>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-item-label">Rating</div>
                    <div class="metric-item-value">⭐ {round(product_info['rating'], 1)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-item-label">Reviews</div>
                    <div class="metric-item-value">{int(product_info['rating_count']):,}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-item-label">Discount</div>
                    <div class="metric-item-value">{int(product_info['discount_percentage'])}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Get Recommendations", type="primary"):
        with st.spinner("Finding similar products..."):
            recommendations = hybrid_recommendations(
                selected_product,
                recommendation_df,
                cosine_sim,
                indices,
            )

            recommendations = recommendations.sort_values(
                by="hybrid_score",
                ascending=False,
            )

            best_product = recommendations.iloc[0]

            st.markdown(
                f"""
                <div class="top-pick-banner">
                    <div class="top-pick-label">Top Recommendation</div>
                    <div class="top-pick-name">{best_product['product_name']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            display_df = recommendations.copy()
            display_df["product_name"] = display_df["product_name"].str.slice(0, 60)
            display_df["hybrid_score"] = display_df["hybrid_score"].round(2)

            max_score = display_df["hybrid_score"].max()
            if max_score == 0:
                max_score = 1.0

            st.markdown(
                '<p class="section-heading">Recommended Products</p>',
                unsafe_allow_html=True,
            )

            rec_rows = list(display_df.iterrows())
            for row_start in range(0, len(rec_rows), 3):
                cols = st.columns(3, gap="medium")
                for col_idx, col in enumerate(cols):
                    item_idx = row_start + col_idx
                    if item_idx >= len(rec_rows):
                        break
                    _, row = rec_rows[item_idx]
                    rank = item_idx + 1
                    with col:
                        st.markdown(
                            render_rec_card(row, rank, max_score),
                            unsafe_allow_html=True,
                        )

else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">🔍</div>
            <div class="empty-state-title">Select a product to get started</div>
            <div class="empty-state-text">
                Search and choose a product above.<br>
                We'll surface the best matches from our catalog.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
