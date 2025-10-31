from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    # index.htmlを表示
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def receive_text():
    # フロントから送信されたJSONを受け取る
    data = request.get_json()
    user_text = data.get("text")  # "text"キーの値を取得
    print(f"受信した文字列: {user_text}")  # コンソール出力
    # 返却データ（JSON）
    return jsonify({"message": f"Pythonで受け取りました: {user_text}"})

if __name__ == "__main__":
    app.run(debug=True)
