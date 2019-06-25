#include <Wire.h>
#define SLAVE_ADDRESS 0x04
byte a;
void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(sendData);
  Serial.println("Ready!");
}
void loop() {
   int RawValue = analogRead(A0);
   a = RawValue;
  delay(100);
}
void sendData() {
  Wire.write(a);
}
