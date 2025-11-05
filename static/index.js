async function sendText() {
  const input = document.getElementById("inputText").value;

  // 入力チェック
  if (!input.trim()) {
    document.getElementById("result").innerText = "文字を入力してください。";
    return;
  }

  const data = {
    text: input,
    time: new Date().toLocaleString()
  };

  // Flaskの /send にPOST送信
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
