import Rhino.Geometry as rg
import copy
import math
# Curves = [rg.Curve()]
# Variables = [10]

def OrientPlane(plane):
    zAxis = plane.ZAxis
    if zAxis.Z < 0: zAxis = -zAxis
    outPlane = rg.Plane(plane.Origin, zAxis)
    xAxis = copy.copy(outPlane.XAxis)
    xAxis.Transform(rg.Transform.ProjectAlong(rg.Plane.WorldXY, outPlane.YAxis))
    outPlane.Transform(rg.Transform.Rotation(outPlane.XAxis, xAxis, outPlane.Origin))
    if outPlane.YAxis.Z <0 : outPlane = rg.Plane(outPlane.Origin, -outPlane.XAxis, -outPlane.YAxis)
    return outPlane


layerHight = 1
divideLength = 20


#Get layer number
sliceNumbers = []
greatestNumber=0
for i,c in enumerate(Curves):
        
    pt0 = c.PointAt(0)
    pt1 = copy.copy(c)
    # scale = rg.Transform.Scale(rg.Point3d.Origin, )
    pt1.Scale(Variables[i])
    pt1 =pt1.PointAt(0)

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

# planes = [planes[0]]

outPlanes = []
for p in planes: 
    
    outPlanes.append( OrientPlane(p))
    print(p.ZAxis.Z)

Planes = outPlanes
