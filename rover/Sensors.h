// James Carthew Feb 2016
// A Simple API for some sensor data in my rover
#ifndef Sensors_h
#define Sensors_h
// IMU Libraries
#include <I2Cdev.h>
#include <MPU6050.h>
#include "Wire.h"
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
      double front;
      double rear;
    } IR;
    struct Vector
    {
      double x;
      double y;
      double z;
    };
    Vector accel;
    Vector gyro;
    Vector compass;
  private:
    // MPU Sensor Bias
    double abx, aby, abz, gbx, gby, gbz;
    boolean initflag = true;
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
    // Data Aquisition Functions
    void readMPU();
    void readIR();
    void determineMPUBias();
};

#endif
