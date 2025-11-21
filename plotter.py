import serial
import time
import json

# ----- 設定 -----
COM_PORT = 'COM3'
BAUD_RATE = 115200
DELAY_DOT = 0.8

# ----- Arduino 接続 -----
def connect_arduino(port=COM_PORT, baud=BAUD_RATE):
    ser = serial.Serial(port, baud)
    time.sleep(2)
    return ser

ser = connect_arduino()

# ----- JSON 読み込み -----
with open("brailleConverter.json", encoding="utf-8") as f:
    BRAILLE = json.load(f)

# ----- 点字ドット送信 -----
def send_dot(d):
    if 1 <= d <= 6:
        ser.write(f"{d}\n".encode())
        print(f"Sent dot: {d}")
        time.sleep(DELAY_DOT)

# ----- 文字打刻 -----
def send_char(ch):
    if ch not in BRAILLE:
        print(f"未対応文字: {ch}")
        return
    pattern = BRAILLE[ch]
    for i, dot_on in enumerate(pattern, start=1):
        if dot_on == 1:
            send_dot(i)

def send_text_input(text):
    """文章を打刻する"""
    for ch in text:
        if ch == "\n":
            continue
        send_char(ch)
    return_to_home()

# ----- pattern を直接打刻 -----
def send_pattern(pattern):
    for i, dot_on in enumerate(pattern, start=1):
        if dot_on == 1:
            send_dot(i)

def send_braille_data(braille_data):
    for item in braille_data:
        send_pattern(item["pattern"])
    return_to_home()

# ----- 履歴IDから打刻 -----
def send_history_by_id(target_id):
    """履歴JSONから指定IDのbrailleDataを打刻"""
    with open("historyText.json", "r", encoding="utf-8") as f:
        history = json.load(f)

    for item in history:
        if item["id"] == target_id:
            print(f"打刻開始: ID={target_id}")
            send_braille_data(item["brailleData"])
            return

    print(f"指定したID {target_id} が見つかりません")

# ----- 原点復帰 -----
def return_to_home():
    ser.write(b"HOME\n")
    time.sleep(2)
    print("原点に戻りました")

# ----- メイン例 -----
if __name__ == "__main__":
    # 文字列打刻例
    send_text_input("こんにちは")

    # 履歴ID打刻例
    send_history_by_id(3)
