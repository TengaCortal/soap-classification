import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")


def train_tfidf_classifier(dataset_file):
    """
    Train a TF-IDF classifier on the provided dataset.

    Args:
    - dataset_file (str): Path to the CSV file containing the dataset.

    Returns:
    - clf (Pipeline): Trained classification pipeline.
    """
    # Load the dataset
    data = pd.read_csv(dataset_file)

    # TF-IDF representation
    vectorizer = TfidfVectorizer()

    # # Compute class weights
    # class_labels = np.unique(data["label"])
    # class_weights = compute_class_weight(
    #     class_weight="balanced", classes=class_labels, y=data["label"]
    # )
    # for label, weight in zip(class_labels, class_weights):
    #     print(f"{label}: {weight}")
    # # Create a dictionary of class weights
    # class_weight_dict = dict(zip(class_labels, class_weights))
    custom_weights = {"A": 0.8, "O": 1.0, "P": 1.0, "S": 0.5, "X": 1.0}
    # Define the classifier
    classifier = make_pipeline(
        vectorizer,
        LogisticRegression(
            solver="lbfgs",
            max_iter=1000,
            penalty="l2",
            C=10.0,
            class_weight=custom_weights,
        ),
    )

    # Fit the classifier
    classifier.fit(data["SOAP"], data["label"])

    return classifier


if __name__ == "__main__":

    dataset_file = os.path.join(SOAPS_PATH, "labeled_dataset.csv")

    classifier = train_tfidf_classifier(dataset_file)
    classifier_file = os.path.join(BASE_PATH, "../resources/trained_classifier.joblib")

    joblib.dump(classifier, classifier_file)  # Save the trained classifier to a file
