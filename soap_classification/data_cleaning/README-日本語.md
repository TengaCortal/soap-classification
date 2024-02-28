## SOAPデータセットの処理

この一連のPythonスクリプトは、CSVファイルに保存されたSOAP（Subjective, Objective, Assessment, Plan）データを処理します。各スクリプトは、データの取得からテキストのクリーニング、語彙の抽出までの処理パイプラインで特定のタスクを実行します。以下に、各スクリプトの概要とその入出力を示します。

| スクリプト名            | <div style="width:290px">説明</div>                                                                                    | 入力                            | 出力                           |
|------------------------|----------------------------------------------------------------------------------------|---------------------------------|--------------------------------|
| `only_soap.py`         | SOAPデータを含むCSVファイルから最初の列を抽出します。                                   | `processed_data_clinicName/DB_soap_orderCode.csv` | `clinicName_soap.csv`：最初の列のみを含む |
| `regex.py`             | CSVファイル内の特定の正規表現パターンを含む行の数をカウントします。                    | `clinicName_soap.csv`            | 一致する行の数                  |
| `total_soap.py`        | 複数のSOAP CSVファイルを1つのCSVファイルに結合します。                                    | `resources/soaps/*.csv`       | `combined_soaps.csv`：すべてのSOAPデータを含む |
| `retrieve_classified_soaps.py` | 特定の正規表現パターンを含む行を取得します。                                              | `combined_soaps.csv`           | ヘッダー行が追加された `classified_soaps.csv` |
| `unify_syntax.py`      | 特定のパターンを置換し、構文を標準化してSOAPデータを修正します。                         | `classified_soaps.csv`         | 修正された構文を含む `unified_syntax_soap.csv` |
| `remove_undesired.py`  | 不要な文字や望ましくないパターンを含む行を削除してSOAPデータをクリーニングします。         | `unified_syntax_soap.csv`      | クリーニングされたデータを含む `cleaned_classified_soaps.csv` |
| `extract_english_vocabulary.py` | クリーニングされたSOAPデータから一意の英単語を抽出します。                               | `cleaned_classified_soaps.csv` | 一意の英単語を含む `clinics_english_words.txt` |

通常、これらのスクリプトは上記の順序で実行され、データ処理パイプラインが完了します。各スクリプトの出力は、次のスクリプトの入力として使用されます。