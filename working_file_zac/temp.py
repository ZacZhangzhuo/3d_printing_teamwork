
import math
import mola
from mola import module_rhino
from ghpythonlib import treehelpers
import csv

with open(r'C:\Users\zac\Desktop\positions.csv')as f:
    tValues = list(csv.reader(f))

Values = tValues


dim = int(math.floor(len(Values) ** (1 / 3) + 0.0001))
# ! Too tree
facesArray = []
lineArray = []
for i in range(dim):
    facesArray.append(Values[dim*dim * i : dim*dim * (i + 1)])

for face in facesArray:
    tempArray = []
    for i in range(dim):
        tempArray.append(face[dim * i : dim * (i + 1)])
    lineArray.append(tempArray)
# ! End to tree

for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            lineArray[0][j][k]=0
            lineArray[-1][j][k] =0
            lineArray[i][0][k]=0
            lineArray[i][-1][k] =0
            lineArray[i][j][0]=0
            lineArray[i][j][-1] =0


# ! Too list
values = []
for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            values.append(lineArray[i][j][k] )
# x = treehelpers.list_to_tree(lineArray)

# print (len(values))
cubes = mola.mesh_marching_cubes(dim, dim, dim, values, 0.5)
cubes.update_topology()
mola.color_faces_by_vertical_angle(cubes.faces)

outTemp = module_rhino.display_mesh(cubes)