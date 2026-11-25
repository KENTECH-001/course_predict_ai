
import joblib
import numpy as np
import pandas as pd
from pathlib import Path


# Get the model directory
MODEL_DIR = Path(__file__).resolve().parent / "ml_models"

# Load saved files
courses = joblib.load(MODEL_DIR / "courses_df.joblib")
sim = joblib.load(MODEL_DIR / "sim.joblib")


def recommend_courses(course_id, difficulty=None, n=10):

    # Validate course index
    if course_id < 0 or course_id >= len(courses):
        return []

    # Get similarity scores for selected course
    scores = sim[course_id]

    # Sort courses by similarity
    similar_indices = np.argsort(scores)[::-1]

    # Remove the selected course itself
    similar_indices = [
        idx for idx in similar_indices if idx != course_id
    ]

    # Keep the top 50 candidates
    similar_indices = similar_indices[:50]

    # Remove courses with zero similarity
    similar_indices = [
        idx for idx in similar_indices if scores[idx] > 0
    ]

    # Apply difficulty filter if provided
    if difficulty:
        similar_indices = [
            idx for idx in similar_indices
            if courses.iloc[idx]['course_difficulty'] == difficulty
        ]

    if not similar_indices:
        return []

    # Normalize course ratings
    ratings = pd.to_numeric(
        courses['course_rating'], errors='coerce'
    )

    min_rating = ratings.min()
    max_rating = ratings.max()

    if pd.isna(min_rating) or pd.isna(max_rating):
        return []

    if max_rating == min_rating:
        rating_norm = pd.Series(0.0, index=courses.index)
    else:
        rating_norm = (ratings - min_rating) / (max_rating - min_rating)

    # Calculate final recommendation scores
    recommendations = []

    for idx in similar_indices:

        similarity = float(scores[idx])
        rating = rating_norm.iloc[idx]

        if pd.isna(rating):
            rating = 0.0

        final_score = (0.8 * similarity) + (0.2 * rating)

        course = courses.iloc[idx].to_dict()

        course['similarity_score'] = similarity
        course['final_score'] = float(final_score)

        recommendations.append(course)

    # Sort by final score
    recommendations.sort(
        key=lambda x: x['final_score'],
        reverse=True
    )

    return recommendations[:n]
