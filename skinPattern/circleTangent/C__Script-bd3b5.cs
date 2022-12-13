using System;
using System.Collections;
using System.Collections.Generic;

using Rhino;
using Rhino.Geometry;

using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;

using Rhino.Geometry.Intersect;


/// <summary>
/// This class will be instantiated on demand by the Script component.
/// </summary>
public abstract class Script_Instance_bd3b5 : GH_ScriptInstance
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
  private void RunScript(List<Point3d> Points, List<double> Radius, ref object OutTemp)
  {


    double maxTangentArcRadius = 10;
    double minTangentArcRadius = 1;
    Random random = new Random();

    //! Start

    List<NurbsCurve> curves = new List<NurbsCurve>();


    for (int i = 0; i < Points.Count - 1; i++)
    {

      NurbsCurve l0 = new NurbsCurve(0, 0);
      NurbsCurve l1 = new NurbsCurve(0, 0);
      getTangentLineCurves(Points[i], Radius[i], Points[i + 1], Radius[i + 1], out l0, out l1);

      if (l0 == null && l1 == null)
      {
        double radius = maxTangentArcRadius * (random.NextDouble() + minTangentArcRadius);
        getTangentArcs(Points[i], Radius[i], Points[i + 1], Radius[i + 1], radius, out l0, out l1);
      }

      curves.Add(l0);
      curves.Add(l1);
      // Print((curves[curves.Count - 1] == null).ToString());
    }



    OutTemp = curves;

  }
  #endregion
  #region Additional
  //! Start Tangent Arcs

  void getTangentArcs(Point3d p0, double r0, Point3d p1, double r1, double Radius, out NurbsCurve l0, out NurbsCurve l1)
  {

    double radius = (p0.DistanceTo(p1) - r0 - r1) / 2;
    if (radius < Radius) { radius = Radius; }

    Circle c0 = new Circle(p0, radius);
    Circle c1 = new Circle(p1, radius);

    Point3d intersectionPoint1 = new Point3d();
    Point3d intersectionPoint2 = new Point3d();



    // Print(x);


    l0 = null;
    l1 = null;


  }

  void CircleCircleIntersection(Circle c1, Circle c2)
  {



  }


  //! Start Tangent Lines
  void getTangentLineCurves(Point3d p0, double r0, Point3d p1, double r1, out NurbsCurve l0, out NurbsCurve l1)
  {
    Point3d r2_low_point = new Point3d(p1);
    Point3d r2_up_point = new Point3d(p1);
    Point3d r1_up_point = new Point3d(p0);
    Point3d r1_low_point = new Point3d(p0);

    double k = Math.Atan2((p0.Y - p1.Y), (p0.X - p1.X));    //求中两个圆心连线的斜率角度
    double centerLine;
    if (p1.Y == p0.Y) //处理斜率为零的情况
    {
      if (p0.X < p1.X)
      {
        centerLine = p0.X - p1.X;

      }
      else
      {
        centerLine = p1.X - p0.X;
      }
    }
    else
    {
      centerLine = (p1.Y - p0.Y) / Math.Sin(k); //求两个圆心连线长度
    }

    double l = Math.Acos((r1 + r1) / centerLine);  //求两个圆心连线和圆心到切点垂线的夹角
    double m = l - k;
    double r2LowX = r1 * Math.Cos(m);
    double r2LowY = r1 * Math.Sin(m);
    double r1UpX = r0 * Math.Cos(m);
    double r1UpY = r0 * Math.Sin(m);
    r2_low_point.X = p1.X - (double)r2LowX;
    r2_low_point.Y = p1.Y + (double)r2LowY;
    r1_up_point.X = p0.X + (double)r1UpX;
    r1_up_point.Y = p0.Y - (double)r1UpY;
    Point2d r2_tempoint = Transition(r2_low_point.X - p1.X, r2_low_point.Y - p1.Y, 2 * l, 1);
    r2_up_point.X = p1.X + r2_tempoint.X;
    r2_up_point.Y = p1.Y + r2_tempoint.Y;
    Point2d r1_tempoint = Transition(r1_up_point.X - p0.X, r1_up_point.Y - p0.Y, 2 * l, 1);
    r1_low_point.X = p0.X + r1_tempoint.X;
    r1_low_point.Y = p0.Y + r1_tempoint.Y;


    l0 = new Line(r1_up_point, r2_low_point).ToNurbsCurve();
    l1 = new Line(r1_low_point, r2_up_point).ToNurbsCurve();


  }
  //点绕点旋转
  private Point2d Transition(double _x, double _y, double _angle, int fx)
  {
    double newX = 0;
    double newY = 0;
    if (fx == 1)
    {
      newX = _x * Math.Cos(_angle) - _y * Math.Sin(_angle);
      newY = _x * Math.Sin(_angle) + _y * Math.Cos(_angle);
    }
    else
    {
      newX = _x * Math.Cos(_angle) + _y * Math.Sin(_angle);
      newY = _y * Math.Cos(_angle) - _x * Math.Sin(_angle);
    }
    return new Point2d((double)newX, (double)newY);
  }
  #endregion
}