# Pre-processing SOAP text and hybrid tokenization
This folder provides source code for pre-processing SOAP text for NLP and hybrid tokenization.<br>

> [!WARNING]
> The hybrid tokenization was not used in the final version of the SOAP classification model. Instead we used the MeCab tokenizer with Manbyo vocabulary added to it.

> [!IMPORTANT]
> To run hybrid_tokenization.py, you might need to adapt the paths to mecabrc and mecab-ipadic-neologd depending on your OS and installation

## 1. :zap: Quick setup :zap:

### 1-1. Execute setup.py 
Navigate to the root directory of the project and run the following command:
`python3 setup.py`

This will install python version 3.11 (required for neologdn) and the libraries that are required to execute the different modules.

> [!WARNING]
> If you are on a Windows-based OS, install python 3.11 manually and then run the folllowing command: 
>`python3.11 setup.py -c "install_libraries"`

Don't forget to change your VSCode python interpreter to version 3.11.


### 1-2. Install Mecab (Japanese morphological analyzer)

https://github.com/jinseikenai/uth-bert/blob/master/README.md

Mac の場合：https://qiita.com/paulxll/items/72a2bea9b1d1486ca751

- path to mecabrc: /opt/homebrew/etc/mecabrc
- path to mecab-ipadic-neologd: /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd


### 1-3. Install mecab-ipadic-neologd (general dictionary for Mecab)

`git clone https://github.com/neologd/mecab-ipadic-neologd.git`<br>
`cd mecab-ipadic-neologd`<br>
`sudo bin/install-mecab-ipadic-neologd -n -a`<br>


### 1-4. Edit /etc/mecabrc<br>
dicdir = /path/to/mecabrc<br>


## 2. Pre-processing text<br>

There is a preprocessing function tailored for Japanese text. Initially, it employs Neologd normalization, a process specifically designed for Japanese text, to standardize various linguistic aspects. Following this, it applies Unicode normalization using the NFKC form, ensuring consistency in character representation. Further, it replaces both English and full-width commas with a uniform separator, "、", promoting uniformity. Lastly, it eliminates full-width spaces, thereby optimizing the text for subsequent processing tasks. This comprehensive preprocessing sequence primes the text for effective handling and analysis.<br>

See [preprocess_text.py] for details<br>
 
## 3. Tokenization

In non-segmented languages such as Japanese, a tokenizer must accurately identify every word in a sentence before attempt to parse it and to do that requires a method of finding word boundaries without the aid of word delimiters. MecabTokenizer and FullTokenizerForMecab segment a word unit into several pieces of tokens included in BERT vocabulary.

See [tokenization_mod.py] for details<br>

## 4. Example

### Original text (soap from Nagoya clinic)

> 昨日より、左股関節を痛がる。歩行できない。　朝は歩けたが、夕方より歩行できなくなった。　現在も継続している。　先行する感染兆候　なし。4日前に、自転車の練習をしていてたくさん運動した。O) 圧痛　左股関節に。　Patrick ＋　Anterior impingement sign -。　Xp：明白な所見は認めず。A/P) 単純性股関節炎。　病態を説明。１週間経過を見てください。　歩行をしてしまったらそれでよいです

### After tokenization

> ['昨日', 'より', '左股関節', 'を', '痛', 'がる', '歩行', 'でき', 'ない', '朝', 'は', '歩け', 'た', 'が', '夕方', 'より', '歩行', 'でき', 'なく', 'なっ', 'た', '現在', 'も', '継続', 'し', 'て', 'いる', '先行', 'する', '感染兆候', 'なし', '4', '##日', '前', 'に', '自転車', 'の', '練習', 'を', 'し', 'て', 'い', 'て', 'たくさん', '運動', 'し', 'た', 'O', '圧痛', '左股関節', 'に', 'Patrick', '+', 'Anterior', 'impingement', 'sign', '-', 'X', '##p', '明', '##白', 'な', '所見', 'は', '認め', 'ず', 'A', 'P', '単純', '##性', '股関節', '##炎', '病態', 'を', '説明', '1', '##週', '##間', '経過', 'を', '見', 'て', 'ください', '歩行', 'を', 'し', 'て', 'しまっ', 'たら', 'それ', 'で', 'よい', 'です']

See [hybrid_tokenization.py] for details<br>



