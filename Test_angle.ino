#include <Servo.h>
Servo SprayHead;
int ServoPin=9;

int Taget_angle=0;  // Change the value in this line and reload to go to the angle you desire

void setup() {
SprayHead.attach(ServoPin);
}

void loop() {
    SprayHead.write(Taget_angle); 
}
