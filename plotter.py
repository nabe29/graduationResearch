import serial
import time
import json

# ----- 設定 -----
COM_PORT = 'COM3'
BAUD_RATE = 115200
DELAY_DOT = 0.8

# ----- Arduino 接続 -----
ser = serial.Serial(COM_PORT, BAUD_RATE)
time.sleep(2)

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


def send_text(text):
    for ch in text:
        if ch == "\n":
            continue
        send_char(ch)


# ----- pattern を直接打刻 -----
def send_pattern(pattern):
    for i, dot_on in enumerate(pattern, start=1):
        if dot_on == 1:
            send_dot(i)


def send_braille_data(braille_data):
    for item in braille_data:
        send_pattern(item["pattern"])


# ----- メイン実行 -----
if __name__ == "__main__":
    mode = input("1: 文字入力打刻  2: 履歴ID打刻  選択してください: ")

    if mode == "1":
        text = input("打刻する文章を入力してください: ")
        send_text(text)
    elif mode == "2":
        # 履歴JSON読み込み
        with open("historyText.json", "r", encoding="utf-8") as f:
            history = json.load(f)

        target_id = int(input("打刻したい履歴IDを入力してください: "))
        for item in history:
            if item["id"] == target_id:
                braille_data = item["brailleData"]
                break
        else:
            print("指定したIDが見つかりません")
            exit()

        print("打刻開始")
        send_braille_data(braille_data)
    else:
        print("無効な選択です")
        exit()

    # 原点に戻す
    ser.write(b"HOME\n")
    time.sleep(2)
    print("原点に戻りました")
