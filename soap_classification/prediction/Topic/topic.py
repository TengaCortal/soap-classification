import pandas as pd
from bertopic import BERTopic
import os
import sys
from tqdm import tqdm
from absl import flags
import re

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../preprocessing")
from preprocessing.hybrid_tokenization import hybrid_tokenize

# Load the dataset
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")
RESOURCES_PATH = os.path.join(BASE_PATH, "../resources")
MECABRC_PATH = "/opt/homebrew/etc/mecabrc"
os.environ["MECABRC"] = MECABRC_PATH

# set the flags for Bert
sys.argv = ["preserve_unused_tokens=False"]
flags.FLAGS(sys.argv)


def classify_soap_notes(notes):
    # Transform the new SOAP notes using the trained BERTopic model
    new_topics, _ = model.transform(notes)

    # Map the topics to labels (S, O, A, P)
    for note, topic in zip(notes, new_topics):
        if topic == 0:
            print(f"Predicted label for SOAP note '{note}': P")
        elif topic == 1:
            print(f"Predicted label for SOAP note '{note}': S")
        elif topic == 2:
            print(f"Predicted label for SOAP note '{note}': O")
        elif topic == 3:
            print(f"Predicted label for SOAP note '{note}': A")
        elif topic == 4:
            print(f"Predicted label for SOAP note '{note}': X")


def tokenize_soaps(soap_file):
    data = pd.read_csv(soap_file)

    # percentage = int(len(data) * 0.1)

    # # Take the first ten percent of the sorted data
    # data = data.head(percentage)

    tqdm.pandas(desc="Tokenizing SOAPS")

    data["tokenized_SOAP"] = data["SOAP"].progress_apply(hybrid_tokenize)

    # Use list comprehension to remove characters from each element in the list
    data["tokenized_SOAP"] = data["tokenized_SOAP"].apply(
        lambda x: [re.sub(r"[\[\]UNK]", "", element) for element in x]
    )

    # Concatenate elements within each list into a single string
    data["tokenized_SOAP"] = data["tokenized_SOAP"].apply(
        lambda x: " ".join(map(str, x))
    )

    # Save the tokenized SOAP data to a CSV file
    data[["tokenized_SOAP", "label"]].to_csv(
        os.path.join(SOAPS_PATH, "tokenized_labeled_soap.csv"), index=False
    )

    data["tokenized_SOAP"].to_csv(
        os.path.join(SOAPS_PATH, "tokenized_soaps.csv"), index=False
    )


if __name__ == "__main__":
    # soap_file = os.path.join(SOAPS_PATH, "labeled_dataset.csv")
    # tokenize_soaps(soap_file)

    data = pd.read_csv(os.path.join(SOAPS_PATH, "tokenized_labeled_soap.csv"))

    # Preprocess the data
    data["tokenized_SOAP"] = data["tokenized_SOAP"].fillna("").astype(str)

    # Take only a % of the data
    # data = data.sample(frac=0.2, random_state=42)

    # Create a BERTopic model
    model = BERTopic(language="multilingual", nr_topics=6)

    # Fit BERTopic to the data
    topics, probs = model.fit_transform(data["tokenized_SOAP"])

    fig = model.visualize_barchart(n_words=10)
    fig.write_html("bertopic.html")

    result_df = pd.DataFrame(
        {
            "soap_text": data["tokenized_SOAP"],
            "topic_no": topics,
            "proba": probs,
        }
    )

    result_df.to_csv(os.path.join(SOAPS_PATH, "bertopic_soaps.csv"), index=False)
