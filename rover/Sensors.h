// James Carthew Feb 2016
#ifndef Sensors_h
#define Sensors_h
// IMU Libraries
#include <I2Cdev.h>
#include <MPU9250.h>
#include "Wire.h"
// IR Range Finders
#include <SharpIR.h>
// my stuff
#include "Vector3D.h"

class Sensors
{
  public:
    Sensors();
    void init();
    void readSensors();
    void prettyPrint();
    void quickPrint();
    // IR Data
    struct IR_t
    {
      double front;
      double rear;
    };
    IR_t ir;
    Vector3D::Vector accel;
    Vector3D::Vector gyro;
    Vector3D::Vector compass;
  private:
    // MPU Sensor Bias
    Vector3D::Vector gyroBias;
    Vector3D::Vector accelBias;
    boolean initflag = true;
    // IR Setup
    int frontIrPin = A3;
    int rearIrPin = A2;
    int irModel = 1080;
    SharpIR frontIR = SharpIR(frontIrPin, irModel);
    SharpIR rearIR = SharpIR(rearIrPin, irModel);
    // IMU Setup
    MPU9250 mpu;
    int16_t ax, ay, az;
    int16_t gx, gy, gz;
    int16_t mx, my, mz;
    uint8_t buffer_m[6];
    // Data Aquisition Functions
    void readMPU();
    void readIR();
    void determineMPUBias();
    // Maths
    Vector3D vec3;
};

#endif
