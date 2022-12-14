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
  private void RunScript(List<Point3d> Points, List<double> Radius, ref object Dir, ref object OutTemp)
  {

    //! Params and declarations
    double maxTangentArcRadius = 2;
    double minTangentArcRadius = 0.3;

    Random random = new Random();
    List<NurbsCurve> curves = new List<NurbsCurve>();
    List<NurbsCurve> tangents = new List<NurbsCurve>();
    NurbsCurve curve = new NurbsCurve(0, 0);
    List<bool> dir = new List<bool>();



    //! Dir
    bool initial = false;//! true: clockwise, false: anti-clockwise
    dir.Add(initial);
    for (int i = 0; i < Points.Count - 1; i++)
    {
      initial = !initial;
      if (Points[i].DistanceTo(Points[i + 1]) < Radius[i] + Radius[i + 1]) { initial = !initial; }
      dir.Add(initial);

    }

    //! Curve
    for (int i = 0; i < Points.Count - 1; i++)
    {

      NurbsCurve l0 = new NurbsCurve(0, 0);
      NurbsCurve l1 = new NurbsCurve(0, 0);

      if (dir[i] != dir[i + 1]) //* Tangent line
      {
        getTangentLineCurves(Points[i], Radius[i], Points[i + 1], Radius[i + 1], out l0, out l1);
        if (dir[i]) tangents.Add(l0);
        else tangents.Add(l1);
      }

      else//* Tangent Arc
      {
        double radius = maxTangentArcRadius * (random.NextDouble() + minTangentArcRadius);
        // Print(radius.ToString());
        // radius = 0.3;
        getTangentArcs(Points[i], Radius[i], Points[i + 1], Radius[i + 1], radius, out l0, out l1);
      }
      if (dir[i]) tangents.Add(l0);
      else tangents.Add(l1);
    }



    //! Circle part

    for (int i = 0; i < tangents.Count - 1; i++)
    {
      curves.Add(tangents[i]);
      curves.Add(new Arc(tangents[i].PointAtEnd, tangents[i].TangentAtEnd, tangents[i + 1].PointAtStart).ToNurbsCurve());
    }
    curves.Add(tangents[tangents.Count - 1]);


    //! Output
    Dir = dir;
    // OutTemp = tangents;
    OutTemp = curves;
    //! End
  }
  #endregion
  #region Additional
  //! Start Tangent Arcs

  void getTangentArcs(Point3d p0, double r0, Point3d p1, double r1, double Radius, out NurbsCurve l0, out NurbsCurve l1)
  {

    double radius = (p0.DistanceTo(p1) - r0 - r1) / 2;
    if (radius < Radius)
    {

      Point3d intersectionPoint0 = new Point3d();
      Point3d intersectionPoint1 = new Point3d();

      CircleCircleIntersection(p0, r0 + Radius, p1, r1 + Radius, out intersectionPoint0, out intersectionPoint1);

      //! intersectionPoint0

      double t0 = r0 / p0.DistanceTo(intersectionPoint0);
      Point3d LCIntersection0 = p0 * (1 - t0) + intersectionPoint0 * t0;

      double t1 = r1 / p1.DistanceTo(intersectionPoint0);
      Point3d LCIntersection1 = p1 * (1 - t1) + intersectionPoint0 * t1;

      Vector3d centerToIntersectionPoint = new Vector3d(p0 - intersectionPoint0);

      Vector3d normal = new Vector3d(1, -centerToIntersectionPoint.X / centerToIntersectionPoint.Y, p0.Z);
      if (normal * new Vector3d(LCIntersection1 - LCIntersection0) < 0) { normal = -normal; }
      l0 = new Arc(LCIntersection0, normal, LCIntersection1).ToNurbsCurve();

      // l0 = new Line(intersectionPoint0, intersectionPoint1).ToNurbsCurve();


      //! IntersectionPoint1
      t0 = r0 / p0.DistanceTo(intersectionPoint1);
      LCIntersection0 = p0 * (1 - t0) + intersectionPoint1 * t0;

      t1 = r1 / p1.DistanceTo(intersectionPoint1);
      LCIntersection1 = p1 * (1 - t1) + intersectionPoint1 * t1;

      centerToIntersectionPoint = new Vector3d(p0 - intersectionPoint1);

      normal = new Vector3d(1, -centerToIntersectionPoint.X / centerToIntersectionPoint.Y, p0.Z);
      if (normal * new Vector3d(LCIntersection1 - LCIntersection0) < 0) { normal = -normal; }
      l1 = new Arc(LCIntersection0, normal, LCIntersection1).ToNurbsCurve();
      // l1 = null;


    }
    else
    {
      radius = Radius;
      Vector3d v = new Vector3d(p1 - p0);
      v.Unitize();

      Point3d pt0 = p0 + v * r0;
      Point3d pt1 = p1 - v * r1;
      Vector3d normal = new Vector3d(1, -v.X / v.Y, v.Z);

      l0 = new Arc(pt0, normal, pt1).ToNurbsCurve();
      l1 = new Arc(pt0, -normal, pt1).ToNurbsCurve();

    }


  }

  void CircleCircleIntersection(Point3d p0, double r0, Point3d p1, double r1, out Point3d intersection0, out Point3d intersection1)
  {

    double d = p0.DistanceTo(p1);//AB
    // if (d == r0 + r1)
    // {
    //   Print("wow".ToString());
    //   Print(r0.ToString());
    //   Print(r1.ToString());
    //   Print(d.ToString());
    // }

    // Print((d == r0 + r1).ToString());

    double cosA = (r1 * r1 + d * d - r0 * r0) / (2 * r1 * d);
    double d1 = r1 * cosA;
    double t1 = d1 / d;
    Point3d midPt = p0 * t1 + p1 * (1 - t1);


    double h = Math.Sqrt(Math.Pow(r1, 2) - Math.Pow(d1, 2)); //CE
    // Print(h.ToString());
    Vector3d normal = new Vector3d(p0 - p1);
    normal.Transform(Transform.Rotation(Math.PI * 0.5, Vector3d.ZAxis, p0));
    normal.Unitize();
    normal *= h;

    intersection0 = midPt - normal; //!Clockwise one
    intersection1 = midPt + normal;//!Anti-clockwise one

    // intersection0 = midPt ;
    // intersection1 = midPt +Vector3d.YAxis;


  }


  //! Start Tangent Lines
  void getTangentLineCurves(Point3d p0, double r0, Point3d p1, double r1, out NurbsCurve l0, out NurbsCurve l1)
  {
    Point3d r1_low_point = new Point3d();
    Point3d r0_up_point = new Point3d();
    Point3d r0_low_point = new Point3d();
    Point3d r1_up_point = new Point3d();

    double aa = Math.Atan2((p1.Y - p0.Y), (p1.X - p0.X));  //求中两个圆心连线的斜率角度
    double centerLine;

    centerLine = p0.DistanceTo(p1); //求两个圆心连线长度

    double bb = Math.Acos((r0 + r1) / centerLine);  //求两个圆心连线和圆心到切点垂线的夹角
    double cc = bb - aa;
    double r2LowX = r1 * Math.Cos(cc);
    double r2LowY = r1 * Math.Sin(cc);
    double r1UpX = r0 * Math.Cos(cc);
    double r1UpY = r0 * Math.Sin(cc);
    r1_low_point.X = p1.X - r2LowX;
    r1_low_point.Y = p1.Y + r2LowY;
    r0_up_point.X = p0.X + r1UpX;
    r0_up_point.Y = p0.Y - r1UpY;
    Point3d r2_tempoint = Transition(r1_low_point.X - p1.X, r1_low_point.Y - p1.Y, 2 * bb, 1);
    r1_up_point.X = p1.X + r2_tempoint.X;
    r1_up_point.Y = p1.Y + r2_tempoint.Y;
    Point3d r1_tempoint = Transition(r0_up_point.X - p0.X, r0_up_point.Y - p0.Y, 2 * bb, 1);
    r0_low_point.X = p0.X + r1_tempoint.X;
    r0_low_point.Y = p0.Y + r1_tempoint.Y;


    l0 = new Line(r0_low_point, r1_up_point).ToNurbsCurve(); //!Clockwise one
    l1 = new Line(r0_up_point, r1_low_point).ToNurbsCurve();//!Anti-clockwise one


  }
  //点绕点旋转
  Point3d Transition(double _x, double _y, double _angle, int fx)
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
    return new Point3d(newX, newY, 0);
  }





  #endregion
}