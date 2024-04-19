import os
import pandas as pd
import joblib as jb
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import ConfusionMatrixDisplay

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")

import soap_preprocessing as sp


def train_tfidf_classifier(dataset_file, output_file):
    """
    Train a TF-IDF classifier on the provided dataset.

    Args:
    - dataset_file (str): Path to the CSV file containing the dataset.

    Returns:
    - clf (Pipeline): Trained classification pipeline.
    """
    # Load the dataset
    data = pd.read_csv(dataset_file)

    # Tokenization
    data["tokens"] = data["SOAP"].apply(sp.get_words)

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        data["tokens"], data["label"], test_size=0.3, random_state=42
    )

    # TF-IDF representation
    vectorizer = TfidfVectorizer(tokenizer=sp.tokenize, lowercase=False)

    # Compute class weights
    class_weights = compute_class_weight(
        class_weight="balanced", classes=np.unique(y_train), y=y_train
    )

    class_weights_dict = {
        class_label: weight
        for class_label, weight in zip(np.unique(y_train), class_weights)
    }

    # Define the classifier
    classifier = make_pipeline(
        vectorizer,
        LogisticRegression(
            solver="lbfgs",
            max_iter=1000,
            penalty="l2",
            C=10.0,
            class_weight=class_weights_dict,
        ),
    )

    # Fit the classifier
    classifier.fit(X_train, y_train)
    jb.dump(classifier, output_file)  # Save the trained classifier to a file

    # Evaluate the classifier
    y_pred = classifier.predict(X_test)

    # Save the classification report as PDF
    report_file = os.path.join(BASE_PATH, "TFIDF/results/tfidf_report.txt")
    with open(report_file, "w") as f:
        f.write(classification_report(y_test, y_pred))

    # Plot confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=conf_matrix, display_labels=np.unique(y_test)
    )
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")

    # Save the confusion matrix as PDF
    matrix_file = os.path.join(BASE_PATH, "TFIDF/results/tfidf_conf_mat.jpg")
    plt.savefig(matrix_file, format="png", dpi=900)

    return classifier


if __name__ == "__main__":

    dataset_file = os.path.join(SOAPS_PATH, "labeled_dataset.csv")
    output_file = os.path.join(BASE_PATH, "../resources/tfidf_classifier.joblib")

    classifier = train_tfidf_classifier(dataset_file, output_file)
