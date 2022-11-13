#include <Servo.h>
Servo SprayHead;
int SensePin=10;
int ServoPin=9;
int A_min=20;
int A_spray=65;

void setup() {
SprayHead.attach(ServoPin);
pinMode(SensePin,INPUT);
SprayHead.write(A_min);
}

void loop() {
if(digitalRead(SensePin)==LOW )
    SprayHead.write(A_min);
else
      SprayHead.write(A_spray);
}
