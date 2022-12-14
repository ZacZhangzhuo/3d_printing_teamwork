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
  private void RunScript(List<Point3d> zPoints, double zIteration, bool zReset, double zRadius, Curve zEdge, int zMaxCounts, double FilletRatio, ref object zOutPoints, ref object zOutTemp)
  {

    List<Circle> circles = new List<Circle>();

    for (int iteration = 0; iteration < zIteration; iteration++)
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
          if (zEdge.Contains(zPoints[k], Plane.WorldXY, 0.01) == PointContainment.Inside)
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


    //! ArcCurve
    //Curve Section
    FilletRatio = FilletRatio / 2;
    List<NurbsCurve> curves = new List<NurbsCurve>();
    for (int i = 1; i < zPoints.Count - 1; i++)
    {

      Point3d p0 = zPoints[i - 1];
      Point3d p1 = zPoints[i];
      Point3d p2 = zPoints[i + 1];

      Point3d t0 = new Point3d(FilletRatio * p0 + p1 * (1 - FilletRatio));
      Point3d t1 = new Point3d(FilletRatio * p2 + p1 * (1 - FilletRatio));

      NurbsCurve arcCurve = new Arc(t0, new Vector3d(p1 - t0), t1).ToNurbsCurve();

      if (arcCurve == null) { arcCurve = new PolylineCurve(new List<Point3d> { t0, p1, t1 }).ToNurbsCurve(); }
      curves.Add(arcCurve);

    }
    // Line Section
    for (int i = 1; i < curves.Count; i++)
    {
      if (! curves[i].PointAtStart.Equals(curves[i - 1].PointAtEnd)) { curves.Insert(i, new Line(curves[i - 1].PointAtEnd, curves[i].PointAtStart).ToNurbsCurve()); }
    }





    //! Output
    zOutTemp = curves;
    zOutPoints = zPoints;
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
  #endregion
}