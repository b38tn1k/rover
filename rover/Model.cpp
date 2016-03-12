#include "Arduino.h"
// my stuff
#include "Model.h"
#include "Sensors.h"
#include "Vector3D.h"

Model::Model()
{

}

void Model::updateModel(Sensors sensors, unsigned long delta)
{
  deltaPose = vec3.multiply(sensors.gyro, delta);
  deltaPose = vec3.multiply(deltaPose, 0.001);
  pose = vec3.add(pose, deltaPose);
}

void Model::prettyPrint()
{
  vec3.prettyPrint(pose, "ROLL/PITCH/YAW", "deg");
}
