import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th


tolerance = 0.001


#this class is focused on the properties and methods of each instance MAS (multi agent system)

class Environment(object):
    
    def __init__(self, u_div, v_div, surface, agents_list = []):
        #self.num_agents = 0    #total number of agents
        self.u_div = u_div
        self.v_div = v_div
        self.surface = surface
        self.agents = []
        if len(agents_list) > 0:
            self.agents = agents_list

    #this function takes the u values and transform them into agents
    def populate_agents(self, u_vals, target_factors):
        # instantiatie all agents
        for u, t_fac in zip(u_vals,target_factors) :
            self.agents.append(Agent(u, 0, 0, t_fac / self.v_div, self.surface)) 

    def update_agents_pos (self, coherence_rad, coherence_fac, align_rad, align_fac, avoid_rad, avoid_fac):
        # generate the new position of each agent by calculating their new direction and velocity
        #for each agent apply all the functions on it given the required factors for each parameter
        #if the agent arrives we pop out this agent from the list and add it to the finished list 
        # add a function that if everything is arrived just stop 
        #list of all effects so as not to change the behaviour of the agents during update
        effects_list = []
        for agent in self.agents:
            effects_vector = rg.Vector2d(0,0)  

            coherence_vector = agent.Coherence(coherence_rad, self.agents, self.u_div, self.v_div, coherence_fac)
            effects_vector += coherence_vector

            alignment_vector = agent.Alignment(align_rad, self.agents, self.u_div, self.v_div, align_fac)
            effects_vector += alignment_vector

            separation_vector = agent.Separation(avoid_rad, self.agents, self.u_div, self.v_div, avoid_fac)
            effects_vector += separation_vector

            #sum all of the vectors + the actual du and dv of the agent + unitize --> do nothing but add them to the effects_list
            agent.AddTotalEffect(self.u_div, self.v_div, effects_vector)

        for agent, effect in zip(self.agents, effects_list):
            agent.AgentStep(effect)

    #function that ensures the agent has reached the final destination

class Agent(object):

#the main parameters are poisiton on the surface, velocity in both directions 
    def __init__(self, u, v, du, dv, surface):
        self.u = u
        self.v = v
        self.surface = surface
        pos_3d = self.surface.PointAt(self.u, self.v)
        self.position = rg.Point2d(pos_3d.X, pos_3d.Y) ##for the surface

        self.du = du
        self.dv = dv
        self.pts = []
        self.pts.append(self.surface.PointAt(self.u, self.v))
        self.arrived = False
        

    def Coherence(self, radius, agents, u_div, v_div, coh_fac):
        # agents : list of agents in the environment
        # fx for Coherence
        """ 
        --- within the specified radius we need to iterate over each agent apart from ours and do the following:
        -> calculate the center (u,v) of the surrounding by 2 getting the average over all of the points 
        -> this shall be the point to aim at from the agent position 
        -> unitize the produced vector 
        """
        #coherence_distance = ra
        centerU= 0
        centerV= 0
        num_neighbors = 0
        for agent in agents:
            if not agent == self:
                dist = self.position.DistanceTo(agent.position)
                if dist<= radius:
                    num_neighbors +=1
                    centerU += agent.u
                    centerV += agent.v

        #get the average vector
        if  num_neighbors > 0:
            centerU /= num_neighbors
            centerV /= num_neighbors

            #unitize the product vector of the coherence  
            cohesion_unit_vect = rg.Vector2d(centerU-self.u, centerV-self.v)
            cohesion_unit_vect = self.UnitizeEffect(u_div, v_div,cohesion_unit_vect) * coh_fac

            return cohesion_unit_vect

        else:
            return rg.Vector2d(0,0)

    def Alignment(self, radius, agents, u_div, v_div, align_fac):
        # fx for Alignment (match velocity)
        """within the specified radius we need to iterate over each agent apart from ours and do the following:
        -> calculate the average velocity [adding all the velocities and dividing the result with the total number of neighbors]
        """
        #radius = 10

        average_du = 0
        average_dv = 0
        num_neighbors = 0

        for agent in agents:
            if not agent == self:
                dist = self.position.DistanceTo(agent.position)
                if dist <= radius:
                    num_neighbors +=1
                    average_du += agent.du
                    average_dv += agent.dv
        
        if  num_neighbors > 0:
            average_du /= num_neighbors
            average_dv /= num_neighbors

            align_unit_vect = rg.Vector2d(average_du, average_dv)
            align_unit_vect = self.UnitizeEffect(u_div, v_div,align_unit_vect) * align_fac

            return align_unit_vect

        else:
            return rg.Vector2d(0,0)


    def Separation (self, radius, agents, u_div, v_div, avoid_fac):
        # fx for Separation
        """within the specified radius we need to iterate over each agent apart from ours and do the following:
        -> define how close two agents can be [min distance before collision]
        -> define a new direction [maybe reversed]
        """
        num_neighbors =0
        moveU=0
        moveV=0
        for agent in agents:
            if not agent == self:
                dist = self.position.DistanceTo(agent.position)
                if dist<= radius:
                    num_neighbors =-1
                    moveU = self.u - agent.u
                    moveY = self.v - agent.v

        if  num_neighbors > 0:

            avoid_unit_vect = rg.Vector2d(moveU, moveV)
            avoid_unit_vect = self.UnitizeEffect(u_div, v_div,avoid_unit_vect) * avoid_fac

            return avoid_unit_vect
        else
            return rg.Vector2d(0,0)

        
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
        #to be cheked!!
        if self.u <= 0:
            self.u = 0
            self.du *= -1

        elif self.u >=1:
            self.u = 1
            self.du *= -1

        #pending: we need to rethink this point and check again!!!  

        if self.v >=1:
            self.v =1
            self.arrived =True


    # pending: fx for limiting speed?

    # helper fxs:7

    # add the effect to the new veloctity vector of the agent that will be added later to its current velocity
    # as an input is the vector of a certain effect, the function does the following
    # --> unitize the vector
    # --> multiply by the effect value 
    # --> add this value to sum of new velocity vector 
    # --> this fx is called in each effect fx 
    def UnitizeEffect(self, u_div, v_div, vector_2b_unitised):           
        vector_2b_unitised.Unitize()
        vector_2b_unitised = rg.Vector2d(vector_2b_unitised.X/u_div, vector_2b_unitised.Y/v_div)
        return vector_2b_unitised

    # adds the new velocty vector to the current velocity vector and unitizes it 
    def AddTotalEffect(self, u_div, v_div, effects_vector):
        effects_vector += rg.Vector2d(self.du, self.dv)
        return self.UnitizeEffect(u_div, v_div, effects_vector)

    # update the agent's params and move it one step forward
    def AgentStep(self, effects_vector):
        self.du = effects_vector.x
        self.dv = effects_vector.y
        self.u += self.du
        self.v += self.dv
        self.pts.append(self.surface.PointAt(self.u, self.v))
       

    #hello Eleniiiii
    #hello Ahmed
######################################################################################################################################
# the execution function:
# given the list of different points to initiate the agents do:
# a for loop iterating over the lists, instantiating each agent in the list then instantaiting an environment given all these agents
# afterwards, for each environment do some action till a certain time t
# afterwards instantiate a bigger environment containing all agents and giving it a certain value for all parameters.


#Swap UV directions of surface if needed
corner_b= surface.PointAt(1,0)
corner_d= surface.PointAt(0,1)

if corner_b.Z > corner_d.Z:
    surface.Transpose(True)



initial_env_list = []
u_lists = th.tree_to_list(u_lists)
target_factors = th.tree_to_list(target_factors)
for u_list, t_factor in zip(u_lists, target_factors):
    #instantiate an instance of the environment:
    new_env = Environment(u_div, v_div, surface)
    new_env.populate_agents(u_list, t_factor)
    initial_env_list.append(new_env)

#depending on the input timestep we update the agents
for t in range(time_1):
    for env in initial_env_list:
        env.update_agents_pos(coherence_rad, coherence_fac, align_rad, align_fac, avoid_rad, avoid_fac)

list_pts = []
paths=[]
for env in initial_env_list:
    list_pts.append([agent.pts for agent in env.agents])
    path = surface.InterpolatedCurveOnSurface([agent.pts for agent in env.agents],tolerance)
    paths.append(path)

paths = th.list_to_tree(paths)
list_pts = th.list_to_tree(list_pts)
