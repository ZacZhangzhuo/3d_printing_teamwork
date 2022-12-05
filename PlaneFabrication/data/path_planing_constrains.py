from compas_fab.robots import BoundingVolume
from compas.geometry import Box
from compas.geometry import Frame
from compas_rhino import conversions
from Rhino.Geometry import Plane


A = BoundingVolume(BoundingVolume.VOLUME_TYPES, Box(conversions.plane_to_compas_frame(Plane.WorldXY), 100,100,-100))