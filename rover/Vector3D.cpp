#include "Vector3D.h"
#include "Arduino.h"

Vector3D::Vector3D()
{

}

Vector3D::Vector Vector3D::double2vec(double x, double y, double z)
{
  Vector newVector;
  newVector.x = x;
  newVector.y = y;
  newVector.z = z;
  return newVector;
}

Vector3D::Vector Vector3D::add(Vector3D::Vector a, Vector3D::Vector b)
{
  Vector newVec;
  newVec.x = a.x + b.x;
  newVec.y = a.y + b.y;
  newVec.z = a.z + b.z;
  return newVec;
}

Vector3D::Vector Vector3D::subtract(Vector3D::Vector a, Vector3D::Vector b)
{
  Vector newVec;
  newVec.x = a.x - b.x;
  newVec.y = a.y - b.y;
  newVec.z = a.z - b.z;
  return newVec;
}

Vector3D::Vector Vector3D::multiply(Vector3D::Vector a, double gain)
{
  Vector3D::Vector newVec;
  newVec.x = a.x * gain;
  newVec.y = a.y * gain;
  newVec.z = a.z * gain;
  return newVec;
}

void Vector3D::prettyPrint(Vector a, char title[], char units[])
{
  Serial.println(title);
  Serial.print(a.x);
  Serial.print(" ");
  Serial.println(units);
  Serial.print(a.y);
  Serial.print(" ");
  Serial.println(units);
  Serial.print(a.z);
  Serial.print(" ");
  Serial.println(units);
}
