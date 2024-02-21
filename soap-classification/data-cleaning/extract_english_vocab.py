import pandas as pd
import re
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")

# Load the cleaned and classified SOAP dataset from CSV
cleaned_soaps = pd.read_csv(os.path.join(SOAPS_PATH, "cleaned_classified_soaps.csv"), header=None)

# Define a regex pattern to match English words
english_word_pattern = re.compile(r'\b[A-Za-z]+\b')

# Function to extract English words from text
def extract_english_words(text):
    return english_word_pattern.findall(str(text))

# Apply the function to each row of the DataFrame
english_words = cleaned_soaps.map(extract_english_words)

# Flatten the list of English words
unique_english_words = set(word for sublist in english_words.values.flatten() for word in sublist)


print(unique_english_words)

# Save the unique English words to a text file
with open(os.path.join(BASE_PATH, "resources/clinics_english_words.txt"), "w") as file:
    for word in unique_english_words:
        file.write(word + "\n")