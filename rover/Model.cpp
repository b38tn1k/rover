#include "Arduino.h"
#include "Model.h"
#include "Sensors.h"

Model::Model()
{

}

void Model::updateModel(Sensors sensors, unsigned long delta)
{
  dRoll = sensors.gyro.x * delta / 1000;
  roll += dRoll;
  dPitch = sensors.gyro.y * delta / 1000;
  pitch += dPitch;
  dYaw = sensors.gyro.z * delta / 1000;
  yaw += dYaw;
}

void Model::prettyPrintData()
{
  Serial.println("ROLL");
  Serial.print(roll);
  Serial.println(" deg");
  Serial.println("PITCH");
  Serial.print(pitch);
  Serial.println(" deg");
  Serial.println("YAW");
  Serial.print(yaw);
  Serial.println(" deg");
}
