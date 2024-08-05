# Machine Learning based SOAP Classification System

このプロジェクトは、マシンラーニングに基づくSOAP（Subjective, Objective, Assessment, Plan）分類システムの開発を含んでいます。

## データの利用について

本プロジェクトで使用されるデータは、プライバシーの問題により公開されておりません。

## モチベーション

このプロジェクトの主な動機の一つは、手動でのSOAPノート分類に必要な時間と労力を削減することにより、医療の文書化プロセスを合理化することです。SOAPノートの分類を自動化することで、医療専門家は患者のケアにより多くの時間を費やし、行政業務には少なくとも注力できるようになります。さらに、ノートの取り扱いに関する一貫性と標準化を確保し、医療提供者間のコミュニケーションの向上とケアの品質の向上につながる可能性があります。


## 現状

現時点では、提供されたコードは、11の日本のクリニックからのデータに対してさまざまな前処理タスクを実行し、分析および分類に使用されるデータを構築しています。

その後、TF-IDF（Term Frequency-Inverse Document Frequency）表現と機械学習アルゴリズムを組み合わせてSOAPノートを分類する最初のアプローチを提案します。この方法では、SOAPテキストをTF-IDFを使用して数値ベクトルに変換し、各用語（単語）のドキュメント内での相対的な重要性を表します。その後、これらのTF-IDFベクトル上で機械学習モデルをトレーニングして、各SOAPノートのセクションラベル（X、Subjective、Objective、Assessment、Plan）を予測します。

最後に、英日ハイブリッドトークナイザーが開発され、LSTMやUTH-BERTなどのより複雑な深層学習モデルに入力として機能するテキストデータを準備するために使用する予定です。

スクリプトの実行方法や出力の理解についての詳細な手順については、サブディレクトリ内の対応するREADMEファイルを参照してください。


## Table of Contents

1. [SOAP Data Construction](soap_classification/data_construction/README-日本語.md)
2. [SOAP Section Prediction](soap_classification/prediction/README-日本語.md)
3. [Pre-processing for NLP and Hybrid Tokenization](soap_classification/preprocessing/README-日本語.md)


## 追加の注意事項

- **要件:** READMEファイルの指示に従って、すべての必要な依存関係がインストールされていることを確認してください。
- **データセット:** 提供されたコードは、SOAPデータがCSVファイルに保存されていると仮定しています。データセットの形式に応じて、データの読み込みと前処理の手順を調整する必要があるかもしれません。