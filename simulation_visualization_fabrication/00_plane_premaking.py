from compas.geometry import Frame
planes = """
O(1.00,0.00,0.00) Z(0.00,0.00,1.00)
O(0.81,0.59,0.00) Z(0.00,0.00,1.00)
O(0.31,0.95,0.00) Z(0.00,0.00,1.00)
O(-0.31,0.95,0.00) Z(0.00,0.00,1.00)
O(-0.81,0.59,0.00) Z(0.00,0.00,1.00)
O(-1.00,0.00,0.00) Z(0.00,0.00,1.00)
O(-0.81,-0.59,0.00) Z(0.00,0.00,1.00)
O(-0.31,-0.95,0.00) Z(0.00,0.00,1.00)
O(0.31,-0.95,0.00) Z(0.00,0.00,1.00)
O(0.81,-0.59,0.00) Z(0.00,0.00,1.00)

"""
planes= planes.replace(" ","").replace("\n","")
planes = planes.replace(")Z(", ",")
# planes = planes.split("O(")

print(planes)

locations = []
for p in planes:  
    if len(p)>1:
        locations.append(Frame())
        



# for plane in planes:

# with open(r'simulation_visualization_fabrication\data\out_printpoints_planes.json', "w") as f:
#     data = json.load(f)
