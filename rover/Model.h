// James Carthew Feb 2016
#ifndef Model_h
#define Model_h

#include "Sensors.h"

class Model
{
  public:
    Model();
    void updateModel(Sensors sensors, unsigned long delta);
    void prettyPrintData();
    double pitch;
    double dPitch;
    double roll;
    double dRoll;
    double yaw;
    double dYaw;

};

#endif
