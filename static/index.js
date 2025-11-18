// /static/index.js
async function sendText() {
  const input = document.getElementById("inputText").value;

  // 入力チェック：空白や未入力の場合
  if (!input.trim()) {
    document.getElementById("result").innerText = "文字を入力してください。";
    return;
  }

  // ひらがなのみかチェック
  if (!checkHiragana(input)) {
    document.getElementById("result").innerText = "ひらがなのみ入力してください。";
    return;
  }

  // データ作成
  const data = {
    text: input,
    time: new Date().toLocaleString()
  };

  // Flaskサーバーに送信
  const res = await fetch("/send", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  document.getElementById("result").innerText = result.message;
}

// ひらがなのみか判定する関数
function checkHiragana(input) {
  const hiraganaRegex = /^[ぁ-んー\s]+$/;
  return hiraganaRegex.test(input);
}
