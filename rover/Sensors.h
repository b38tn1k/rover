// James Carthew Feb 2016
// A Simple API for some sensor data in my rover
#ifndef Sensors_h
#define Sensors_h
// IMU Libraries
#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
// IR Range Finders
#include <SharpIR.h>

class Sensors
{
public:
        Sensors(int irSensorModel, int frontIrPin, int rearIrPin);
        void readSensors();
        // IR Data
        struct IR_t
        {
                volatile int front;
                volatile int rear;
        } IR;
        // Acceleronmeter Data
        struct accel_t
        {
                volatile int x;
                volatile int y;
                volatile int z;
        } accel;
        // Gyro Data
        struct gyro_t
        {
                volatile int x;
                volatile int y;
                volatile int z;
        } gyro;
        // Compass Data
        struct compass_t
        {
                volatile int x;
                volatile int y;
                volatile int z;
        } compass;
private:
        // http://stackoverflow.com/questions/22117310/c-global-variable-initialization-order
        int frontIrPin, rearIrPin, irSensorModel;
        SharpIR frontIR = SharpIR(frontIrPin, irSensorModel);
        SharpIR rearIR = SharpIR(rearIrPin, irSensorModel);
        void readCompass();
        void readAccel();
        void readGyro();
        void readIR();
};

#endif
