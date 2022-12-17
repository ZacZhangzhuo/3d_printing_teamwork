from compas_rhino.conversions import point_to_compas
from compas import rpc
# from compas_slicer.utilities import save_to_json


if run:
    printPoints = []
    for p in planes_as_list:
        printPoints.append(PrintPoint(point_to_compas(p.Origin), p.Origin.Z, p.ZAxis))

    save_to_json(printPoints, path+'\\'+folder_name,json_name)

# path, folder_name, json_na    



# """
# Serializes COMPAS objects to JSON.
# """
# from ghpythonlib.componentbase import executingcomponent as component

# import compas


# class CompasInfo(component):
#     def RunScript(self, data, filepath, pretty):
#         json = filepath

#         if filepath:
#             compas.json_dump(data, filepath, pretty)
#         else:
#             json = compas.json_dumps(data, pretty)

#         return json
