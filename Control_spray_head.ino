int ledPin = 9;      // LED connected to digital pin 9



void setup() {
  pinMode(ledPin, OUTPUT);  // sets the pin as output
}

void loop() {
 
  analogWrite(ledPin, 100); // analogRead values go from 0 to 1023, analogWrite values from 0 to 255
}
