import Rhino.Geometry as rg


tolerance = None
layerHeight = None

planes_of_each_layer = []


def singleSurface( planes_of_each_layer = [], tolerance = None, layerHeight = None):
    move = rg.Transform.Translation(rg.Vector3d(0,0,layerHeight/2))


    for i in range(len(planes_of_each_layer)):
        for j in range(len(planes_of_each_layer) - j):

            if planes_of_each_layer[i].Origin.DistanceTo(planes_of_each_layer[j].Origin) < tolerance:

                middlePoint = (planes_of_each_layer[i].Origin + planes_of_each_layer[j].Origin) / 2

                planes_of_each_layer[i].Transform(rg.Vector3d(middlePoint = planes_of_each_layer[i].Origin))
                planes_of_each_layer[j].Transform(rg.Vector3d(middlePoint = planes_of_each_layer[j].Origin))

                planes_of_each_layer[i].Transform(move)
                planes_of_each_layer[j].Transform(-move)

    return planes_of_each_layer