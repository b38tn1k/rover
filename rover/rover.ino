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
// My Stuff
#include "Sensors.h"
#include "Model.h"
Sensors sensors = Sensors();
Model model = Model();
unsigned long  loopStart = 0;
unsigned long loopDelta = 10;
void setup()
{
  Serial.begin(38400);
  MOTOR.init();
  sensors.init();
}

void loop()
{
  loopStart = millis();
  // LOOP-COUNTER: NOTHING ABOVE HERE

  sensors.readSensors(); // about 9ms
  // sensors.prettyPrintData();
  model.updateModel(sensors);

  delay(100);
  //  MOTOR.setSpeedDir(100, DIRF);
  // LOOP-COUNTER: NOTHING BELOW HERE
  loopDelta = millis() - loopStart;
  Serial.println("DELTA:");
  Serial.println(loopDelta);
  Serial.println("");
}
