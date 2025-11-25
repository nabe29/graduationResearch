from flask import Flask, request, jsonify, render_template
import json
import os
import plotter

app = Flask(__name__)

# 点字変換ライブラリの呼び出し
def convert_to_braille(text: str):
    with open("brailleConverter.json", "r", encoding="utf-8") as f:
        braille_map = json.load(f)
        result = []
        for ch in text:
            # 文字に対応する6点のパターンを取得（未定義は[0,0,0,0,0,0]）
            pattern = braille_map.get(ch, [0, 0, 0, 0, 0, 0])
            result.append({"char": ch, "pattern": pattern})
        return result

# ルートパスにアクセスされたことを検知
# '/'と結びついているのはindex()関数
@app.route('/')
def index():
    # templatesのhtmlファイルを表示する
    return render_template('index.html') 
 
# JSから送られてきたJSONデータを受け取る
# JSサイドで'/send'エンドポインタを指定している
@app.route('/send', methods=['POST'])
def send_textPy():
    # JSから送られたデータを受け取る
    data = request.get_json()
    text = data.get("text")

    # 点字変換を実行
    braille_data = convert_to_braille(text)

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

    # IDを自動で割り振る
    next_id = len(json_data) + 1

    # 新しいデータを追加
    json_data.append({
        "id":next_id,
        "text": text,
        "brailleData":braille_data,
        "lineNumber":"",
        "time": data.get("time")
    })

    # JSONとして保存
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # 発火ポイント
    # plotter.send_history_by_id(next_id)

    return jsonify({"message": f"'{text}' を保存しました！"})

if __name__ == '__main__':
    app.run(debug=True)
