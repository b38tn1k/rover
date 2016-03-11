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
    signed long heading; // about z axes (assuming normal operation)
    signed long deltaHeading;
    signed long velocity;
    signed long pitch;
    signed long roll;
    signed long yaw;
};

#endif
