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
#include "Model.h"
Sensors sensors = Sensors();
Model model = Model();
unsigned long  loopStart = 0;
unsigned long loopDelta = 10;
long loopCounter = 0;
void setup()
{
  Serial.begin(38400);
  delay(100);
  Serial.println("\nHello, World!");
  MOTOR.init();
  sensors.init();
}

void loop()
{
  sensors.readSensors(); // about 9ms
  sensors.prettyPrint();
  model.updateModel(sensors, loopDelta);
  model.prettyPrint();

  // LOOP-COUNTER: NOTHING BELOW HERE
  loopDelta = millis() - loopStart;
  loopStart = millis();
  loopCounter++;
}
