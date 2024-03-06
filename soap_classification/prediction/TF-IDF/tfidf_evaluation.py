import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import os
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import GradientBoostingClassifier
from tqdm import tqdm


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")

# Load the dataset
data = pd.read_csv(os.path.join(SOAPS_PATH, "labeled_dataset.csv"))

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    data["SOAP"], data["label"], test_size=0.15, random_state=42
)

# Compute class weights

class_weights = compute_class_weight(
    class_weight="balanced", classes=np.unique(y_train), y=y_train
)
# TF-IDF representation
vectorizer = TfidfVectorizer()

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

# Perform cross-validation
cv_scores = cross_val_score(classifier, X_train, y_train, cv=5)

print("Cross Validation Scores:")
print(cv_scores)
print("Mean CV Accuracy: {:.2f}".format(np.mean(cv_scores)))


# Fit the classifier
classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = classifier.predict(X_test)

# Generate the classification report
class_rep = classification_report(y_test, y_pred, output_dict=True)

# Save the classification report as PDF
with open("tfidf_report.txt", "w") as f:
    f.write(classification_report(y_test, y_pred))

# Plot confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(
    confusion_matrix=conf_matrix, display_labels=np.unique(y_test)
)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")


# Save the confusion matrix as PDF
plt.savefig("tfidf_conf_mat.jpg", format="png", dpi=1200)
