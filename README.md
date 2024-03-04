# Machine Learning based SOAP Classification System

日本語の[README](soap_classification/README-日本語.md)あります！

This project involves the development of a Machine Learning based SOAP (Subjective, Objective, Assessment, Plan) classification system. 


## Motivation

One of the primary motivations behind this project is to streamline the documentation process in healthcare by reducing the time and effort required for manual note classification. By automating the classification of SOAP notes, healthcare professionals can focus more on patient care and less on administrative tasks. Additionally, it can help ensure consistency and standardization in note-taking practices, leading to improved quality of care and better communication among healthcare providers.


## Current state

For now, the provided code performs various preprocessing tasks on data from 11 Japanese clinics to construct the data that will be used for analysis and classification.

Then we propose a first approach to classifying SOAP notes by using TF-IDF (Term Frequency-Inverse Document Frequency) representation coupled with machine learning algorithms. In this method, the SOAP texts are transformed into numerical vectors using TF-IDF, which represents the importance of each term (word) in the document relative to a collection of documents. A machine learning model is then trained on these TF-IDF vectors to predict the section labels (X, Subjective, Objective, Assessment, Plan) of each SOAP note.

Finally a English-Japanese hybrid tokenizer was developped to prepare textual data that will serve as input for more complicated deep learning models such as LSTM and UTH-BERT. 

For detailed instructions on running the scripts and understanding their output, refer to the respective README files in the subdirectories.


## Table of Contents

1. [SOAP Data Construction](soap_classification/data_construction/README.md)
2. [SOAP Section Prediction](soap_classification/prediction/README.md)
3. [Pre-processing for NLP and Hybrid Tokenization](soap_classification/preprocessing/README.md)


## Additional Notes

- **Requirements:** Ensure that all necessary dependencies are installed as per the instructions provided in the README files.
- **Dataset:** The provided code assumes that the SOAP data is stored in CSV files. You may need to adjust the data loading and preprocessing steps according to your dataset format.

