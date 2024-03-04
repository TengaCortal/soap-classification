## データ構築

この一連のPythonスクリプトは、CSVファイルに保存されたSOAP（Subjective, Objective, Assessment, Plan）データを処理します。各スクリプトは、データの取得からテキストのクリーニング、語彙の抽出までの処理パイプラインで特定のタスクを実行します。以下に、各スクリプトの概要とその入出力を示します。


| スクリプト名            | <br> 説明 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                                                  | 入力                            | 出力                           |
|------------------------|----------------------------------------------------------------------------------------|---------------------------------|--------------------------------|
| `only_soap.py`         | SOAPデータを含むCSVファイルから最初の列を抽出。                                   | `processed_data_clinicName/DB_soap_orderCode.csv` | `clinicName_soap.csv`：最初の列のみを含む |
| `regex.py`             | CSVファイル内の特定の正規表現パターンを含む行の数をカウント。                    | `clinicName_soap.csv`            | 一致する行の数                  |
| `total_soap.py`        | 複数のSOAP CSVファイルを1つのCSVファイルに結合。                                    | `resources/soaps/*.csv`       | `combined_soaps.csv`：すべてのSOAPデータを含む |
| `retrieve_classified_soaps.py` | 特定の正規表現パターンを含む行を取得。                                              | `combined_soaps.csv`           | ヘッダー行が追加された `classified_soaps.csv` |
| `unify_syntax.py`      | 特定のパターンを置換し、構文を標準化してSOAPデータを修正。                         | `classified_soaps.csv`         | 修正された構文を含む `unified_syntax_soap.csv` |
| `remove_undesired.py`  | 不要な文字や望ましくないパターンを含む行を削除してSOAPデータをクリーニング。         | `unified_syntax_soap.csv`      | クリーニングされたデータを含む `cleaned_classified_soaps.csv` |
| `extract_english_vocabulary.py` | クリーニングされたSOAPデータから一意の英単語を抽出。                               | `cleaned_classified_soaps.csv` | 一意の英単語を含む `clinics_english_words.txt` |
| `split_soap_sections.py` | クリーンおよび分類されたSOAPノートから、各セクション（X, SUB、OBJ、ASM、PLN）ごとに個別のCSVファイルを作成します。 | `cleaned_classified_soaps.csv` | 各セクションのCSVファイルが`soap_sections`ディレクトリに保存されます。 |
| `create_labeled_dataset.py` | 別々のCSVファイル（X、SUB、OBJ、ASM、PLN）からのセクションを結合して、単一のラベル付きデータセットCSVファイルを作成します。 | 各セクションのCSVファイル（`x_sections.csv`、`sub_sections.csv`、`obj_sections.csv`、`asm_sections.csv`、`pln_sections.csv`） | 対応するラベル付きセクションを含む`labeled_dataset.csv` |

通常、これらのスクリプトは、データ構築パイプラインを完了するために上記の順に実行されます（regex.pyとextract_english_vocabulary.pyを除く）。各スクリプトの出力は、次のスクリプトの入力として機能します。
