// James Carthew Feb 2016
#ifndef Sensors_h
#define Sensors_h
// IMU Libraries
#include <I2Cdev.h>
#include <MPU6050.h>
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
    // IR Data
    struct IR_t
    {
      double front;
      double rear;
    } IR;
    Vector3D::Vector accel;
    Vector3D::Vector gyro;
    Vector3D::Vector compass;
  private:
    // MPU Sensor Bias
    double abx, aby, abz, gbx, gby, gbz; // due to gravity only occuring in one direction I think it is easier to treat these guys seperate rather than as a Vector (for now atleast).
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
    Vector3D vec3;
};

#endif
