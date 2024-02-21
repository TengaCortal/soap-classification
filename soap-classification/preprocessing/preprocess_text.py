import unicodedata
import neologdn


def preprocess(text):

    # Neologd Normalization
    text = neologdn.normalize(text)

    # Normalization Form Compatibility Composition (NFKC)
    text = unicodedata.normalize("NFKC", text)

    text = text.replace(",", "、")
    text = text.replace("，", "、")

    # remove full-width space
    text = text.replace("\u3000", "")

    return text
