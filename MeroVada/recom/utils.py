from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from owner.models import Item
import scipy.sparse

def get_recommendations(item_id, num_recommendations=5):
    """
    Generate item recommendations based on cosine similarity using TF-IDF and price.
    """
    # Fetch all items
    items = Item.objects.all()
    if not items.exists():
        return []

    # Prepare data
    item_data = []
    item_ids = []
    for item in items:
        # Combine text fields: name, category, location
        text = f"{item.name} {item.category} {item.location or ''}"
        item_data.append(text)
        item_ids.append(item.id)

    # TF-IDF Vectorization for text data
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(item_data)

    # Normalize price
    prices = np.array([[float(item.price)] for item in items])  
    scaler = MinMaxScaler()
    normalized_prices = scaler.fit_transform(prices)

    # Combine TF-IDF features with normalized price
   
    if isinstance(tfidf_matrix, scipy.sparse.spmatrix):
        tfidf_dense = np.asarray(tfidf_matrix.todense())
    else:
        tfidf_dense = np.asarray(tfidf_matrix)

    combined_features = np.hstack([tfidf_dense, normalized_prices])

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(combined_features)

    
    try:
        item_idx = item_ids.index(item_id)
    except ValueError:
        return []

    
    sim_scores = list(enumerate(similarity_matrix[item_idx]))
    # Sort by similarity score (descending) and exclude the item itself
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] != item_idx][:num_recommendations]

    
    recommended_indices = [i[0] for i in sim_scores]
    recommended_items = Item.objects.filter(id__in=[item_ids[idx] for idx in recommended_indices])

    return recommended_items