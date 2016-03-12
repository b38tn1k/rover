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

  if (initflag == false) {
    accel.x = (ax - abx)/16384.0;
    accel.y = (ay - aby)/16384.0;
    accel.z = (az - abz)/16384.0;
    gyro.x = (gx - gbx)/130.0;
    gyro.y = (gy - gby)/130.0;
    gyro.z = (gz - gbz)/130.0;
  } else {
    accel.x = ax;
    accel.y = ay;
    accel.z = az;
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

void Sensors::prettyPrint()
{
  Serial.println("IR_FRONT_REAR:");
  Serial.print(IR.front);
  Serial.println(" cm");
  Serial.print(IR.rear);
  Serial.println(" cm");
  Serial.println();

  vec3.prettyPrint(accel, "ACCEL", "g");
  vec3.prettyPrint(gyro, "GYRO", "deg/s");
}

void Sensors::determineMPUBias()
{
  int counter = 0;
  int sampleCount = 500.0;
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
  Wire.begin();
  mpu.initialize();
  determineMPUBias();

  initflag = false;
}
