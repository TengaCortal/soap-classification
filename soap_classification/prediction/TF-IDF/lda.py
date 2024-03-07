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
from preprocessing.tokenization_mod import MecabTokenizer
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


if __name__ == "__main__":

    data = pd.read_csv(os.path.join(SOAPS_PATH, "labeled_dataset.csv"))

    # Take only 10% of the data
    data_subset = data.sample(frac=1, random_state=42)

    # Create a BERTopic model
    model = BERTopic(language="multilingual", nr_topics=6)

    tqdm.pandas(desc="Tokenizing SOAPS")
    data_subset["tokenized_SOAP"] = data_subset["SOAP"].progress_apply(hybrid_tokenize)

    print(data_subset["tokenized_SOAP"])

    # Use list comprehension to remove characters from each element in the list
    data_subset["tokenized_SOAP"] = data_subset["tokenized_SOAP"].apply(
        lambda x: [re.sub(r"[\#\[\]UNK]", "", element) for element in x]
    )

    # Concatenate elements within each list into a single string
    data_subset["tokenized_SOAP"] = data_subset["tokenized_SOAP"].apply(
        lambda x: " ".join(map(str, x))
    )

    # Save the tokenized SOAP data to a CSV file
    data_subset[["tokenized_SOAP", "label"]].to_csv(
        os.path.join(SOAPS_PATH, "tokenized_labeled_soap.csv"), index=False
    )

    data_subset["tokenized_SOAP"].to_csv(
        os.path.join(SOAPS_PATH, "tokenized_soaps.csv"), index=False
    )
    print(data_subset["tokenized_SOAP"])

    # # Fit BERTopic to the data
    # tqdm.pandas(desc="Fitting BERTopic")
    # topics, probs = model.fit_transform(data_subset["tokenized_SOAP"])

    # fig = model.visualize_barchart(n_words=10)
    # fig.write_html("bertopic.html")

    # result_df = pd.DataFrame(
    #     {
    #         "soap_text": data_subset["tokenized_SOAP"],
    #         "topic_no": topics,
    #         "proba": probs,
    #     }
    # )

    # print(result_df.head(10).to_string(justify="left", index=False))
