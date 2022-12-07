import Rhino.Geometry as rg
import copy
import math

def OrientPlane(plane):
    zAxis = plane.ZAxis
    if zAxis.Z < 0:
        zAxis = -zAxis
    outPlane = rg.Plane(plane.Origin, zAxis)
    xAxis = copy.copy(outPlane.XAxis)
    xAxis.Transform(rg.Transform.ProjectAlong(rg.Plane.WorldXY, outPlane.YAxis))
    outPlane.Transform(rg.Transform.Rotation(outPlane.XAxis, xAxis, outPlane.Origin))
    if outPlane.YAxis.Z < 0:
        outPlane = rg.Plane(outPlane.Origin, -outPlane.XAxis, -outPlane.YAxis)
    return outPlane


planes = []
for i in range(LayerNumber):
    for c in Curves:
        params = c.DivideByCount(DivideCount, True)
        for k,p in enumerate(params):
                pt0 = c.PointAt(p)
                pt1 = Brep.ClosestPoint(pt0)
                temp = rg.Plane(pt1, rg.Vector3d(pt1-pt0))
                plane = OrientPlane(temp)
                dir = rg.Vector3d(pt0-pt1)
                dir.Unitize()

                move = rg.Transform.Translation( dir*LayerHight*i)

                plane.Transform(move)

                halfLength = len(params)/2
                rotation2 = rg.Transform.Rotation((((halfLength - abs(halfLength-k))/halfLength)*-math.pi), plane.Normal, plane.Origin)
                plane.Transform(rotation2)

                planes.append(plane)


for p in planes:
    z = p.ZAxis
    z.Unitize()
    newZ = z*Inclination + rg.Vector3d.ZAxis*(1-Inclination)
    rotation = rg.Transform.Rotation(z, newZ,p.Origin)
    p.Transform(rotation)





Planes = planes
