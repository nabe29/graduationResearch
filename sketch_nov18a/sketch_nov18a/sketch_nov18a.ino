#include <Servo.h>

// ---- Stepper 設定 ----
const long stepsPerRevolution = 4096;  // 28BYJ-48 半ステップ
const float mmPerRev = 20.0;           // 機構に合わせて調整
const float stepsPerMm = stepsPerRevolution / mmPerRev;

// 点字間隔
const float pitchX = 2.5;  // 横方向間隔（mm）
const float pitchY = 2.6;  // 縦方向間隔（mm）

// X軸ピン
int xPins[4] = {2, 3, 4, 5};
// Y軸ピン
int yPins[4] = {A0, A1, A2, A3};

// 半ステップ配列
int seq[8][4] = {
  {1,0,0,0},
  {1,1,0,0},
  {0,1,0,0},
  {0,1,1,0},
  {0,0,1,0},
  {0,0,1,1},
  {0,0,0,1},
  {1,0,0,1}
};

// サーボ設定
Servo myServo;
int servoPin = 11;
int servoPress = 0;
int servoRelease = 90;
int servoDelayMs = 250;

float currentX = 0;
float currentY = 0;

void setup() {
  for (int i=0; i<4; i++){
    pinMode(xPins[i], OUTPUT);
    pinMode(yPins[i], OUTPUT);
  }
  myServo.attach(servoPin);
  myServo.write(servoRelease);
  Serial.begin(115200);
  Serial.println("READY");
}

// --- ステッパー制御 ---
void stepMotor(int motorPins[], int stepIndex){
  for(int i=0; i<4; i++){
    digitalWrite(motorPins[i], seq[stepIndex][i]);
  }
}

void rotateSteps(int motorPins[], long steps, int delayMs){
  int dir = (steps>=0)?1:-1;
  long s = abs(steps);
  for(long i=0;i<s;i++){
    int idx = (i*dir)%8;
    if(idx<0) idx+=8;
    stepMotor(motorPins, idx);
    delay(delayMs);
  }
}

// --- 移動 ---
void moveTo(float targetX, float targetY){
  long sX = (targetX - currentX) * stepsPerMm;
  long sY = (targetY - currentY) * stepsPerMm;
  rotateSteps(xPins, sX, 2);
  rotateSteps(yPins, sY, 2);
  currentX = targetX;
  currentY = targetY;
}

// --- 打刻 ---
void dot(){
  myServo.write(servoPress);
  delay(servoDelayMs);
  myServo.write(servoRelease);
  delay(servoDelayMs);
}

// --- ドット番号 → 座標 ---
void moveToDot(int dotNumber){
  float tx=0, ty=0;
  switch(dotNumber){
    case 1: tx=0;       ty=0; break;
    case 2: tx=0;       ty=pitchY; break;
    case 3: tx=0;       ty=pitchY*2; break;
    case 4: tx=pitchX;  ty=0; break;
    case 5: tx=pitchX;  ty=pitchY; break;
    case 6: tx=pitchX;  ty=pitchY*2; break;
  }
  moveTo(tx, ty);
}

// 追加部分：loop() に HOME コマンド対応

void loop(){
  if(Serial.available()){
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // HOME コマンド
    if(cmd == "HOME"){
      moveTo(0, 0);
      Serial.println("HOME_DONE");
      return;
    }

    // 数字ドット
    int d = cmd.toInt();
    if(d>=1 && d<=6){
      moveToDot(d);
      dot();
      Serial.println(d);
    }
  }
}

