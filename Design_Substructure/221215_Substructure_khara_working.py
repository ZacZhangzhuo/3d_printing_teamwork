import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import random
import math
from copy import deepcopy

#hellooo
random.seed(seeed)
tolerance = 0.001

#this class is focused on the properties and methods of each instance MAS (multi agent system)
class Environment(object):
    
    def __init__(self, u_div, v_div, surface, agents_list = [], repulsion_thresh = 0.5):
        #self.num_agents = 0    #total number of agents
        self.u_div = u_div
        self.v_div = v_div
        self.surface = surface
        self.agents = []
        self.main_agents = []
        self.sub_agents = []

        self.finished_agents = []
        if len(agents_list) > 0:
            self.agents = agents_list
            self.main_agents = [agent for agent in agents_list]
        self.repulsion_thresh = repulsion_thresh
        self.strong_agents = self.GenerateStrongAgentsList()

    #this function takes the u values and transform them into agents
    def populate_agents(self, u_vals, target_factors):
        # instantiatie all agents
        for u, t_fac in zip(u_vals,target_factors) :
            self.agents.append(Agent(u, 0, 0, t_fac / self.v_div,t_fac, self.surface)) 

    #generates new agents in the env 
    def populate_sub_agents(self, prev_envs, num_new_agents, shift_up_factor,shift_down_factor, sub_goal_fac):
        #rememeber to add to the full list of agents
        sub_agents = []
        goals=[]
        all_v = []
        for env in prev_envs:
            boundary = env.CalculateBoundaryRegion()
            all_v.append(boundary[-1])
            for i in range(num_new_agents):
                u = Remap(random.random(),0,1, boundary[0], boundary[1])
                v = Remap(random.random(),0,1, boundary[2], boundary[3])
                sub_agents.append(Agent(u,v,0,0,0,self.surface)) #pending !!

        #populate each point separately 
        #get the highest value of v 
        print (all_v)
        all_v.sort()
        lower_bound_v = all_v[-1]
        lower_bound_v += shift_up_factor 
        upper_bound_v = 1 - shift_down_factor
        for sub_agent in sub_agents:
            sub_agent.isSubAgent = True
            sub_agent.sub_goal_u = random.random()
            sub_agent.sub_goal_v = Remap(random.random(), 0, 1, lower_bound_v, upper_bound_v)
            goals.append(self.surface.PointAt( sub_agent.sub_goal_u, sub_agent.sub_goal_v))
            raw_du = sub_agent.sub_goal_u - sub_agent.u
            raw_dv = sub_agent.sub_goal_v - sub_agent.v
            vector = rg.Vector2d(raw_du, raw_dv)
            unit_vect = sub_agent.UnitizeEffect(self.u_div, self.v_div, vector)
            sub_agent.du = sub_goal_fac * unit_vect.X
            sub_agent.dv = sub_goal_fac * unit_vect.Y
            self.agents.append(sub_agent)
            self.sub_agents.append(sub_agent)
        return goals, [agent.pts for agent in sub_agents]
        
    



    def update_agents_pos (self, coherence_rad, coherence_fac, align_rad, align_fac, avoid_rad, avoid_fac, Coherence_T, Alignment_T, Separation_T, sub_goal_rad = 0, sub_goal_fac = 0):
        # generate the new position of each agent by calculating their new direction and velocity
        #for each agent apply all the functions on it given the required factors for each parameter
        #if the agent arrives we pop out this agent from the list and add it to the finished list 
        # add a function that if everything is arrived just stop 
        #list of all effects so as not to change the behaviour of the agents during update
        effects_list = []
        for agent in self.agents:
            #always add a positive up vector in the beginning
            if agent.isSubAgent:
                agent.UpdateSubAgentProgress(sub_goal_rad, sub_goal_fac, self.u_div, self.v_div)
            effects_vector = rg.Vector2d(agent.right_force,agent.up_force)            

            if Coherence_T:
                coherence_vector = agent.Coherence(coherence_rad, self.agents, self.u_div, self.v_div, coherence_fac)
                effects_vector += coherence_vector

            if Alignment_T:
                alignment_vector = agent.Alignment(align_rad, self.agents, self.u_div, self.v_div, align_fac)
                effects_vector += alignment_vector

            if Separation_T:
                separation_vector = agent.Separation(avoid_rad, self.agents, self.u_div, self.v_div, avoid_fac)
                effects_vector += separation_vector

                #sum all of the vectors + the actual du and dv of the agent + unitize --> do nothing but add them to the effects_list
                effects_list.append(agent.AddTotalEffect(self.u_div, self.v_div, effects_vector))


        temp_removed_agents = []
        for agent, effect in zip(self.agents, effects_list):
            agent.AgentStep(effect)
            if agent.arrived:
                temp_removed_agents.append(agent)
       
        for fin_agent in temp_removed_agents:
            self.finished_agents.append(fin_agent)
            self.agents.remove(fin_agent)


        #pending: function that ensures all agents have reached the final destination
    #checks all agents in the environment if they are strong or not based on their direction vector
    def GenerateStrongAgentsList(self):
        strong_Agents_list = []
        for agent in self.agents:
            if agent.unitized_upForce > self.repulsion_thresh:
                strong_Agents_list.append(agent)
        return strong_Agents_list

    #from an environment detects the minimum and maximum boundary
    def CalculateBoundaryRegion(self):
        all_u = [agent.u for agent in self.agents]
        all_u.sort()

        all_v = [agent.v for agent in self.agents]
        all_v.sort()

        return [all_u[0], all_u[-1],all_v[0], all_v[-1]]
    

            
class Agent(object):

#the main parameters are poisiton on the surface, velocity in both directions 
    def __init__(self, u, v, du, dv,unit_dv, surface):
        self.u = u
        self.v = v
        self.surface = surface
        self.position = self.surface.PointAt(self.u, self.v) ##for the surface

        #save the dv as the constant upward vector for the current agent
        self.up_force = dv

        self.right_force = 0
        self.unitized_upForce = unit_dv #unitized value of the up vector
        #print (self.unitized_upForce)
        self.du = du
        self.dv = dv
        self.pts = []
        self.pts.append(self.position)
        self.arrived = False

        self.isSubAgent = False
        self.sub_goal_u = 0
        self.sub_goal_v = 0

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

    # fx for Alignment (match velocity)
    def Alignment(self, radius, agents, u_div, v_div, align_fac):
        
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
    
    #pending: trial
    def Separation (self, radius, agents, u_div, v_div, avoid_fac):
        # fx for Separation
        """within the specified radius we need to iterate over each agent apart from ours and do the following:
        -> define how close two agents can be [min distance before collision]
        -> define a new direction [maybe reversed]
        """
        move_dU= 0
        move_dV= 0

        min_dist = 1000000
        closest_agent = self

        for agent in agents:
            if not agent == self:
                dist = self.position.DistanceTo(agent.position)
                if dist<= radius:
                    if dist < min_dist:
                        min_dist = dist
                        closest_agent = agent
        if closest_agent != self:
            move_dU += self.u - closest_agent.u
            move_dV += self.v - closest_agent.v

            avoid_unit_vect = rg.Vector2d(move_dU, move_dV)
            avoid_unit_vect = self.UnitizeEffect(u_div, v_div,avoid_unit_vect) * avoid_fac
            return avoid_unit_vect

        else:
            return rg.Vector2d(0,0)
    

    #checks the boundaries and for end of life of agent
    def withinBounds (self): 
        """
        ->check if (0<=u,v<=1)
        ->if not mirror u (*-1)
        ->
        """
        if abs(0.5 - self.u) >= 0.5 :       
            if self.u < 0:
                self.u = 0

            elif self.u > 1:
                self.u = 1
            self.du*=-1
            #self.right_force *=-1
            #self.arrived=True
            
        #we check if it has arrived (finished)  
        if self.v >= 1:
            self.v = 1
            self.arrived = True

    #update the distance to goal until reaching the radius and then change direction and disable the agent 
    def UpdateSubAgentProgress(self, radius,factor, u_div, v_div):
        #calculate distance to the goal point at certain instant
        raw_du = self.sub_goal_u - self.u
        raw_dv = self.sub_goal_v - self.v
        vector = rg.Vector2d(raw_du, raw_dv)
        distance = vector.Length

        #update the direction unit towards the goal
        unitized_vector = self.UnitizeEffect(u_div, v_div, vector)
        self.right_force = unitized_vector.X * factor
        self.up_force = unitized_vector.Y * factor

        #if the goal was reached, flip the du and right_force (the latter will be contant till the end of the game)
        if distance <= radius:
            self.du *= -1  
            #disable subagent  
            self.isSubAgent = False 
            self.right_force *= -1    
            

        


    
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

    # update the agent's params and move it one step forward while checking its elgibility for movement
    def AgentStep(self, effects_vector):

        self.du = effects_vector.X
        self.dv = effects_vector.Y
        
        if self.dv< 0:
            self.dv *=-10
        self.u += self.du
        self.v += self.dv
        #checks the agent compliance with boundary
        self.withinBounds()

        self.pts.append(self.surface.PointAt(self.u, self.v))

class SubGoal(object):

    def __init__(self):
        self.u = 0
        self.v = 0
        self.buffer_Zone = 0
         

    #hello Eleniiiii
    #hello Ahmed
######################################################################################################################################
# the execution function:
# given the list of different points to initiate the agents do:
# a for loop iterating over the lists, instantiating each agent in the list then instantaiting an environment given all these agents
# afterwards, for each environment do some action till a certain time t
# afterwards instantiate a bigger environment containing all agents and giving it a certain value for all parameters.
#helpful functions:
def Remap(value, min, max, new_min, new_max):
    old_range = max - min
    new_range = new_max - new_min
    return (((value - min)* new_range)/ old_range) + new_min


#Swap UV directions of surface if needed
corner_b= surface.PointAt(1,0)
corner_d= surface.PointAt(0,1)

if corner_b.Z > corner_d.Z:
    surface.Transpose(True)

all_agents = []
################################strt with first phase (t1)###############################
initial_env_list = []
u_lists = th.tree_to_list(u_lists)
target_factors = th.tree_to_list(target_factors)
for u_list, t_factor in zip(u_lists, target_factors):
    #instantiate an instance of the environment:
    new_env = Environment(u_div, v_div, surface)
    new_env.populate_agents(u_list, t_factor)
    #add all agents to the big list
    all_agents.extend(new_env.agents)
    initial_env_list.append(new_env)

pts_list = []
#depending on the input timestep we update the agents
for t in range(time_1):
    for env in initial_env_list:
        env.update_agents_pos(coherence_rad, coherence_fac, align_rad, align_fac, avoid_rad, avoid_fac, Coherence_T, Alignment_T, Separation_T)

###############################second phase (t2)#########################################
#Create a new env containing all agents
combined_env = Environment(u_div, v_div, surface, all_agents)
#add the new sub_agents

goals, sub_agents = combined_env.populate_sub_agents(initial_env_list, num_new_agents, shift_up_factor, shift_down_factor, sub_goal_fac)

for t in range(time_2):
    combined_env.update_agents_pos(coherence_rad2, coherence_fac2, align_rad2, align_fac2, avoid_rad2, avoid_fac2, Coherence_T2, Alignment_T2, Separation_T2, sub_goal_rad, sub_goal_fac)

list_pts = []
main_paths = []
sec_paths = []

for agent in combined_env.main_agents:
    #if agent.right_force != 0:
    path = surface.InterpolatedCurveOnSurface(agent.pts,tolerance) 
    if Rebuild_T:
        path= path.Rebuild(rebuild_points, rebuild_degree, True)
        path.Domain = rg.Interval(0.0, 1.0)
        main_paths.append(path)  
for agent in combined_env.sub_agents:
    path = surface.InterpolatedCurveOnSurface(agent.pts,tolerance) 
    if Rebuild_T:
        path= path.Rebuild(rebuild_points, rebuild_degree, True)
        path.Domain = rg.Interval(0.0, 1.0)
        sec_paths.append(path)

#sub_agents = th.list_to_tree(sub_agents)
main_paths = th.list_to_tree(main_paths)
sec_paths = th.list_to_tree(sec_paths)
list_pts = th.list_to_tree(list_pts)
