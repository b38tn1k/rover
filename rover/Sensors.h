// James Carthew Feb 2016
// A Simple API for some sensor data in my rover
#ifndef Sensors_h
#define Sensors_h
// IMU Libraries
#include <I2Cdev.h>
#include <MPU6050.h>
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
// IR Range Finders
#include <SharpIR.h>

class Sensors
{
  public:
    Sensors();
    void init();
    void readSensors();
    void prettyPrintData();
    // IR Data
    struct IR_t
    {
      float front;
      float rear;
    } IR;
    // Acceleronmeter Data
    struct accel_t
    {
      float x;
      float y;
      float z;
    } accel;
    // Gyro Data
    struct gyro_t
    {
      float x;
      float y;
      float z;
    } gyro;
    // Compass Data
    struct compass_t
    {
      float x;
      float y;
      float z;
    } compass;
  private:
    // MPU Sensor Bias
    float abx, aby, abz, gbx, gby, gbz;
    // IR Setup
    int frontIrPin = A3;
    int rearIrPin = A2;
    int irModel = 1080;
    SharpIR frontIR = SharpIR(frontIrPin, irModel);
    SharpIR rearIR = SharpIR(rearIrPin, irModel);
    // IMU Setup
    MPU6050 mpu;
    I2Cdev I2C_M;
    int16_t ax, ay, az;
    int16_t gx, gy, gz;
    int16_t mx, my, mz;
    // Data Aquisition Functions
    void readMPU();
    void readIR();
    void determineMPUBias();
};

#endif
