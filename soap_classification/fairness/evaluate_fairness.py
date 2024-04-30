import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
import warnings
import sys

# Suppress warnings
warnings.filterwarnings("ignore")

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_PATH)

os.environ["MECABRC"] = "/opt/homebrew/etc/mecabrc"
import prediction.soap_preprocessing as sp


def evaluate_fairness(data, subgroup_column):
    """
    Evaluate fairness of a classifier.

    Args:
        data (DataFrame): The dataset containing SOAP notes and labels.
        subgroup_column (str): The column containing subgroup information.

    Returns:
        tuple: A tuple containing percentage of correct predictions and subgroup counts.
    """
    # Tokenization
    data["tokens"] = data["soap"].apply(sp.get_words)

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

    # Predict on the test set
    y_pred = classifier.predict(X_test)

    # Save the classification report
    with open(f"fairness_tfidf_report_{subgroup_column}.txt", "w") as f:
        f.write(classification_report(y_test, y_pred))

    # Calculate the percentage of correct predictions
    correct_predictions_percentage = (y_test == y_pred).mean() * 100

    # Count occurrences of each subgroup value
    subgroup_counts = data[subgroup_column].value_counts()

    return correct_predictions_percentage, subgroup_counts


if __name__ == "__main__":
    print(BASE_PATH)
    # Load the dataset
    data = pd.read_csv(os.path.join(BASE_PATH, "fairness/fairness_labeled_dataset.csv"))

    # Dictionary to store fairness percentages for each subgroup
    fairness_results = {}

    # Iterate over each subgroup and calculate fairness percentage
    for subgroup_column in [
        "age",
        "gender_type",
        "physician",
        "department",
        "clinic_id",
    ]:
        subgroup_data = data.groupby(subgroup_column)
        subgroup_fairness = {}
        for subgroup_value, subgroup_df in subgroup_data:
            print(f"Calculating fairness for {subgroup_column}={subgroup_value}")
            fairness_percentage, subgroup_counts = evaluate_fairness(
                subgroup_df, subgroup_column
            )
            subgroup_fairness[subgroup_value] = (fairness_percentage, subgroup_counts)
        fairness_results[subgroup_column] = subgroup_fairness

    # Print fairness percentages and counts
    print("Fairness Results:")
    for subgroup_column, subgroup_fairness in fairness_results.items():
        print(f"\n{subgroup_column.capitalize()}:")
        for subgroup_value, (
            fairness_percentage,
            subgroup_counts,
        ) in subgroup_fairness.items():
            print(
                f"{subgroup_value}: {fairness_percentage:.2f}% (Nb: {subgroup_counts.values[0]})"
            )
