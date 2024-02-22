import unicodedata
import neologdn


def preprocess(text):
    """Preprocesses the input text by applying various normalization and formatting steps.

    Args:
        text (str): The input text to be preprocessed.

    Returns:
        str: The preprocessed text after applying normalization and formatting.
    """
    # Neologd Normalization
    text = neologdn.normalize(text)

    # Normalization Form Compatibility Composition (NFKC)
    text = unicodedata.normalize("NFKC", text)

    text = text.replace(",", "、")
    text = text.replace("，", "、")

    # remove full-width space
    text = text.replace("\u3000", "")

    return text
