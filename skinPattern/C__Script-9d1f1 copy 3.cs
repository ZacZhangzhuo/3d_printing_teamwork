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
  private void RunScript(List<Point2d> Points, double Iteration, double MaxRadius, double MinRadius, Point2d AttractPoint, Curve Edge, int MaxCount, double FilletRatio, ref object OutPoints, ref object Radiuses, ref object OutTemp)
  {









  }
  #endregion
  #region Additional


  /// <summary>
  /// 计算两个相离的圆的内公切线。（相交没有内公切线，只有外公切线）
  /// 圆C1, 圆心(a, b), 半径r1.
  /// 圆C2, 圆心(c, d), 半径r2.
  /// </summary>
  /// <returns>返回两条内公切线段，线段的两个端点是圆上的切点。</returns>

  List<Point2d> getTangentPoint(double a, double b, double r1, double c, double d, double r2)
  {

    
    Point2d r2_low_point = new Point2d();
    Point2d r2_up_point = new Point2d();
    Point2d r1_up_point = new Point2d();
    Point2d r1_low_point = new Point2d();


    double k = Math.Atan2((b - d), (a - c));    //求中两个圆心连线的斜率角度
    double centerLine;
    if (d == b)                            //处理斜率为零的情况       
    {
      if (a < c)
      {
        centerLine = a - c;

      }
      else
      {
        centerLine = c - a;
      }
    }
    else
    {
      centerLine = (d - b) / Math.Sin(k); //求两个圆心连线长度
    }
    double l = Math.Acos((r1 + r2) / centerLine);  //求两个圆心连线和圆心到切点垂线的夹角
    double m = l - k;
    double r2LowX = r2 * Math.Cos(m);
    double r2LowY = r2 * Math.Sin(m);
    double r1UpX = r1 * Math.Cos(m);
    double r1UpY = r1 * Math.Sin(m);
    r2_low_point.X = c - (double)r2LowX;
    r2_low_point.Y = d + (double)r2LowY;
    r1_up_point.X = a + (double)r1UpX;
    r1_up_point.Y = b - (double)r1UpY;
    Point2d r2_tempoint = Transition(r2_low_point.X - c, r2_low_point.Y - d, 2 * l, 1);
    r2_up_point.X = c + r2_tempoint.X;
    r2_up_point.Y = d + r2_tempoint.Y;
    Point2d r1_tempoint = Transition(r1_up_point.X - a, r1_up_point.Y - b, 2 * l, 1);
    r1_low_point.X = a + r1_tempoint.X;
    r1_low_point.Y = b + r1_tempoint.Y;


    List<Point2d> outPoints = new List<Point2d>();

    outPoints.Add(r2_low_point);
    outPoints.Add(r2_up_point);
    outPoints.Add(r1_up_point);
    outPoints.Add(r1_low_point);

    return outPoints;
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