// Include the AccelStepper library:
#include <AccelStepper.h>
// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin 2
#define stepPin 3
#define Potentiometer A0
#define motorInterfaceType 1
int Value[]={0,0,0,0,0};
int Stepper_Speed=0;
int i=0, Buff=0;
// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);
void setup() {
  // Set the maximum speed in steps per second:
  stepper.setMaxSpeed(1300);
  pinMode(Potentiometer, INPUT);

  // Define as 1/8 steps
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(5, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);
  // Enable pin
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
}
void loop() {
  Value[i]=analogRead(Potentiometer);
  i=(i+1)%5;
  Buff=(Value[0]+Value[1]+Value[2]+Value[3]+Value[4])/5;
  if (Buff>Stepper_Speed+5 || Buff<Stepper_Speed-5)
    Stepper_Speed = Buff;
  
  // Set the speed in steps per second:
  stepper.setSpeed(Stepper_Speed);
  // Step the motor with a constant speed as set by setSpeed():
  stepper.runSpeed();
}
