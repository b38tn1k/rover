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

int frontIrPin = A3;
int rearIrPin = A2;
int irModel = 1080;
Sensors sensor = Sensors(irModel, frontIrPin, rearIrPin);

void setup()
{
  Serial.begin(9600);
  MOTOR.init();
}

void loop()
{
  readSensors();
//  MOTOR.setSpeedDir(100, DIRF);
}

void readSensors() {
  // sensor.IR.front = frontIR.distance();
  // sensor.IR.rear = rearIR.distance();
  // Serial.println(sensor.IR.front);
}
