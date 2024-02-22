from preprocess_text import preprocess as my_preprocess
from tokenization_mod import MecabTokenizer, FullTokenizerForMecab
from bert import tokenization
import re
import os
import sys
from absl import flags

# define paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_PATH = os.path.join(BASE_PATH, "resources")
MECABRC_PATH = "/opt/homebrew/etc/mecabrc"
os.environ["MECABRC"] = MECABRC_PATH

# set the flags for Bert
sys.argv = ["preserve_unused_tokens=False"]
flags.FLAGS(sys.argv)


def detect_language(text):
    """Detects the language of the input text.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        str: The detected language of the text, either "ja" for Japanese or "en" for English.
    """
    # check if theres are japanese characters
    if re.search(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]", text):
        return "ja"
    else:
        return "en"


if __name__ == "__main__":

    # special token for a Person's name
    name_token = "＠＠Ｎ"

    # path to the mecab-ipadic-neologd
    mecab_ipadic_neologd = "/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd"

    # path to the J-Medic (We used MANBYO_201907_Dic-utf8.dic)
    mecab_J_medic = os.path.join(RESOURCES_PATH, "MANBYO_201907_Dic-utf8.dic")

    # path to the uth-bert vocabulary
    vocab_file_jap = os.path.join(RESOURCES_PATH, "uthbert_vocab.txt")

    # path to the BioBert vocabulary
    vocab_file_eng = os.path.join(RESOURCES_PATH, "biobert_vocab.txt")

    # MecabTokenizer
    sub_tokenizer = MecabTokenizer(
        mecab_ipadic_neologd=mecab_ipadic_neologd,
        mecab_J_medic=mecab_J_medic,
        name_token=name_token,
    )

    # FullTokenizerForMecab for Japanese
    tokenizer_japanese = FullTokenizerForMecab(
        sub_tokenizer=sub_tokenizer, vocab_file=vocab_file_jap, do_lower_case=False
    )

    # FullTokenizer for English
    tokenizer_english = tokenization.FullTokenizer(
        vocab_file=vocab_file_eng, do_lower_case=False
    )

    # pre process and tokenize example
    original_text = "昨日より、左股関節を痛がる。歩行できない。　朝は歩けたが、夕方より歩行できなくなった。　現在も継続している。　先行する感染兆候　なし。4日前に、自転車の練習をしていてたくさん運動した。O) 圧痛　左股関節に。　Patrick ＋　Anterior impingement sign -。　Xp：明白な所見は認めず。A/P) 単純性股関節炎。　病態を説明。１週間経過を見てください。　歩行をしてしまったらそれでよいです"

    print("Original text:", original_text)
    print()

    pre_processed_text = my_preprocess(original_text)

    separators = r"[。、：: 、,)/）／ ]"
    splitted_text = re.split(separators, pre_processed_text)

    # Hybrid Tokenization based on language (japanese or english)
    segments = []
    current_segment = {"text": "", "language": None}

    for word in splitted_text:
        language = detect_language(word)
        if current_segment["language"] is None:
            current_segment["language"] = language
        elif current_segment["language"] != language:
            segments.append(current_segment)
            current_segment = {"text": "", "language": language}
        current_segment["text"] += word + " "

    segments.append(current_segment)

    tokens = []

    for segment in segments:
        if segment["language"] == "ja":
            # Japanese Tokenization
            output_tokens = tokenizer_japanese.tokenize(segment["text"])
        else:
            # English Tokenization
            output_tokens = tokenizer_english.tokenize(segment["text"])

        tokens.extend(output_tokens)
        # print("Language:", segment['language'])
        # print("Tokenized text:", ' '.join(output_tokens))

    print("Tokenized text:", tokens)
