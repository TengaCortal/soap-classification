## SOAP Dataset Processing

This set of Python scripts processes SOAP (Subjective, Objective, Assessment, Plan) data stored in CSV files. Each script performs a specific task in the processing pipeline, from data retrieval to text cleaning and vocabulary extraction. Below is an overview of each script, along with its input and output.

| Script Name            | <br> Description &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                                                                               | Input                          | Output                         |
|------------------------|----------------------------------------------------------------------------------------------|--------------------------------|--------------------------------|
| `only_soap.py`         | Extracts the first column from a CSV file containing SOAP data.                                | `processed_data_clinicName/DB_soap_orderCode.csv` | `clinicName_soap.csv` containing only the first column |
| `regex.py`             | Counts the number of rows containing a specific regex pattern in a CSV file.                 | `clinicName_soap.csv`             | Number of matching rows        |
| `total_soap.py`        | Combines multiple SOAP CSV files into a single CSV file.                                       | `resources/soaps/*.csv`       | `combined_soaps.csv` containing all SOAP data |
| `retrieve_classified_soaps.py` | Retrieves rows containing a specific regex pattern.              | `combined_soaps.csv`          | `classified_soaps.csv` with header row added |
| `unify_syntax.py`      | Modifies the SOAP data by replacing specific patterns and standardizing the syntax.           | `classified_soaps.csv`        | `unified_syntax_soap.csv` with modified syntax |
| `remove_undesired.py`  | Cleans the SOAP data by removing unnecessary characters and rows with undesired patterns.     | `unified_syntax_soap.csv`     | `cleaned_classified_soaps.csv` with cleaned data |
| `extract_english_vocabulary.py` | Extracts unique English words from the cleaned SOAP data                                | `cleaned_classified_soaps.csv` | `clinics_english_words.txt` containing unique English words |

The scripts would usually be executed in the order listed above to complete the data processing pipeline. The output of each script serves as the input for the subsequent script.
