from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.append("..")  # ルートディレクトリへのパスを追加
import soap_classification.prediction.TFIDF.tfidf_classifier as tc


abs_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(abs_path, "..")

# suggest~をデモの場合にして実行
app = Flask(__name__)


# ホームページの表示
@app.route("/")
def home():
    return render_template("index.html")


# 分類処理を行うエンドポイント
@app.route("/classify", methods=["POST"])
def classify():
    # リクエストからJSON形式のデータを取得する
    request_data = request.json

    # JSONデータからSOAPデータを取得する
    soap_data = request_data.get("soap")

    if soap_data is None:
        return jsonify({"error": "SOAPデータが提供されていません"}), 400

    # ここでSOAPデータを分類する処理を実行し、結果を取得する
    result = tc.for_demo(soap_data)

    # 分類結果をJSON形式で返す
    return jsonify({"soap": soap_data, "result": result})


if __name__ == "__main__":
    app.run(debug=True)
