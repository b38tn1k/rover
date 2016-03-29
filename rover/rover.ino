/*
Rover.
Software for a Hercules Platform utilising various cheap sensors:
  - Pixy CMU Computer Vision Camera
  - Sharp IR Range Finders * 2
  - Seeed Studios Grove IMU 9DOF
  - onboard hall encoders ignored for now
Rover must be on all 4 wheels on horizontal surface at start up
*/

// Pixy Cam Libraries
#include <SPI.h>
#include <Pixy.h>
// IMU Libraries
#include <Wire.h>
#include <I2Cdev.h>
#include <MPU9250.h>
// IR Range Finders
#include <SharpIR.h>
// Hercules Motor Controller
#include <motordriver_4wd.h>
#include <seeed_pwm.h>
// My Stuff
#include "Vector3D.h"
#include "Sensors.h"
Sensors sensors = Sensors();

char message[127];
char header = '*';
int messageLength = 0;

void parse(char msg[]){
  if (msg[0] == 'r') {
    sensors.readSensors();
    sensors.quickPrint();
  }
}
  
void setup()
{
  Serial.begin(38400);
  delay(100);
//  MOTOR.init();
  sensors.init();
  Serial.println("\nHello, World!");
}

void loop()
{
  if (Serial.available() > 2) {
    // find the start of a message if there is junk
    if (Serial.peek() != '~') {
      Serial.read();
    }
    header= Serial.read();
    messageLength = Serial.read();
    messageLength -= 100;
  }
  // if a header was found and the rest of the message has arrived, read it!
  if (header == '~' && Serial.available() >= messageLength) {
    for(int n=0; n<messageLength; n++) {
      message[n] = Serial.read();
    }
    parse(message);
//    Serial.print("Message Length: ");
//    Serial.println(messageLength);
//    Serial.print("Data ID: ");
//    Serial.println(message[0]);
    header = '*';
    messageLength = 0;
  }
  
      
}
