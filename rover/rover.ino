/*
Rover.
Software for a Hercules Platform utilising various cheap sensors:
  - Pixy CMU Computer Vision Camera
  - Sharp IR Range Finders * 2
  - Seeed Studios Grove IMU 9DOF
  - onboard hall encoders ignored for now
*/

// Pixy Cam Libraries
#include <SPI.h>
#include <Pixy.h>
// IMU Libraries
#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
// IR Range Finders
#include <SharpIR.h>
// Hercules Motor Controller
#include <motordriver_4wd.h>
#include <seeed_pwm.h>
// Sensor Data Handler Class
#include "Sensors.h"

Sensors sensors = Sensors();
void setup()
{
  Serial.begin(38400);
  MOTOR.init();
  sensors.init();
}

void loop()
{
  sensors.readSensors();
  sensors.prettyPrintData();
  delay(2000);
  Serial.println("");
  //  MOTOR.setSpeedDir(100, DIRF);
}
