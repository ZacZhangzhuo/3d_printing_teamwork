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





//! Start Tangent Lines
void getTangentLineCurves(Point3d p0, double r0, Point3d p1, double r1, out NurbsCurve l0, out NurbsCurve l1)
{

    double aa = Math.Atan2((p0.Y - p1.Y), (p0.X - p1.X));    //求中两个圆心连线的斜率角度
    double centerLine;

    centerLine = p0.DistanceTo(p1); //求两个圆心连线长度

    double bb = Math.Acos((r0 + r1) / centerLine);  //求两个圆心连线和圆心到切点垂线的夹角
    double cc = bb - aa;
    double r2LowX = r1 * Math.Cos(cc);
    double r2LowY = r1 * Math.Sin(cc);
    double r1UpX = r0 * Math.Cos(cc);
    double r1UpY = r0 * Math.Sin(cc);
    r2_low_point.X = centerOfCircle2.X - r2LowX;
    r2_low_point.Y = centerOfCircle2.Y + r2LowY;
    r1_up_point.X = centerOfCircle1.X + r1UpX;
    r1_up_point.Y = centerOfCircle1.Y - r1UpY;
    Point3d r2_tempoint = Transition(r2_low_point.X - centerOfCircle2.X, r2_low_point.Y - centerOfCircle2.Y, 2 * bb, 1);
    r2_up_point.X = centerOfCircle2.X + r2_tempoint.X;
    r2_up_point.Y = centerOfCircle2.Y + r2_tempoint.Y;
    Point3d r1_tempoint = Transition(r1_up_point.X - centerOfCircle1.X, r1_up_point.Y - centerOfCircle1.Y, 2 * bb, 1);
    r1_low_point.X = centerOfCircle1.X + r1_tempoint.X;
    r1_low_point.Y = centerOfCircle1.Y + r1_tempoint.Y;
}
//点绕点旋转
Point2d Transition(float _x, float _y, double _angle, int fx)
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
    return new Point2d(  newX, newY);
}

