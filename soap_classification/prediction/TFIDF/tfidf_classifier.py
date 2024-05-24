import joblib
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import soap_preprocessing as sp
from soap_preprocessing import tokenize
import train_tfidf as tt

SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")

os.environ["MECABRC"] = "/opt/homebrew/etc/mecabrc"


def get_classifier():
    """
    Retrieve or train and save a classifier for SOAP notes.

    Returns:
        classifier: Trained or retrieved classifier.
    """
    # Train the classifier
    dataset_file = os.path.join(SOAPS_PATH, "labeled_dataset.csv")
    classifier_file = os.path.join(BASE_PATH, "../resources/tfidf_classifier.joblib")

    # Check if trained classifier exists, if not, train it
    if not os.path.exists(classifier_file):
        print("Training the SOAP classifier")
        # Train the classifier
        classifier = tt.train_tfidf_classifier(dataset_file, classifier_file)
    else:
        # Load the trained classifier
        classifier = joblib.load(
            classifier_file
        )  # Load a trained classifier from a file
    return classifier


def classify_soap(classifier, soap, soap_type, sep):

    if soap_type == "notes":

        # Define separator according to partitioning mode
        separator_mapping = {"newline": "\n", "space": "　", "point": "。"}
        separator = separator_mapping.get(sep, None)

        # partition SOAP notes
        if type(soap) == str:
            partitioned_soaps = [sp.partition_soap_text(soap, separator)]
        else:
            partitioned_soaps = sp.partition_all_soap_text(soap, separator)

        # tokenize SOAP notes
        tokenized_soaps = []
        for partitioned_soap in partitioned_soaps:
            tokenized_soap = []
            for partition in partitioned_soap:
                tokenized_partition = sp.get_words(partition)
                tokenized_soap.append(tokenized_partition)
            tokenized_soaps.append(tokenized_soap)

        # predict labels
        labels = []
        for tokenized_soap in tokenized_soaps:
            label = classifier.predict(tokenized_soap)
            labels.append(label.tolist())

        return partitioned_soaps, labels

    elif soap_type == "section":

        # tokenize SOAP notes
        tokenized_soap = [sp.get_words(soap)]
        # predict label
        labels = classifier.predict(tokenized_soap)

        return labels


def for_demo(soap_data, soap_type, sep):
    """
    Perform prediction for a single SOAP note.

    Args:
        soap (str): The SOAP note to be processed.

    Returns:
        tuple: A tuple containing partitioned SOAP note and predicted labels.
    """
    classifier = get_classifier()

    return classify_soap(classifier, soap_data, soap_type, sep)


if __name__ == "__main__":

    csv_file = os.path.join(SOAPS_PATH, "cleaned_classified_soaps.csv")

    classifier = get_classifier()
    # Testing with different types of SOAP inputs
    mode = "free-text"
    sep = "space"
    cleaned_soaps = sp.remove_annotations(csv_file, mode)
    clius_soap = cleaned_soaps[888:889]
    clius_labels = classify_soap(classifier, clius_soap, "notes", sep)
    print(f"CLIUS SOAP labels: {clius_labels} \n")

    mode = "separated-text"
    sep = "newline"
    cleaned_soaps = sp.remove_annotations(csv_file, mode)
    separated_clius_soap = cleaned_soaps[888:889]
    separated_clius_labels = classify_soap(
        classifier, separated_clius_soap, "notes", sep
    )
    print(f"Separated CLIUS SOAP labels: {separated_clius_labels} \n")

    gpt_soap = "患者は今日の訪問時に胸の痛みを訴えています。痛みは3週間前から始まり、1日に3回以上、約1分間続きます。痛みの増強は動作に関連しておらず、冷や汗や嘔気はありません。患者は心筋梗塞の既往歴があり、心配しています。体温は36.4 ℃で、収縮期血圧は158 mmHg、拡張期血圧は98 mmHgです。体重は76.2 kgであり、心電図には明らかな異常はありません。診察時には胸痛の症状はありませんでした。患者の症状は心筋梗塞と関連がある可能性がありますが、現在の検査結果では異常は見られません。ただし、患者の心配を考慮し、負荷心電図検査をお勧めします。次回の診察時には負荷心電図検査を行い、その結果に基づいて適切な処置を検討します。胸痛が再発した場合は、直ちに診察を受けるように指示します。"
    gpt_labels = classify_soap(classifier, gpt_soap, "notes", "point")
    print(f"GPT SOAP labels: {gpt_labels} \n")

    O_section = "収縮期血圧 130 mmHg 拡張期血圧 61 mmHg 脈拍 90 bpm100歳体操へ行ってる"
    label = classify_soap(classifier, O_section, "section", "none")
    print(f"O section predicted label: {label} \n")
