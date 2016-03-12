// James Carthew Feb 2016
#ifndef Vector3D_h
#define Vector3D_h

class Vector3D
{
  public:
    Vector3D();
    struct Vector
    {
      double x;
      double y;
      double z;
    };
    Vector double2vec(double x, double y, double z);
    Vector add(Vector a, Vector b);
    Vector subtract(Vector a, Vector b);
    Vector multiply(Vector a, double gain);
    void prettyPrint(Vector a, char title[], char units[]);
};

#endif
