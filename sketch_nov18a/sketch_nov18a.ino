// ====== Arduino Braille Puncher ======
// PC(Python) からのコマンド:
//
// MOVE x y   → XY移動
// PUNCH      → 打刻
// HOME       → ホーム位置へ戻る
// PING       → "OK" を返す（Python の接続確認）
//
// ======================================

#include <AccelStepper.h>

// --- モーター設定（例） ---
AccelStepper stepperX(AccelStepper::DRIVER, 2, 5); // STEP=2, DIR=5
AccelStepper stepperY(AccelStepper::DRIVER, 3, 6); // STEP=3, DIR=6

// 打刻ソレノイド
const int PIN_PUNCH = 9;

// ホームスイッチ
const int PIN_HOME_X = 10;
const int PIN_HOME_Y = 11;

// 座標 → ステップ変換係数
const float STEPS_PER_MM_X = 80;  // 例：1mm = 80step
const float STEPS_PER_MM_Y = 80;

void setup() {
  Serial.begin(115200);

  pinMode(PIN_PUNCH, OUTPUT);
  pinMode(PIN_HOME_X, INPUT_PULLUP);
  pinMode(PIN_HOME_Y, INPUT_PULLUP);

  stepperX.setMaxSpeed(2000);
  stepperX.setAcceleration(2000);

  stepperY.setMaxSpeed(2000);
  stepperY.setAcceleration(2000);

  homeAll();
  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // ----- PING 応答 -----
    if (cmd == "PING") {
      Serial.println("OK");
    }

    // ----- HOME -----
    else if (cmd == "HOME") {
      homeAll();
      Serial.println("DONE");
    }

    // ----- PUNCH -----
    else if (cmd == "PUNCH") {
      punch();
      Serial.println("DONE");
    }

    // ----- MOVE x y -----
    else if (cmd.startsWith("MOVE")) {
      float x, y;
      sscanf(cmd.c_str(), "MOVE %f %f", &x, &y);
      moveToXY(x, y);
      Serial.println("DONE");
    }

    // ----- 不明コマンド -----
    else {
      Serial.println("ERR");
    }
  }
}

// =============================
//   XY 移動
// =============================
void moveToXY(float x_mm, float y_mm) {
  long targetX = x_mm * STEPS_PER_MM_X;
  long targetY = y_mm * STEPS_PER_MM_Y;

  stepperX.moveTo(targetX);
  stepperY.moveTo(targetY);

  while (stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) {
    stepperX.run();
    stepperY.run();
  }
}

// =============================
//   打刻
// =============================
void punch() {
  digitalWrite(PIN_PUNCH, HIGH);
  delay(120);   // 打刻時間
  digitalWrite(PIN_PUNCH, LOW);
  delay(50);
}

// =============================
//   ホームに戻る
// =============================
void homeAll() {
  // X軸ホーム
  stepperX.setSpeed(-500);
  while (digitalRead(PIN_HOME_X) == HIGH) {
    stepperX.runSpeed();
  }
  stepperX.setCurrentPosition(0);

  // Y軸ホーム
  stepperY.setSpeed(-500);
  while (digitalRead(PIN_HOME_Y) == HIGH) {
    stepperY.runSpeed();
  }
  stepperY.setCurrentPosition(0);

  delay(200);
  Serial.println("HOME_OK");
}

