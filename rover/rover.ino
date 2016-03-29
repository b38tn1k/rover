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
bool incomming = false;

void parse(char msg[]) {
  if (msg[0] == 'r') {
//    sensors.readSensors();
//    sensors.quickPrint();
  }
}

void logMessage(char msg[], int msgLength) {
  Serial.print("Message Length: ");
  Serial.println(msgLength);
  Serial.print("Data ID: ");
  Serial.println(msg[0]);
  for (int i = 1; i < msgLength; i++) {
    Serial.print("Data ");
    Serial.print(i);
    Serial.print(':');
    Serial.println(msg[i]);
  }
}

void setup()
{
  Serial.begin(38400);
  //  MOTOR.init();
  //  sensors.init();
  Serial.println("\nHello, World!");
}

void loop()
{
  // Is there a new message?
  if (Serial.available() > 2 && Serial.peek() == '~') {
    header = Serial.read();
    messageLength = Serial.read();
    incomming = true;
  }
  // Read the new message!
  if (Serial.available() >= messageLength && incomming) {
    for (int n = 0; n < messageLength; n++) {
      message[n] = Serial.read();
    }
    logMessage(message, messageLength);
    incomming = false;
  }
}
