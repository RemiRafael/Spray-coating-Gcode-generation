#include <Servo.h>
Servo SprayHead;
int SensePin=10;
int ServoPin=9;

void setup() {
SprayHead.attach(ServoPin);
pinMode(SensePin,INPUT);
SprayHead.write(65);
}

void loop() {
if(digitalRead(SensePin)==HIGH )
    SprayHead.write(20);
else
      SprayHead.write(65);
}
