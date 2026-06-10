import pandas as pd

def hybrid_recommendations(
    product_name,
    recommendation_df,
    cosine_sim,
    indices,
    top_n=10
):

    idx = indices[product_name]

    similarity_scores = list(
        enumerate(cosine_sim[idx])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[1:51]

    recommendations = []

    for i, sim_score in similarity_scores:

        popularity = recommendation_df.loc[
            i,
            'normalized_popularity'
        ]

        hybrid_score = (
            0.7 * sim_score
            +
            0.3 * popularity
        )

        recommendations.append(
            (
                i,
                hybrid_score
            )
        )

    recommendations = sorted(
        recommendations,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = recommendations[:top_n]

    product_indices = [
        i[0]
        for i in recommendations
    ]

    scores = [
        i[1]
        for i in recommendations
    ]

    results = recommendation_df.iloc[
        product_indices
    ][
        [
            'product_name',
            'rating',
            'rating_count'
        ]
    ].copy()

    results['hybrid_score'] = scores

    return results