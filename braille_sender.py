import serial
import time
import json

# ----- 設定 -----
COM_PORT = 'COM3'      # Arduino UNO のポート
BAUD_RATE = 115200
DELAY_DOT = 0.8        # 1点打刻後の待機時間(秒)
CHAR_SPACING = 6       # 文字間隔を無視する場合は使わない
LINE_SPACING = 10      # 改行時のY移動は未対応（今の単純コードでは無視）

# ----- Arduino 接続 -----
ser = serial.Serial(COM_PORT, BAUD_RATE)
time.sleep(2)  # Arduino 起動待ち

# ----- JSON 読み込み -----
with open("braille.json", encoding="utf-8") as f:
    BRAILLE = json.load(f)

# ----- 点字ドット送信 -----
def send_dot(d):
    """Arduino にドット番号を送信"""
    if 1 <= d <= 6:
        ser.write(f"{d}\n".encode())
        print(f"Sent dot: {d}")
        time.sleep(DELAY_DOT)

# ----- 文字打刻 -----
def send_char(ch):
    """1文字分の点字を送信"""
    if ch not in BRAILLE:
        print(f"未対応文字: {ch}")
        return

    pattern = BRAILLE[ch]  # [0,1,0,1,1,0] の6点
    for i, dot_on in enumerate(pattern, start=1):
        if dot_on == 1:
            send_dot(i)

# ----- 文章打刻 -----
def send_text(text):
    for ch in text:
        if ch == "\n":
            continue  # 改行時は単純にスキップ（必要ならY移動追加）
        send_char(ch)

# ----- 実行例 -----
if __name__ == "__main__":
    text = input("打刻する文章を入力してください: ")
    send_text(text)
    print("打刻完了")

    # ---- 追加部分: 原点に戻す ----
    ser.write(b"HOME\n")
    time.sleep(2)  # 移動待ち
    print("原点に戻しました")

