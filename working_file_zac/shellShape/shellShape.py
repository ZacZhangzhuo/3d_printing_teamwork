import Rhino.Geometry as rg
import copy
import math
# Curves = [rg.Curve()]
# Variables = [10]


def OrientPlane(plane):
    xAxis = copy.copy(plane.XAxis)
    xAxis.Transform(rg.Transform.ProjectAlong(rg.Plane.WorldXY, plane.YAxis))
    plane.Transform(rg.Transform.Rotation(plane.XAxis, xAxis, plane.Origin))
    if plane.YAxis.Z < 0:
        plane = rg.Plane(plane.Origin, -plane.XAxis, -plane.YAxis)
    return plane

layerHight = 1
divideLength = 5

#Get layer number
sliceNumbers = []
greatestNumber=0
for i,c in enumerate(Curves):
    pt1 = c.PointAt(0)
    pt0 = copy.copy(pt1)
    scale = rg.Transform.Scale(rg.Point3d.Origin, Variables[i])
    pt1.Transform(scale)
    layerNumber = math.ceil(pt0.DistanceTo(pt1)/layerHight)
    sliceNumbers.append(layerNumber)

    if layerNumber > greatestNumber:
        greatestNumber = layerNumber

## points
planes = []
for i in range(int(greatestNumber)):
    for j in range(len(Curves)):
        if sliceNumbers[j]>i:
            params = Curves[j].DivideByLength(divideLength, True, False)

            for p in params: 
                pt = Curves[j].PointAt(p)
                factor = rg.Vector3d(pt)
                b, plane = rg.Curve.FrameAt(Curves[j], p)
                factor.Unitize()
                factor *= layerHight * i

                move = rg.Transform.Translation(factor)
                plane.Transform(move)
                planes.append(plane)


for p in planes: 
    p = OrientPlane(p)

outTemp = planes
