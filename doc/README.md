# ドキュメンテーション

以下の理由からドキュメンテーションを作成しました。

- 明確さと理解
- 新しい開発者のオンボーディング
- 保守性
- APIリファレンス
- デバッグとトラブルシューティング

## Sphinxを使用したPythonドキュメンテーション

Sphinx（スフィンクス）は、Pythonプロジェクトのドキュメントを作成するためのツールです。Sphinxを使用すると、ソースコードから自動的にドキュメントを生成し、HTMLやPDFなどの形式で出力することができます。これにより、開発者はプロジェクトの構造やAPI、モジュールの説明などを簡単に記述し、分かりやすいドキュメントを提供することができます。Sphinxは柔軟でカスタマイズ可能なツールであり、多くのPythonプロジェクトで広く使用されています。

> [!NOTE]
>　Sphinxによるドキュメンテーションの生成プロセスは次のようになります：
>　プロジェクトのソースコード（Pythonまたはその他のサポートされる言語）→ reStructuredTextファイル → ドキュメンテーション（HTMLまたはそ 他のサポートされる形式）

## ドキュメンテーションの生成ガイド 

1. **sphinx-quickstartを使用してSphinxソースディレクトリを生成する**

        CLIUS-AI 
        ├── doc   
        └── soap_classification
            ├── data_cleaning
            └── preprocessing

    ```bash
    pip3 install sphinx
    mkdir doc 
    cd doc
    sphinx-quickstart
    ```

2. **Sphinxの拡張機能やテーマをインストール**

    ```bash
    pip3 install sphinxcontrib-napoleon
    pip3 install sphinx-rtd-theme
    pip3 install sphinx-rtd-size
    ```

3. **conf.pyを設定する**

    ```python
    import os
    import sys
    sys.path.insert(0, os.path.abspath(".."))
    sys.path.append(os.path.abspath("../.."))
    sys.path.append(os.path.abspath("../../soap_classification"))

    extensions = [
        "sphinx.ext.napoleon", "sphinx_rtd_size"
    ]

    sphinx_rtd_size_width = "100%"

    napoleon_google_docstring = True

    language = "ja"

    html_theme = "sphinx_rtd_theme"
    ```

4. **sphinx-apidocを使用してソースコードからreStructuredTextファイルを自動生成する**

    ```bash
    sphinx-apidoc -f -o <path-to-output> <path-to-module>
    ```

    例：

    ```bash
    sphinx-apidoc -f -o source/ ../soap_classification
    ```

4. **index.rstを編集する**

        CLIUS-AI (project folder)
        │
        ├── doc 
        │   ├── build 
        │   ├── source 
        │   │   ├── _static
        │   │   ├── _templates
        │   │   ├── conf.py
        │   │   ├── index.rst
        │   │   ├── modules.rst
        │   │   ├── ***.rst
        │   │   ├── ***.***.rst
        │   │   └── ***.***.rst
        │   ├── make.bat
        │   ├── Makefile
        │
        └── soap_classification
            ├── data_cleaning
            └── preprocessing

    ```
    .. toctree::
       :maxdepth: 3
       :caption: Contents:

       modules
    ```

5. **ドキュメンテーションをビルドする**

    ```bash
    make html
    ```

>[!NOTE]
>HTMLベースのドキュメントは、build/htmlに保存されます。生成されたドキュメンテーションを表示するには、VS Codeの拡張機能を使用してindex.htmlをプレビューするか、ブラウザでlocalhost（127.0.0.1）で開きます。

6. **ドキュメントの更新方**

    もし新しい関数やモジュールがorder_recommendに追加された場合は、まずその関数やモジュールに対してdocstringを書きます。そして、docフォルダに移動して次のコマンドを実行します：

    ```bash
    make clean 
    sphinx-apidoc -f -o source/ ../soap_classification
    make html
    ```
