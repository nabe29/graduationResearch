from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # ← あなたのHTMLを表示

@app.route('/send', methods=['POST'])
def send_text():
    # JSから送られたデータを受け取る
    data = request.get_json()
    text = data.get("text")

    # 保存先
    file_path = 'historyText.json'

    # 既存データを読み込み（なければ空リスト）
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                json_data = json.load(f)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []

    # 新しいデータを追加
    json_data.append({
        "text": text,
        "time": data.get("time")
    })

    # JSONとして保存
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    return jsonify({"message": f"'{text}' を保存しました！"})

if __name__ == '__main__':
    app.run(debug=True)
