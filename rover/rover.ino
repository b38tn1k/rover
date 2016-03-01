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
// SharpIR frontIR = SharpIR(frontIrPin, irModel);
// SharpIR rearIR = SharpIR(rearIrPin, irModel);
void setup()
{
  Serial.begin(9600);
  MOTOR.init();
}

void loop()
{
  sensors.readSensors();
  Serial.println(sensors.IR.rear);
  Serial.println(sensors.IR.front);
  delay(100);
//  MOTOR.setSpeedDir(100, DIRF);
}
