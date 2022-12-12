import Rhino
import Rhino.Geometry as rg
import random

tolerance = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

#this class is focused on the properties and methods of each instance MAS (multi agent system)

class System(object):
    
    def __init__(self, num_agents, num_groups):
        self.num_agents = num_agents    #total number of agents
        self.num_groups = num_groups
        self.agents=[]

        if time==0:
    
    def starting_positions(self):
        st_u= 1/ self.num_groups
        st_v=0

        
        # generate the initial position of each agent
        # call the agent class 

    def updated_positions (self):
        # for each second (??) generate the new position of each agent by calculating their new direction and velocity



class Agent(object):

#the main parameters are poisiton on the surface, velocity in both directions 
    def __init__(self, u, v, du, dv):
        self.u = u
        self.v = v

        self.position = rg.Surface.PointAt(self.u, self.v)

        self.du = du
        self.dv = dv
        

    def Coherence(self):
        # fx for Coherence
        """ 
        --- within the specified radius we need to iterate over each agent apart from ours and do the following:
        -> calculate the center (u,v) of the surrounding by 2 getting the average over all of the points 
        -> this shall be the point to aim at from the agent position 
        -> unitize the produced vector 
        """
        coherence_distance = 10
        centerU=self.u
        centerV= self.v
        num_neighbors = 1
        for agent in group_of_agents:
            if not agent == self:
                dist = GivenSurface.ShortPath(self.position, agent.position, tolerance).GetLength()
                if dist<= coherence_distance:
                    num_neighbors +=1
                    centerU += agent.u
                    centerV += agent.v
        
        centerU /= num_neighbors
        centerV /= num_neighbors

        self.du += (centerU-self.u)*coherence_factor
        self.dv += (centerV-self.v)*coherence_factor

    def Alignment(self):
        # fx for Alignment (match velocity)
        """within the specified radius we need to iterate over each agent apart from ours and do the following:
        -> calculate the average velocity [adding all the velocities and dividing the result with the total number of neighbors]
        """
        alignment_distance = 10

        average_du = self.du
        average_dv = self.dv
        num_neighbors = 1

        for neighbor_agent in group_of_agents:
            if not neighbor_agent == self:
                dist = GivenSurface.ShortPath(self.position, neighbor_agent.position, tolerance).GetLength()
                if dist <= alignment_distance:
                    num_neighbors +=1
                    average_du += neighbor_agent.du
                    average_dv += neighbor_agent.dv
        
        average_du /= num_neighbors
        average_dv /= num_neighbors

        self.du += (average_du-self.u)*alignment_factor
        self.dv += (average_du-self.v)*alignment_factor


    def Separation (self):
        # fx for Separation
        """within the specified radius we need to iterate over each agent apart from ours and do the following:
        -> define how close two agents can be [min distance before collision]
        -> define a new direction [maybe reversed]
        """
        seperation_distance = 10


        for neighbor_agent in group_of_agents:
            if not neighbor_agent == self:
                dist = GivenSurface.ShortPath(self.position, neighbor_agent.position, tolerance).GetLength()
                if dist<= seperation_distance:
                    self.du *= -1


    # fx for Target reach
    """
    -> adds an upward vector to the velocity based on a certain criteria 
    """

    def withinBounds (self):
        # fx to keep within Bounds
        """
        ->check if (0<=u,v<=1)
        ->if not mirror u (*-1)
        ->
        """
        if self.u <= 0 or self.u>=1:
            self.du * = -1
            
        if self.v >=1:
            arrived =True




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



