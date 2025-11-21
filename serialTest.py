import serial

try:
    ser = serial.Serial('COM3', 115200)
    print("接続成功")
    ser.close()
except Exception as e:
    print(e)
