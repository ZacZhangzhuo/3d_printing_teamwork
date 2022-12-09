
import Rhino.Geometry as rg
import scriptcontext as rs

if Reset: Iteration = rs.sticky["Iteration"] = 0

Iteration = Iteration+1

circles = []
OutPoints = []

for i in range(Iteration):

    totalVec = [rg.Vector3d(0,0,0)]*len(Points)
    counts = [0]*len(Points)

    for i in range(len(Points)):
        for j in range(i,len(Points)):
            distance = Points[i].DistanceTo(Points[j])
            if ( 2*Radius>distance):
                
                subVec = Points[i] - Points[j]
                subVec.Unitize()
                subVec *= 0.5*((2*Radius)-distance)
                totalVec[i] += subVec
                totalVec[j] -= subVec
                counts[i] +=1
                counts[j] +=1


    #! Bounding
    for k in range(len(Points)):
        if counts[k] != 0 and Edge.Contains(Points[k]) == rg.PointContainment.Inside:
            move = totalVec[k] / counts[k]
            Points[k] += move

        if (Points.Count<MaxCounts):
            indices = []

            for i in range(Points.Count-1):
                if Points[i].DistanceTo(Points[i + 1]) > Radius:
                    indices.append(i+1+len(indices))

            for j in indices:
                addPoint = 0.5* (Points[j-1]+Points[j])
                Points.Insert(j, addPoint)



OutPoints = Points



