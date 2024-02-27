import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
import os


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

    # Define the classifier
    classifier = make_pipeline(
        vectorizer, LogisticRegression(solver="lbfgs", max_iter=1000)
    )

    # Fit the classifier
    classifier.fit(data["SOAP"], data["label"])

    return classifier


def predict_label(classifier, soap_text):
    """
    Predict the label for a given SOAP text using the trained classifier.

    Args:
    - classifier (Pipeline): Trained classification pipeline.
    - soap_text (str): SOAP text for prediction.

    Returns:
    - predicted_label (str): Predicted label for the SOAP text.
    """
    # Predict the label
    predicted_label = classifier.predict([soap_text])[0]

    return predicted_label


if __name__ == "__main__":
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")

    # Train the classifier
    dataset_file = os.path.join(SOAPS_PATH, "labeled_dataset.csv")
    classifier = train_tfidf_classifier(dataset_file)

    # Example usage: predict label for a given SOAP text
    soap_text = "右記処方。ルリッドからビブラマイシンに処方を変更して継続。"
    predicted_label = predict_label(classifier, soap_text)
    print("Predicted label:", predicted_label)
