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
  private void RunScript(List<Point3d> zPoints, bool zReset, double zRadius, Curve zEdge, int zMaxCounts, ref object zOutPoints)
  {

    if (zReset)
    { zInteration = 0; }
    zInteration++;
    List<Circle> circles = new List<Circle>();
    List<Point3d> OutPoint = new List<Point3d>();
    for (int iteration = 0; iteration < zInteration; iteration++)
    {
      List<Vector3d> totalVector = new List<Vector3d>();
      List<double> counts = new List<double>();
      for (int i = 0; i < zPoints.Count; i++)
      {
        totalVector.Add(new Vector3d(0, 0, 0));
        counts.Add(0);
      }
      for (int i = 0; i < zPoints.Count; i++)
        for (int j = i + 1; j < zPoints.Count; j++)
        {
          double distance = zPoints[i].DistanceTo(zPoints[j]);
          if (2 * zRadius < distance) continue;
          else
          {

            Vector3d subVector = zPoints[i] - zPoints[j];
            subVector.Unitize();
            subVector *= 0.5 * (2 * zRadius - distance);
            totalVector[i] += subVector;
            totalVector[j] -= subVector;
            counts[i] += 1;
            counts[j] += 1;

          }
        }
      for (int k = 0; k < zPoints.Count; k++)
        if (counts[k] != 0)
        {
          if (zEdge.Contains(zPoints[k]) == PointContainment.Inside)
          {
            Vector3d move = totalVector[k] / counts[k];
            zPoints[k] += move;
          }

        }
      if (zPoints.Count < zMaxCounts)
      {
        List<int> Indices = new List<int>();

        for (int i = 0; i < zPoints.Count - 1; i++)
        {
          if (zPoints[i].DistanceTo(zPoints[i + 1]) > zRadius)
          { Indices.Add(i + 1 + Indices.Count); }
        }
        foreach (int Index in Indices)
        {
          Point3d addPoint = 0.5 * (zPoints[Index - 1] + zPoints[Index]);
          zPoints.Insert(Index, addPoint);
        }
      }
    }

    foreach (Point3d point in zPoints)
    {
      OutPoint.Add(point);
    }
    zOutPoints = OutPoint;

  }
  #endregion
  #region Additional

  int zInteration = 0;
  #endregion
}