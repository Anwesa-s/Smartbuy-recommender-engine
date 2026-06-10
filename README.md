# SmartBuy Recommender Engine

## Day 1 Findings

- Dataset contains 1465 reviews.
- Dataset contains 1351 unique products.
- Dataset contains 1194 unique users.
- No duplicate rows found.
- Only 2 missing values in rating_count.
- Average rating: ___
- Most common category: ___
- Most reviewed product: ___

# Day 2 Summary

## Data Cleaning

- Converted discounted_price to numeric.
- Converted actual_price to numeric.
- Converted discount_percentage to numeric.
- Converted rating to numeric.
- Converted rating_count to numeric.
- Handled all missing values.

## Feature Engineering

Created:

1. discount_amount
2. discount_ratio
3. popularity_score

## Output

Saved cleaned dataset as:

cleaned_amazon.csv

# Day 5 Summary

Built a Popularity-Based Recommendation System.

Features:
- Top Product Recommendations
- Category-Based Recommendations
- Popularity Rankings

Metrics Used:
- Rating
- Rating Count
- Popularity Score

# Day 6 Summary

Built a Hybrid Recommendation System.

Combined:

1. Content-Based Filtering
2. Popularity-Based Filtering

Hybrid Score:

0.7 × Similarity Score
+
0.3 × Popularity Score

Benefits:
- More relevant recommendations
- More popular recommendations
- Better recommendation quality

# Day 7 Summary

## Objective

Evaluate the performance and behavior of the recommendation system.

## Analyses Performed

- Top Rated Product Analysis
- Rating vs Rating Count Analysis
- Correlation Analysis
- Recommendation Quality Evaluation

## Key Findings

- Product popularity is strongly associated with review count.
- Most products maintain ratings between 3.5 and 4.5.
- Hybrid recommendations provide a better balance between relevance and popularity.
- Content-based similarity works effectively using product descriptions and category information.

## Outcome

The evaluation confirmed that the Hybrid Recommendation System produces relevant and practical product recommendations while maintaining recommendation diversity.