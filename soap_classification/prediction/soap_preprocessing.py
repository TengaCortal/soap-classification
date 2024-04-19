import os
import pandas as pd
import re
import MeCab

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")


def remove_annotations(csv_file, mode):
    """
    Remove annotations from every row in a CSV file containing SOAP notes.

    Args:
    - csv_file (str): Path to the CSV file containing the SOAP notes.

    Returns:
    - cleaned_soaps (DataFrame): DataFrame with annotations removed from every row.
    """
    # Load the CSV file
    data = pd.read_csv(csv_file, header=None)

    # Define patterns to remove
    patterns = ["X:", "SUB:", "OBJ:", "ASM:", "PLN:"]

    # Remove annotations from each row
    if mode == "free-text":
        cleaned_soaps = data.apply(
            lambda row: " ".join(
                [re.sub("|".join(patterns), "", text) for text in row]
            ),
            axis=1,
        ).to_frame()
    elif mode == "separated-text":
        cleaned_soaps = data.apply(
            lambda row: " ".join(
                [re.sub("|".join(patterns), "\n", text) for text in row]
            ),
            axis=1,
        ).to_frame()

    return cleaned_soaps


def partition_soap_text(soap_text, separator):
    """
    Partition a SOAP text using a separator.

    Args:
    - soap_text (str): The SOAP text to be partitioned.

    Returns:
    - partitions (list): List of partitions extracted from the SOAP text.
    """
    partitions = soap_text.split(separator)

    partitions = [partition.strip() for partition in partitions if partition.strip()]
    return partitions


def partition_all_soap_text(cleaned_soaps, separator):
    """
    Partition all rows in the output of remove_annotations and return a list of partitioned SOAP texts.

    Args:
    - cleaned_soaps (DataFrame): DataFrame with annotations removed from every row.

    Returns:
    - partitioned_soaps (list): List of lists containing partitioned SOAP texts.
    """
    partitioned_soaps = []
    for soap_text in cleaned_soaps[0]:
        partitions = partition_soap_text(soap_text, separator)
        partitioned_soaps.append(partitions)
    return partitioned_soaps


# MeCabの形態素解析結果から単語を取得する関数
def get_words(text):
    # MeCabのインスタンスを作成
    mecab = MeCab.Tagger("-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd")
    words = []
    node = mecab.parseToNode(text)
    while node:
        word = node.surface
        if word:
            words.append(node.surface)
        node = node.next
    return words


def tokenize(text):
    return text


if __name__ == "__main__":
    print("Partitioning Test:")
    csv_file = os.path.join(SOAPS_PATH, "cleaned_classified_soaps.csv")
    cleaned_soaps = remove_annotations(csv_file)
    separator = " "
    partitioned_soaps = partition_all_soap_text(cleaned_soaps, separator)
    print(partitioned_soaps[2:3])
