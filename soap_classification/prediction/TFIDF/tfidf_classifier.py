import joblib
import os
import sys
import csv

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import soap_partitioner as sp
import train_tfidf as tt

SOAPS_PATH = os.path.join(BASE_PATH, "../resources/soaps")


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
    if isinstance(soap_text, str):
        # Predict the label for a single SOAP text
        predicted_label = classifier.predict([soap_text])[0]
    elif isinstance(soap_text, list):
        # Predict the labels for a list of SOAP texts
        predicted_label = classifier.predict(soap_text)
    else:
        raise ValueError("Invalid input format. Expected str or list.")

    return predicted_label


def predict_labels(classifier, partitioned_soap_notes):
    """
    Predict the section label for each part of partitioned SOAP notes using the trained classifier.

    Args:
    - classifier (Pipeline): Trained classification pipeline.
    - partitioned_soap_notes (list): List of partitioned SOAP notes, where each item is a list of SOAP parts.

    Returns:
    - predicted_labels (list): List of lists containing predicted labels for each part of each SOAP note.
    """
    predicted_labels = []
    for partitioned_soap in partitioned_soap_notes:
        predicted_labels.append(predict_label(classifier, partitioned_soap))
    return predicted_labels


def get_classifier():
    # Train the classifier
    dataset_file = os.path.join(SOAPS_PATH, "labeled_dataset.csv")
    classifier_file = os.path.join(BASE_PATH, "../resources/trained_classifier.joblib")

    # Check if trained classifier exists, if not, train it
    if not os.path.exists(classifier_file):
        # Train the classifier
        classifier = tt.train_tfidf_classifier(dataset_file)
        # Save the trained classifier
        tt.save_classifier(classifier, classifier_file)
    else:
        # Load the trained classifier
        classifier = joblib.load(
            classifier_file
        )  # Load a trained classifier from a file
    return classifier


def predict_final_label(classifier, partitioned_soap):

    # Predict labels for all parts
    predicted_labels = predict_labels(classifier, partitioned_soap)

    predicted_label_first_part = predict_label(classifier, partitioned_soap[0])

    # If the predicted label for the first part is neither "X" nor "S", choose the one with higher probability
    if len(partitioned_soap) > 2 and predicted_label_first_part not in [
        "X",
        "S",
    ]:
        x_probability = classifier.predict_proba(partitioned_soap)[0][
            classifier.classes_.tolist().index("X")
        ]
        s_probability = classifier.predict_proba([partitioned_soap])[0][
            classifier.classes_.tolist().index("S")
        ]
        if x_probability > s_probability:
            predicted_labels[0] = "X"
        else:
            predicted_labels[0] = "S"

    # If there are 3 or more parts and any section is missing, find the longest part and repartition it
    if len(partitioned_soap) > 2 and not check_all_sections(predicted_labels):
        # Find the index of the longest element in the partition
        longest_element_index = max(
            range(len(partitioned_soap)), key=lambda x: len(partitioned_soap[x])
        )
        longest_element = partitioned_soap[longest_element_index]

        # Sort indices to find the index of the second longest element in the partition if needed later
        sorted_indices = sorted(
            range(len(partitioned_soap)),
            key=lambda x: len(partitioned_soap[x]),
            reverse=True,
        )

        # Repartition the longest element using space as a separator
        repartitioned_parts_longest = sp.partition_soap_text(
            longest_element, separator=" "
        )

        # Predict labels for the repartitioned parts
        repartitioned_labels_longest = predict_labels(
            classifier, repartitioned_parts_longest
        )

        print("partitioned_soap")
        print(partitioned_soap)
        # Update the partitioned SOAP note and the predicted labels
        partitioned_soap.pop(longest_element_index)  # Remove the longest element
        predicted_labels.pop(
            longest_element_index
        )  # Remove the corresponding predicted label
        for j, part in enumerate(repartitioned_parts_longest):
            partitioned_soap.insert(
                longest_element_index + j, part
            )  # Insert the repartitioned parts
            predicted_labels.insert(
                longest_element_index + j, repartitioned_labels_longest[j]
            )  # Insert the repartitioned labels

        # If any section is still missing, find the second longest element and repartition it
        if not check_all_sections(predicted_labels):
            second_longest_element_index = sorted_indices[1]
            second_longest_element = partitioned_soap[second_longest_element_index]

            # Repartition the second longest element using space as a separator
            repartitioned_parts_second_longest = sp.partition_soap_text(
                second_longest_element, separator=" "
            )

            # Predict labels for the repartitioned parts
            repartitioned_labels_second_longest = predict_labels(
                classifier, repartitioned_parts_second_longest
            )

            # Update the partitioned SOAP note and the predicted labels
            partitioned_soap.pop(
                second_longest_element_index
            )  # Remove the second longest element
            predicted_labels.pop(
                second_longest_element_index
            )  # Remove the corresponding predicted label
            for j, part in enumerate(repartitioned_parts_second_longest):
                partitioned_soap.insert(
                    second_longest_element_index + j, part
                )  # Insert the repartitioned parts
                predicted_labels.insert(
                    second_longest_element_index + j,
                    repartitioned_labels_second_longest[j],
                )  # Insert the repartitioned labels

            if (
                len(predicted_labels) >= 5
                and check_all_sections(predicted_labels)
                and predicted_labels[-3],
                predicted_labels[-2] == "P",
            ):
                predicted_labels[-1] = "".join("P")

    return partitioned_soap, predicted_labels


def check_all_sections(predicted_labels):
    all_sections_present = all(
        section in "".join(predicted_labels) for section in ["S", "O", "A", "P"]
    )
    return all_sections_present


def prediction_pipeline():

    classifier = get_classifier()
    csv_file = os.path.join(SOAPS_PATH, "cleaned_classified_soaps.csv")
    cleaned_soaps = sp.remove_annotations(csv_file)
    separator = "。"
    partitioned_soaps = sp.partition_all_soap_text(cleaned_soaps, separator)
    partitioned_soaps = partitioned_soaps[10952:10953]

    predicted_labels_all = []
    partitioned_soap_all = []
    for i, partitioned_soap in enumerate(partitioned_soaps):
        if i % 1000 == 0:
            print("Processing SOAP Note:", i)

        final_partitioned_soap, final_predicted_labels = predict_final_label(
            classifier, partitioned_soap
        )

        # Append predicted labels for current SOAP note to the list
        predicted_labels_all.append(final_predicted_labels)
        partitioned_soap_all.append(final_partitioned_soap)

    return partitioned_soap_all, predicted_labels_all


def generate_csv_with_section_labels(
    partitioned_soaps, predicted_labels_all, output_file
):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for i, partitioned_soap in enumerate(partitioned_soaps):
            labeled_soap_note = ""
            prev_label = None
            for j, soap_part in enumerate(partitioned_soap):
                current_label = predicted_labels_all[i][j]
                if current_label == prev_label:
                    labeled_soap_note += soap_part.strip() + " "
                else:
                    labeled_soap_note += f"{current_label}: {soap_part.strip()} "
                prev_label = current_label
            if labeled_soap_note:
                writer.writerow([labeled_soap_note.strip()])


def for_demo(soap):
    classifier = get_classifier()
    partitioned_soap, predict_label = predict_final_label(classifier, soap)
    return partitioned_soap, predict_label


if __name__ == "__main__":
    soap = "023\/07\/19　初診大分前から両目に黒い物が見える。5月か6月位に夜になると、右眼の奥にピカっと光る物が何度か見えた。今は治まっている。夜勤のお仕事。散瞳検査OK。歩いて来院。S)両目　眼の際　痒み+　目脂は出ない。眼を抑えるようにごしごしかいていたのでそれはやめるよう伝えた。２ｗ間隔位で来ていただいてるので今日は視力検査しませんでした。両AH+　アレジオンLX両2　処方以前緑内障と言われていたIOP　14\/12ｍｍHg　→15\/15mmHg　やや高めOCT NFLD+ R>L　眼鏡は左が過矯正　眼鏡改作 try眼鏡処方（2023\/08\/16）改作を勧めたタプロス両1　do（2023\/09\/06-）経過観察　1M"
    separator = "。"
    partitioned_soaps = sp.partition_soap_text(soap, separator)
    # partitioned_soaps, predicted_labels_all = prediction_pipeline()
    # print(partitioned_soaps)
    # print()
    # print(predicted_labels_all)
    # # Print partitioned SOAP note and the associated predicted labels
    # for i, partitioned_soap in enumerate(partitioned_soaps):
    #     print("SOAP Note:", i + 1)
    #     for j, soap_part in enumerate(partitioned_soap):
    #         print("Part", j + 1, ":", soap_part)
    #         print("Predicted Label:", predicted_labels_all[i][j])
    #     print()

    # # generate the CSV file
    # generate_csv_with_section_labels(
    #     partitioned_soaps,
    #     predicted_labels_all,
    #     os.path.join(SOAPS_PATH, "tfidf_sectionized_soaps.csv"),
    # )

    for_demo(soap)
