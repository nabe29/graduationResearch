async function sendText() {
  const input = document.getElementById("inputText").value;

  // 入力チェック：空白や未入力の場合はエラーメッセージを表示して処理を止める
  if (!input.trim()) {
    document.getElementById("result").innerText = "文字を入力してください。";
    return;
  }

  // 送信するデータをオブジェクト形式で作成
  // timeには現在時刻を文字列で入れる
  const data = {
    text: input,
    time: new Date().toLocaleString()
  };

  // Flaskサーバーの「/send」エンドポイントにデータを送信する
  // fetch() は非同期通信を行う関数
  const res = await fetch("/send", {
    // HTTPメソッドを指定（POST）
    method: "POST",

    // 送るデータの形式をJSONとして指定
    headers: {
      "Content-Type": "application/json"
    },

    // JavaScriptのオブジェクトをJSON文字列に変換して送信
    body: JSON.stringify(data)
  });

  // Flask側から返ってきたレスポンス（JSON形式）を解析
  const result = await res.json();

  // Flaskが返したメッセージを画面に表示
  document.getElementById("result").innerText = result.message;
}
