import serial
import time

ser = serial.Serial('COM3', 115200)
time.sleep(2)  # Arduino 起動待ち

dots = [1, 2, 4]

for d in dots:
    ser.write(f"{d}\n".encode())
    time.sleep(1)  # サーボ動作待ち
