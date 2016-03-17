// James Carthew Feb 2016
#ifndef Model_h
#define Model_h

#include "Sensors.h"
#include "Vector3D.h"


class Model
{
  public:
    Model();
    void updateModel(Sensors sensors, unsigned long delta);
    void prettyPrint();
    void quickPrint();
    Vector3D::Vector deltaPose;
    Vector3D::Vector pose;
  private:
    Vector3D vec3;
};

#endif
