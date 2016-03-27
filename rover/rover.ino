/*
Rover.
Software for a Hercules Platform utilising various cheap sensors:
  - Pixy CMU Computer Vision Camera
  - Sharp IR Range Finders * 2
  - Seeed Studios Grove IMU 9DOF
  - onboard hall encoders ignored for now
Rover must be on all 4 wheels on horizontal surface at start up
*/

#define MESSAGE_LENGTH 7

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
char message[MESSAGE_LENGTH];
bool newMessage = false;

void act(char data[])
{
  // Check the data is formatted properly
  if (data[0] == '>') {
    if (data[1] == 'r') {
      sensors.readSensors();
      sensors.quickPrint();
    } else if (data[1] == 'c') {
      Serial.println("Control");
    }
  // If data is not formatted properly fix it for the future by locating header in serial queue
  } else {
    for (int i=0; i<MESSAGE_LENGTH;i++){
      if (data[i] == '>') {
        for (int j=i; j<MESSAGE_LENGTH;j++){
          Serial.read(); // read junk of badly formatted message
        }
      }
    }
  }
}
  
void setup()
{
  Serial.begin(38400);
  delay(100);
  Serial.println("\nHello, World!");
  Serial.println(MESSAGE_LENGTH);
//  MOTOR.init();
  sensors.init();
  
}

void loop()
{
  
  if (Serial.available() >= MESSAGE_LENGTH) {
    newMessage = true;
  }
  if (newMessage) {
    for(int n=0; n<MESSAGE_LENGTH; n++) {
      message[n] = Serial.read();
    }
    act(message);
    newMessage = false;
  }
}
