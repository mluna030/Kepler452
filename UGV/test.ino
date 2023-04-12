#include <PIDLoop.h>
#include <Pixy2.h>
#include <SPI.h>
#include <Servo.h>

Pixy2 pixy;

#define SERVO_XPIN 2
#define SERVO_ZPIN 3

Servo servoTilt;  // servo control object
Servo servoPan;

int panAngle = 0;
int tiltAngle = 0;

int panMin = 0;
int panMax = 180;
int tiltMin = 0;
int tiltMax = 55;

int panStep = 15;
int tiltStep = 5;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pixy.init();

  pinMode(SERVO_XPIN, OUTPUT);
  pinMode(SERVO_ZPIN, OUTPUT);

  //pixy.changeProg("color_connected_components");

  setServo(SERVO_ZPIN, panAngle);
  setServo(SERVO_XPIN, tiltAngle);

}

void loop() 
{
  int numBlocks = pixy.ccc.getBlocks();
  if (numBlocks > 0)
  {
    int errorX = (int)(pixy.ccc.blocks[0].m_x - 160);
    int errorY = (int)(pixy.ccc.blocks[0].m_y - 100);

    panAngle -= map(errorX, -160, 160, -panStep, panStep);
    if (panAngle < panMin) panAngle = panMin;
    if (panAngle > panMax) panAngle = panMax;
    setServo(SERVO_ZPIN, panAngle);

    tiltAngle -= map(errorY, -100, 100, -tiltStep, tiltStep);
    if (tiltAngle < tiltMin) tiltAngle = tiltMin;
    if (tiltAngle > tiltMax) tiltAngle = tiltMax;
    setServo(SERVO_XPIN, tiltAngle);
  }
  else
  {
    setServo(SERVO_ZPIN, 0);
    setServo(SERVO_XPIN, 0);
  }
}

void setServo(int pin, int angle) 
{
  int pwm = map(angle, 0, 180, 544, 2400);
  digitalWrite(pin, HIGH);
  delayMicroseconds(pwm);
  digitalWrite(pin, LOW);
}
