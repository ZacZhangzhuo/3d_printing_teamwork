using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;



/// <summary>
/// This class will be instantiated on demand by the Script component.
/// </summary>
public abstract class Script_Instance_9d1f1 : GH_ScriptInstance
{
  #region Utility functions
  /// <summary>Print a String to the [Out] Parameter of the Script component.</summary>
  /// <param name="text">String to print.</param>
  private void Print(string text) { /* Implementation hidden. */ }
  /// <summary>Print a formatted String to the [Out] Parameter of the Script component.</summary>
  /// <param name="format">String format.</param>
  /// <param name="args">Formatting parameters.</param>
  private void Print(string format, params object[] args) { /* Implementation hidden. */ }
  /// <summary>Print useful information about an object instance to the [Out] Parameter of the Script component. </summary>
  /// <param name="obj">Object instance to parse.</param>
  private void Reflect(object obj) { /* Implementation hidden. */ }
  /// <summary>Print the signatures of all the overloads of a specific method to the [Out] Parameter of the Script component. </summary>
  /// <param name="obj">Object instance to parse.</param>
  private void Reflect(object obj, string method_name) { /* Implementation hidden. */ }
  #endregion

  #region Members
  /// <summary>Gets the current Rhino document.</summary>
  private readonly RhinoDoc RhinoDocument;
  /// <summary>Gets the Grasshopper document that owns this script.</summary>
  private readonly GH_Document GrasshopperDocument;
  /// <summary>Gets the Grasshopper script component that owns this script.</summary>
  private readonly IGH_Component Component;
  /// <summary>
  /// Gets the current iteration count. The first call to RunScript() is associated with Iteration==0.
  /// Any subsequent call within the same solution will increment the Iteration count.
  /// </summary>
  private readonly int Iteration;
  #endregion
  /// <summary>
  /// This procedure contains the user code. Input parameters are provided as regular arguments,
  /// Output parameters as ref arguments. You don't have to assign output parameters,
  /// they will have a default value.
  /// </summary>
  #region Runscript
  private void RunScript(List<Point3d> Points, double Iteration, double MaxRadius, double MinRadius, Point3d AttractPoint, Curve Edge, int MaxCount, double FilletRatio, ref object OutPoints, ref object Radiuses, ref object OutTemp)
  {
    // !Initialization
    List<Circle> circles = new List<Circle>();
    List<double> radiuses = new List<double>();


    for (int i = 0; i < Points.Count; i++)
    {
      radiuses.Add(Remap(Points[i].DistanceTo(AttractPoint), 20, 0, MinRadius, MaxRadius));
    }

    //!Iteration
    for (int iteration = 0; iteration < Iteration; iteration++)
    {

      List<Vector3d> totalVector = new List<Vector3d>();
      List<double> counts = new List<double>();
      for (int i = 0; i < Points.Count; i++)
      {
        totalVector.Add(new Vector3d(0, 0, 0));
        counts.Add(0);
      }

      for (int i = 0; i < Points.Count; i++)
        for (int j = i + 1; j < Points.Count; j++)
        {
          double distance = Points[i].DistanceTo(Points[j]);
          if (radiuses[i] + radiuses[j] > distance)
          {

            Vector3d subVector = Points[i] - Points[j];
            subVector.Unitize();
            subVector *= 1 * (radiuses[i] + radiuses[j] - distance);
            // subVector *= 0.5 / distance;
            // subVector *= 
            totalVector[i] += subVector;
            totalVector[j] -= subVector;
            counts[i] += 1;
            counts[j] += 1;

          }


        }


      for (int k = 0; k < Points.Count; k++)
        if (counts[k] != 0)
        {
          if (Edge.Contains(Points[k], Plane.WorldXY, 0.01) == PointContainment.Inside)
          {
            Vector3d move = totalVector[k] / counts[k];
            // Vector3d move = totalVector[k] ;
            Points[k] += move;
          }

        }

      //! Add points
      if (Points.Count < MaxCount)
      {
        List<int> Indices = new List<int>();

        for (int i = 0; i < Points.Count - 1; i++)
        {
          if (Points[i].DistanceTo(Points[i + 1]) > radiuses[i] + radiuses[i + 1])
          { Indices.Add(i + 1 + Indices.Count); }
        }
        foreach (int Index in Indices)
        {
          if (Points.Count < MaxCount)
          {
            Point3d addPoint = 0.5 * (Points[Index - 1] + Points[Index]);
            Points.Insert(Index, addPoint);
          }
        }
      }


      // ! Generate the radius
      radiuses = new List<double>();
      for (int i = 0; i < Points.Count; i++)
      {
        radiuses.Add(Remap(Points[i].DistanceTo(AttractPoint), 20, 0, MinRadius, MaxRadius));
      }

      // Print(totalVector[54].Length.ToString());
    }


    //! Make curve




    //!Info
    Print("Points.Count =" + Points.Count.ToString());
    // ! Output
    // zOutTemp = curves;
    OutPoints = Points;
    Radiuses = radiuses;

  }
  #endregion
  #region Additional


  bool IsLinear(Point3d p0, Point3d p1, Point3d p2)
  {

    Vector3d v1 = new Vector3d(p1 - p0);
    Vector3d v2 = new Vector3d(p2 - p1);
    

    double x = v1.X / v2.X;

    if (v1.Y / v2.Y == x && v1.Z / v2.Z == x) { return true; }
    else return false;
  }
  double Remap(double x, double t1, double t2, double s1, double s2)
  {
    double mapped = (s2 - s1) / (t2 - t1) * (x - t1) + s1;
    if (mapped < s1) mapped = s1;
    if (mapped > s2) mapped = s2;
    return mapped;
    // return (x - t1) / (t2 - t1) * (s2 - s1) + s1;
  }
  #endregion
}