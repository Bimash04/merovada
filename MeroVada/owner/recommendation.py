import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from owner.models import Item

def get_recommendations(item_name, location, n_neighbors=5):
    items = list(Item.objects.filter(location=location).values('name', 'price'))
    df = pd.DataFrame(items)

    if item_name not in df['name'].values:
        return []

    features = df[['price']].values
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    knn.fit(features)

    index = df[df['name'] == item_name].index[0]
    _, indices = knn.kneighbors([features[index]])

    recommendations = df.iloc[indices[0][1:]]['name'].tolist()
    return recommendations
