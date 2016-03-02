#include "Arduino.h"
#include "Model.h"
#include "Sensors.h"

Model::Model()
{

}

void Model::updateModel(Sensors sensors)
{
  sensors.prettyPrintData();

}
