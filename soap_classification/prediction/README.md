# SOAP Section Prediction

This folder contains a collection of prediction models designed to automate the categorization of SOAP sections within medical records. Currently, the primary prediction model implemented is based on TF-IDF

## 1. TF-IDF

TF-IDF (Term Frequency-Inverse Document Frequency) is a numerical statistic used in information retrieval and text mining to evaluate the importance of a word in a document relative to a collection of documents (corpus).

It consists of two main components: TF & IDF

### 1-1. Term Frequency (TF):

Measures the frequency of a term (word) within a document.
It is calculated by dividing the number of occurrences of a term in a document by the total number of terms in the document.

TF(t, d) = (Number of times term t appears in document d) / (Total number of terms in document d)

### 1-2. Inverse Document Frequency (IDF)

Measures the rarity of a term across all documents in the corpus.

It is calculated by taking the logarithm of the total number of documents in the corpus divided by the number of documents containing the term, and then adding 1 to avoid division by zero.

IDF(t) = log_e(Total number of documents / Number of documents containing term t)

### 1-3. TF-IDF score

The TF-IDF score for a term in a document is obtained by multiplying its TF and IDF scores:
TF-IDF(t, d) = TF(t, d) * IDF(t)

TF-IDF highlights terms that are frequent in a document but rare in the corpus, thus giving more weight to terms that are likely to be more informative and discriminative. It is commonly used in various natural language processing tasks such as text classification, information retrieval, and document clustering.

### 1-4. Implementation of the TF-IDF classifier

Let's break down the process step by step:

1. **Input**: The input to the TF-IDF classifier is a list of partitioned SOAP notes. Each SOAP note is initially divided into sections using "。" as a separator.

2. **Prediction**: The classifier predicts the section label for each partition in each SOAP note. For example, if a SOAP note has three partitions, the classifier predicts the labels for each of these partitions.

3. **Check for all labels (S, O, A, P)**: After prediction, if any partitioned SOAP note doesn't have all four labels (S, O, A, P), it indicates that the initial partitioning might not have been effective.

4. **Repartitioning**: In such cases, the system identifies the longest partition in the partitioned SOAP note. It then repartitions this longest partition using " " (space) as a separator. This step aims to break down the longest partition into smaller units to capture more comprehensive sections.

5. **Prediction on new partitions**: After repartitioning, the classifier predicts the section labels for the newly formed partitions.

6. **Updating predictions**: Finally, the predicted labels are updated based on the predictions made after repartitioning. These updated labels replace the previous predictions for the partitions in the SOAP note.
