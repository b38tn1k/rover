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
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  accel.x = ax / 1.72; // gives mm/s^2 
  accel.y = ay / 1.72;
  accel.z = az / 1.72;
  gyro.x = gx;
  gyro.y = gy;
  gyro.z = gz;
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
  Serial.println("IR_REAR:");
  Serial.println(IR.rear);
  Serial.println("ACCELXYZ:");
  Serial.println(accel.x);
  Serial.println(accel.y);
  Serial.println(accel.z);
  Serial.println("GYROXYZ:");
  Serial.println(gyro.x);
  Serial.println(gyro.y);
  Serial.println(gyro.z);
}

void Sensors::init()
{
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
       Wire.begin();
   #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
       Fastwire::setup(400, true);
   #endif

   // initialize serial communication
   // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
   // it's really up to you depending on your project)

   // initialize device
   Serial.println("Initializing I2C devices...");
   mpu.initialize();

   // verify connection
   Serial.println("Testing device connections...");
   Serial.println(mpu.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

}
