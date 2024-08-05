# SOAPテキストの前処理とハイブリッドトークン化
このフォルダでは、SOAPテキストの前処理とハイブリッドトークン化のためのソースコードが提供されています。


> [!WARNING]
> ハイブリッドトークン化はSOAP分類モデルの最終版では使用されませんでした。代わりに、Manbyo語彙を追加したMeCabトークナイザーを使用しました。

> [!IMPORTANT]
> hybrid_tokenization.pyを実行するには、OSとインストールに応じてmecabrcとmecab-ipadic-neologdへのパスを適応する必要があります。

## 1. :zap: クイックセットアップ :zap:

### 1-1. setup.pyを実行
プロジェクトのルートディレクトリに移動し、次のコマンドを実行してください：
`python3 setup.py`

これにより、pythonバージョン3.11（neologdnに必要）と、異なるモジュールを実行するために必要なライブラリがインストールされます。

> [!WARNING]
> WindowsベースのOSの場合、手動でpython 3.11をインストールしてから次のコマンドを実行してください：
> `python3.11 setup.py -c "install_libraries"`

VSCodeのPythonインタープリターをバージョン3.11に変更することを忘れないでください。

### 1-2. Mecabをインストール（日本語形態素解析器）

https://github.com/jinseikenai/uth-bert/blob/master/README.md

Macの場合：https://qiita.com/paulxll/items/72a2bea9b1d1486ca751

- mecabrcへのパス：/opt/homebrew/etc/mecabrc
- mecab-ipadic-neologdへのパス：/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd

### 1-3. mecab-ipadic-neologdをインストール（Mecab用の一般辞書）

`git clone https://github.com/neologd/mecab-ipadic-neologd.git`<br>
`cd mecab-ipadic-neologd`<br>
`sudo bin/install-mecab-ipadic-neologd -n -a`<br>

### 1-4. /etc/mecabrcを編集
dicdir = mecab-ipadic-neologdへのパス

## 2. テキストの前処理

日本語テキスト用に特別に作成された前処理関数があります。最初に、日本語テキスト用に設計されたNeologd正規化を使用して、さまざまな言語的側面を標準化します。これに続いて、NFKC形式を使用したUnicode正規化を適用し、文字の表現の一貫性を確保します。さらに、英語と全角コンマを統一されたセパレーター "、" で置き換え、一貫性を促進します。最後に、全角スペースを削除して、テキストを後続の処理タスクに最適化します。この包括的な前処理シーケンスにより、テキストが効果的に処理および分析できるようになります。

詳細は[preprocess_text.py]を参照してください。

## 3. トークン化

日本語のような非セグメント化された言語では、解析する前に文中のすべての単語を正確に特定する必要がありますが、それを行うには、単語区切り文字の支援なしに単語の境界を見つける方法が必要です。 MecabTokenizerとFullTokenizerForMecabは、単語ユニットをBERT語彙に含まれる複数のトークンの一部に分割します。

詳細は[tokenization_mod.py]を参照してください。

## 4. 例

### 元のテキスト（名古屋クリニックからのSOAP）

> 昨日より、左股関節を痛がる。歩行できない。　朝は歩けたが、夕方より歩行できなくなった。　現在も継続している。　先行する感染兆候　なし。4日前に、自転車の練習をしていてたくさん運動した。O) 圧痛　左股関節に。　Patrick ＋　Anterior impingement sign -。　Xp：明白な所見は認めず。A/P) 単純性股関節炎。　病態を説明。１週間経過を見てください。　歩行をしてしまったらそれでよいです

### トークン化後

> ['昨日', 'より', '左股関節', 'を', '痛', 'がる', '歩行', 'でき', 'ない', '朝', 'は', '歩け', 'た', 'が', '夕方', 'より', '歩行', 'でき', 'なく', 'なっ', 'た', '現在', 'も', '継続', 'し', 'て', 'いる', '先行', 'する', '感染兆候', 'なし', '4', '##日', '前', 'に', '自転車', 'の', '練習', 'を', 'し', 'て', 'い', 'て', 'たくさん', '運動', 'し', 'た', 'O', '圧痛', '左股関節', 'に', 'Patrick', '+', 'Anterior', 'impingement', 'sign', '-', 'X', '##p', '明', '##白', 'な', '所見', 'は', '認め', 'ず', 'A', 'P', '単純', '##性', '股関節', '##炎', '病態', 'を', '説明', '1', '##週', '##間', '経過', 'を', '見', 'て', 'ください', '歩行', 'を', 'し', 'て', 'しまっ', 'たら', 'それ', 'で', 'よい', 'です']

詳細は[hybrid_tokenization.py]を参照してください。