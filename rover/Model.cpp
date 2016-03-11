#include "Arduino.h"
#include "Model.h"
#include "Sensors.h"

Model::Model()
{

}

void Model::updateModel(Sensors sensors, unsigned long delta)
{
  deltaHeading = sensors.gyro.z * delta / 1000;
  heading += deltaHeading;
}

void Model::prettyPrintData()
{
  Serial.println("HEADING");
  Serial.print(heading);
  Serial.println(" deg");
}
