#include "Arduino.h"
#include "Sensors.h"
// IMU Libraries
#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
// IR Range Finders
#include <SharpIR.h>

Sensors::Sensors(int model, int front, int rear) : irSensorModel(model),  frontIrPin(front), rearIrPin(rear)
{

}

void Sensors::readSensors()
{
        readCompass();
        readAccel();
        readGyro();
        readIR();

}

void Sensors::readCompass()
{

}

void Sensors::readAccel()
{

}

void Sensors::readGyro()
{

}

void Sensors::readIR()
{


}
