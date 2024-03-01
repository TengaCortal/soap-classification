import joblib
import os
import sys

sys.path.append("..")
import soap_partitioner as sp
import train_tfidf as tt

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    for soap_note_parts in partitioned_soap_notes:
        predicted_labels.append(predict_label(classifier, soap_note_parts))
    return predicted_labels


def prediction_pipeline():

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

    csv_file = os.path.join(SOAPS_PATH, "cleaned_classified_soaps.csv")
    cleaned_soaps = sp.remove_annotations(csv_file)
    separator = "。"
    partitioned_soaps = sp.partition_all_soap_text(cleaned_soaps, separator)

    partitioned_soaps = partitioned_soaps[1:5]

    predicted_labels_all = []

    for i, soap_note_parts in enumerate(partitioned_soaps):

        # Predict labels for all parts
        predicted_labels = []
        for soap_part in soap_note_parts:
            predicted_labels.append(predict_labels(classifier, [soap_part])[0])

        # Check if all sections (S, O, A, P) are present in the predicted labels
        all_sections_present = all(
            section in "".join(predicted_labels) for section in ["S", "O", "A", "P"]
        )

        # If any section is missing, find the longest and second longest parts and repartition them
        if not all_sections_present:
            # Find the index of the longest element in the partition
            longest_element_index = max(
                range(len(soap_note_parts)), key=lambda x: len(soap_note_parts[x])
            )
            longest_element = soap_note_parts[longest_element_index]

            # Find the index of the second longest element in the partition
            sorted_indices = sorted(
                range(len(soap_note_parts)),
                key=lambda x: len(soap_note_parts[x]),
                reverse=True,
            )

            # Repartition the longest element using space as a separator
            repartitioned_parts_longest = sp.partition_soap_text(
                longest_element, separator=" "
            )

            # Predict labels for the repartitioned parts
            repartitioned_labels_longest = []
            for part in repartitioned_parts_longest:
                repartitioned_labels_longest.append(
                    predict_labels(classifier, [part])[0]
                )

            # Update the partitioned SOAP note and the predicted labels
            partitioned_soaps[i].pop(
                longest_element_index
            )  # Remove the longest element
            predicted_labels.pop(
                longest_element_index
            )  # Remove the corresponding predicted label
            for j, part in enumerate(repartitioned_parts_longest):
                partitioned_soaps[i].insert(
                    longest_element_index + j, part
                )  # Insert the repartitioned parts
                predicted_labels.insert(
                    longest_element_index + j, repartitioned_labels_longest[j]
                )  # Insert the repartitioned labels

        # If any section is still missing, find the second longest element and repartition it
        if not all_sections_present:
            second_longest_element_index = sorted_indices[1]
            second_longest_element = soap_note_parts[second_longest_element_index]

            # Repartition the second longest element using space as a separator
            repartitioned_parts_second_longest = sp.partition_soap_text(
                second_longest_element, separator=" "
            )

            # Predict labels for the repartitioned parts
            repartitioned_labels_second_longest = []
            for part in repartitioned_parts_second_longest:
                repartitioned_labels_second_longest.append(
                    predict_labels(classifier, [part])[0]
                )

            print(
                "Second Longest Element Before Repartitioning:", second_longest_element
            )
            print(
                "Repartitioned Parts Second Longest:",
                repartitioned_parts_second_longest,
            )
            print(
                "Repartitioned Labels Second Longest:",
                repartitioned_labels_second_longest,
            )

            # Update the partitioned SOAP note and the predicted labels
            partitioned_soaps[i].pop(
                second_longest_element_index
            )  # Remove the second longest element
            predicted_labels.pop(
                second_longest_element_index
            )  # Remove the corresponding predicted label
            for j, part in enumerate(repartitioned_parts_second_longest):
                partitioned_soaps[i].insert(
                    second_longest_element_index + j, part
                )  # Insert the repartitioned parts
                predicted_labels.insert(
                    second_longest_element_index + j,
                    repartitioned_labels_second_longest[j],
                )  # Insert the repartitioned labels

        # Append predicted labels for current SOAP note to the list
        predicted_labels_all.append(predicted_labels)

    return partitioned_soaps, predicted_labels_all


if __name__ == "__main__":
    processed_data = prediction_pipeline()
    partitioned_soaps, predicted_labels_all = processed_data
    print(partitioned_soaps)
    print()
    print(predicted_labels_all)
    # Print partitioned SOAP note and the associated predicted labels
    for i, soap_note_parts in enumerate(partitioned_soaps):
        print("SOAP Note:", i + 1)
        for j, soap_part in enumerate(soap_note_parts):
            print("Part", j + 1, ":", soap_part)
            print("Predicted Label:", predicted_labels_all[i][j])
        print()
