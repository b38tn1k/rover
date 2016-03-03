#include "Arduino.h"
#include "Sensors.h"
// IMU Libraries
#include <I2Cdev.h>
#include <MPU6050.h>
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
// IR Range Finders
#include <SharpIR.h>

Sensors::Sensors()
{
}

void Sensors::readSensors()
{
  readIR();
  readMPU();
}

void Sensors::readMPU()
{
  // 16384 is 1g for MPU6050 with range +/- 2g represented over [-32768, +32767]
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  if (initflag == false) {
    accel.x = (ax - abx);
    accel.y = (ay - aby);
    accel.z = (az - abz);
    // +/- 250 deg/sec represented over [-32768, +32767]
    gyro.x = (gx - gbx);
    gyro.y = (gy - gby);
    gyro.z = (gz - gbz);
  } else {
    accel.x = ax;
    accel.y = ay;
    accel.z = az;
    // +/- 250 deg/sec represented over [-32768, +32767]
    gyro.x = gx;
    gyro.y = gy;
    gyro.z = gz;
  }
}

void Sensors::readIR()
{
  IR.front = frontIR.distance();
  IR.rear = rearIR.distance();
}

void Sensors::prettyPrintData()
{
  Serial.println("IR_FRONT:");
  Serial.println(IR.front);
  Serial.println();
  Serial.println("IR_REAR:");
  Serial.println(IR.rear);
  Serial.println();
  Serial.println("ACCELXYZ:");
  Serial.println(accel.x);
  Serial.println(accel.y);
  Serial.println(accel.z);
  Serial.println();
  Serial.println("GYROXYZ:");
  Serial.println(gyro.x);
  Serial.println(gyro.y);
  Serial.println(gyro.z);
  Serial.println();
}

void Sensors::determineMPUBias()
{
  int counter = 0;
  int sampleCount = 500.0;
  float ax, ay, az, gx, gy, gz = 0.0;
  while (counter < sampleCount) {
    readSensors();
    abx = abx + (accel.x / sampleCount);
    aby = aby + (accel.y / sampleCount);
    abz = abz + ((accel.z + 16384) / sampleCount); //16384 is 1g for MPU6050 with range +/- 2g represented over [-32768, +32767]
    gbx = gbx + (gyro.x / sampleCount);
    gby = gby + (gyro.y / sampleCount);
    gbz = gbz + (gyro.z / sampleCount);
    counter++;
  }

  Serial.println("Accel Bias:");
  Serial.println(abx);
  Serial.println(aby);
  Serial.println(abz);
  Serial.println("Gyro Bias:");
  Serial.println(gbx);
  Serial.println(gby);
  Serial.println(gbz);
  Serial.println();

}

void Sensors::init()
{
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif
  mpu.initialize();
  determineMPUBias();
  
  initflag = false;
}
