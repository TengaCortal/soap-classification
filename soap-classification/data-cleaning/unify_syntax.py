import pandas as pd
import re
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")

# Load the SOAP dataset from CSV
soaps = pd.read_csv(os.path.join(SOAPS_PATH, "classified_soaps.csv"))

soap_notes = soaps.iloc[:, 0]
soap_notes.name = "soap"

# Define the pattern
S_pattern = re.compile(r'。S\)| S。|。S）|。S |"S|S:|\(S\)|（S）|nS|S：|"S。|。S。|S\.|。Ｓ|Ｓ）|<S>|S\)')
O_pattern = re.compile(r'。O\)| O。|。O）|。O |O:|\(O\)|（O）|nO|O：|。O。|O\.|。Ｏ|Ｏ）|<O>|O\)')
A_pattern = re.compile(r'。A\)| A。|。A）|。A |A:|\(A\)|（A）|nA|A：|。A。|A\.|。Ａ|Ａ）|<A>|A\)')
P_pattern = re.compile(r'。P\)| P。|。P）|。P |P:|\(P\)|（P）|nP|P：|。P。|P\.|。Ｐ|Ｐ）|<P>|P\)')

# Function to replace patterns with "SUB:"
def replace_sub(text):
    text = re.sub(S_pattern, " SUB:", text)
    text = re.sub(O_pattern, " OBJ:", text)
    text = re.sub(A_pattern, " ASM:", text)
    text = re.sub(P_pattern, " PLN:", text)
    return text

# Apply the function to the 'soap' column
unified_soaps = soap_notes.apply(replace_sub)

# Save the modified DataFrame to a new CSV file
unified_soaps.to_csv(os.path.join(SOAPS_PATH, "unified_syntax_soap.csv"), index=False, header=False)
