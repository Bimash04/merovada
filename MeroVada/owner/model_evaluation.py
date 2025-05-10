import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from owner.models import Item

def evaluate_accuracy():
    # Retrieve the items data from the database
    items = list(Item.objects.all().values('id', 'name', 'price', 'category', 'location'))
    df = pd.DataFrame(items)

    if df.shape[0] < 10:
        print("Not enough data to evaluate.")
        return

    # Create feature matrix using multiple columns (price, category, location)
    features = pd.get_dummies(df[['price', 'category', 'location']])  # One-hot encode categorical variables
    feature_values = features.values 

    # Split into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(
        feature_values, df[['category']], test_size=0.2, random_state=42
    )

    # Initialize Nearest Neighbors model
    knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
    knn.fit(train_features)

    correct_predictions = 0
    total_tests = len(test_features)

    # For each test instance, find the nearest neighbors and check if they belong to the same category
    for i, test_instance in enumerate(test_features):
        _, indices = knn.kneighbors(np.array([test_instance]))
        
        # Get the predicted neighbors' categories
        neighbor_categories = df.iloc[indices[0]]['category'].values
        
        # Check if the majority of neighbors belong to the same category as the test instance
        if test_labels.iloc[i]['category'] in neighbor_categories:
            correct_predictions += 1

    accuracy = (correct_predictions / total_tests) * 100
    print(f"Recommendation System Accuracy: {accuracy:.2f}%")

