import Rhino.Geometry as rg

#this class is focused on the properties and methods of each instance MAS (multi agent system)
class Agent(object):

#the main parameters are poisiton on the surface, velocity in both directions 
    def __init__(self, u, v, du, dv):
        self.u = u
        self.v = v
        self.du = du
        self.dv = dv
        


# fx for Coherence
""" 
--- within the specified radius we need to iterate over each agent apart from ours and do the following:
-> calculate the center (u,v) of the surrounding by 2 getting the average over all of the points 
-> this shall be the point to aim at from the agent position 
-> unitize the produced vector 

"""
# fx for Alignment (match velocity)
"""within the specified radius we need to iterate over each agent apart from ours and do the following:
-> calculate the average velocity [adding all the velocities and dividing the result with the total number of neighbors]
"""

# fx for Separation
"""within the specified radius we need to iterate over each agent apart from ours and do the following:
-> define how close two agents can be [min distance before collision]
-> define a new direction [maybe reversed]
"""

# fx for Target reach
"""
-> adds an upward vector to the velocity based on a certain criteria 
"""
# fx to keep with Bounds
"""
->check if (0<=u,v<=1)
->if not mirror u (*-1)
->


"""

# fx for limiting speed?

# helper fxs:7

# add the effect to the new veloctity vector of the agent that will be added later to its current velocity
# as an input is the vector of a certain effect, the function does the following
# --> unitize the vector
# --> multiply by the effect value 
# --> add this value to sum of new velocity vector 
# --> this fx is called in each effect fx 
    def addSingleEffect(self):
        pass
# adds the new velocty vector to the current vector and unitizes it 
    def addTotalEffect(self):
        pass

#hello Eleniiiii
#hello Ahmed



