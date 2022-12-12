import Rhino.Geometry as rg
from compas_rhino.conversions import plane_to_compas
from compas_rhino.conversions import  plane_to_rhino


# Test planes
plane = [rg.Plane(1,1,1,1)]


plane = plane_to_rhino(plane_to_compas(plane))