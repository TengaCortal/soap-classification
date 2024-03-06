import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
from sklearn.decomposition import TruncatedSVD
from tqdm import tqdm

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")


# Function to classify using cosine similarity
def classify_with_cosine_similarity(
    query, X_train_tfidf_reduced, y_train, vectorizer, k=5
):
    query_tfidf = vectorizer.transform([query])
    query_tfidf_reduced = svd.transform(query_tfidf)

    # Compute cosine similarities with reduced dimensions
    similarities = cosine_similarity(query_tfidf_reduced, X_train_tfidf_reduced)
    top_indices = np.argsort(similarities, axis=1)[0][-k:]
    labels = [y_train[idx] for idx in top_indices]
    vote_count = Counter(labels)
    total_docs = len(labels)
    normalized_votes = {
        label: count / total_docs for label, count in vote_count.items()
    }
    return normalized_votes


if __name__ == "__main__":
    # Load the dataset
    data = pd.read_csv(os.path.join(SOAPS_PATH, "labeled_dataset.csv"))

    svd = TruncatedSVD(n_components=100)

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        data["SOAP"], data["label"], test_size=0.15, random_state=42
    )

    # TF-IDF representation
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    X_train_tfidf_reduced = svd.fit_transform(X_train_tfidf)
    X_test_tfidf_reduced = svd.transform(X_test_tfidf)

    # Reset indices of y_train to ensure alignment
    y_train.reset_index(drop=True, inplace=True)

    # # Example usage
    # query = "＃1　高コレステロール血症＃2　高尿酸血症＃3　アルコール性肝障害"
    # votes = classify_with_cosine_similarity(
    #     query, X_train_tfidf_reduced, y_train, vectorizer
    # )
    # print("Votes for each class:", votes)

    # Classify each document in the test set
    predicted_labels = []
    for query_tfidf_reduced in tqdm(X_test_tfidf_reduced, desc="Classifying"):
        # Compute cosine similarities with reduced dimensions
        similarities = cosine_similarity([query_tfidf_reduced], X_train_tfidf_reduced)
        top_indices = np.argsort(similarities, axis=1)[0][
            -5:
        ]  # Top 5 similar documents
        labels = [y_train[idx] for idx in top_indices]
        predicted_label = max(set(labels), key=labels.count)  # Majority vote
        predicted_labels.append(predicted_label)

    # Evaluate performance
    accuracy = np.mean(predicted_labels == y_test)
    print("Accuracy:", accuracy)
