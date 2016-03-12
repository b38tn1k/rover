#include "Arduino.h"
#include "Sensors.h"
// IMU Libraries
#include <I2Cdev.h>
#include <MPU6050.h>
#include "Wire.h"
// IR Range Finders
#include <SharpIR.h>
// my stuff
#include "Vector3D.h"

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
  // 131 is 1 deg/sec with range +/- 250 deg/sec represented over [-32768, +32767]
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  accel = vec3.double2vec(ax, ay, az);
  gyro = vec3.double2vec(gx, gy, gz);
  if (initflag == false) {
    accel = vec3.subtract(accel, accelBias);
    accel = vec3.multiply(accel, 1.0/16384.0);
    gyro = vec3.subtract(gyro, gyroBias);
    gyro = vec3.multiply(gyro, 1.0/130.0);
  }
}

void Sensors::readIR()
{
  IR.front = frontIR.distance();
  IR.rear = rearIR.distance();
}

void Sensors::prettyPrint()
{
  Serial.println("IR_FRONT_REAR:");
  Serial.print(IR.front);
  Serial.println(" cm");
  Serial.print(IR.rear);
  Serial.println(" cm");
  vec3.prettyPrint(accel, "ACCEL", "g");
  vec3.prettyPrint(gyro, "GYRO", "deg/s");
}

void Sensors::determineMPUBias()
{
  int counter = 0;
  int sampleCount = 500;
  double invSampleCount = 0.002; // 1/500
  Vector3D::Vector invGravity;
  invGravity = vec3.double2vec(0, 0, 16384); // Gravity is -16384 but want to zero everything to find bias
  while (counter < sampleCount) {
    readSensors();
    accel = vec3.add(accel, invGravity);
    accel = vec3.multiply(accel, invSampleCount);
    accelBias = vec3.add(accelBias, accel);
    gyro = vec3.multiply(gyro, invSampleCount);
    gyroBias = vec3.add(gyroBias, gyro);
    counter++;
  }
  vec3.prettyPrint(accelBias, "ACCEL BIAS", "ticks");
  vec3.prettyPrint(gyroBias, "GYRO BIAS", "ticks");
}

void Sensors::init()
{
  Wire.begin();
  mpu.initialize();
  determineMPUBias();
  initflag = false;
}
