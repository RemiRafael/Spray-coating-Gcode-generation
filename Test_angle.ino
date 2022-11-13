#include <Servo.h>
Servo SprayHead;
// int SensePin=10;
int ServoPin=9;
int ServoState=0;

int Taget_angle=0;  // Change the value in this line and reload to go to the angle you desire

void setup() {
  // put your setup code here, to run once:
SprayHead.attach(ServoPin);
//pinMode(SensePin,INPUT);
SprayHead.write(20);
}

void loop() {
  // put your main code here, to run repeatedly:

    SprayHead.write(Taget_angle);
    
}
