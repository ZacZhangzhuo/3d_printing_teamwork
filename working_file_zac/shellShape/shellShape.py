import Rhino.Geometry as rg
import copy
import math

# Curves = [rg.Curve()]
# Variables = [10]


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


layerHight = 1
divideLength = 10

avas = []
# Get layer number
sliceNumbers = []
greatestNumber = 0
for i, c in enumerate(Curves):

    params = c.DivideByLength(divideLength, True, False)
    ava = [0, 0, 0]
    for p in params:
        pt = c.PointAt(p)
        ava[0] = ava[0] + pt.X
        ava[1] = ava[1] + pt.Y
        ava[2] = ava[2] + pt.Z
    ava[0] = ava[0] / len(params)
    ava[1] = ava[1] / len(params)
    ava[2] = ava[2] / len(params)
    avas.append(ava)
    pt1 = c.PointAt(0)
    pt0 = copy.copy(pt1)
    scale = rg.Transform.Scale(rg.Point3d(ava[0],ava[1],ava[2]), Variables[i])
    pt1.Transform(scale)
    layerNumber = math.ceil(pt0.DistanceTo(pt1) / layerHight)
    sliceNumbers.append(layerNumber)

    if layerNumber > greatestNumber:
        greatestNumber = layerNumber


planes = []
for i in range(int(greatestNumber)):
    for j in range(len(Curves)):
        if sliceNumbers[j] > i:
            params = Curves[j].DivideByLength(divideLength, False, False)

            for k,p in enumerate(params):
                pt = Curves[j].PointAt(p)
                factor = rg.Vector3d(pt-rg.Point3d(avas[j][0],avas[j][1],avas[j][2]))
                b, plane = rg.Curve.FrameAt(Curves[j], p)
                factor.Unitize()
                factor *= layerHight * i

                move = rg.Transform.Translation(factor)
                plane.Transform(move)
                x = OrientPlane(plane)
                plane = copy.copy(x)
                rotation = rg.Transform.Rotation((k*math.pi*2)/len(params), plane.Normal, plane.Origin)
                plane.Transform(rotation)


                # testPlane = rg.Plane(plane.Origin, rg.Vector3d.XAxis, rg.Vector3d.YAxis)
                planes.append(plane)

# planes = [planes[0]]

Planes = planes
