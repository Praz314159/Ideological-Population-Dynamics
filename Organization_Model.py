'''
Organizational population dynamics model in python 
This is a matlab model meant to demonstrate how hiring can be used as a mechanism to mitigate 
ideological homogeneity within an organization and, conversely, how it can be used as a mechanism
to create an organization full of zealots. TY SEEDS OF PEACE!!!! 

Model Assumptions Assumptions: 

1. No correlation between incompetency and ideology 
2. 3 basic hiring modes: Default (D), Leadership Self-Replication (SR), Anti Leadership Self-Replication (ASR)
3. Individuals change their mind through speaker-listener interactions 
4. When an individual engages in an interaction as a listener, they only move one position in the direction of the 
   speaker.
5. Every individual within the organization has complete knowledge of the organization state -- that is, what everybody 
   thinks at any given point in time. This is perhaps the most unrealistic assumption, since  

PREFERENCE FALSIFICATION!!!! 

Model Functionality:  

 1. We have the following general rules: 
 A,A' |  B  |  AB
 A,A' |  AB |  A
 B    |  A  |  AB
 B    |  AB |  B

 2. Each individual has 2 threshold values
    1. TOPP --> this is the percentage of the organization that is of the opposite ideology of the individual at 
                which the individual resigns. TOPP is a measure of an individual's tolerance for being in the
                minority. 
    2. THOM --> this is the percentage of the organization that is of the same ideology of the individual at which
                the individual resigns. THOM is a measure of an individual's absolute tolerance for ideological 
                homogeneity 
    Notice that THOM = 1 - TOPP. We make this reasonable simplifying assumption 

3. Any organization will have a natural steady turn over rate. We assume that individuals won't be fired for 
  ideological reasons unless the leader is a zealot. In the normal case, once an individual leaves the organization
  (incompetence, surpassed threshold), they are replaced by someone from the hiring pool. Here are some factors to 
  consider: 
    1. The HP might be ideologically biased --> note that unbiased hring (D mode) will select for this bias 
    2. If in SR mode, then bias of leader compounds the HP bias 
    3. If in ASR mode, then bias of leader will counteract HP bias 

4. We have a global scaling of probabilities with which A --> A' and B --> B' that is based on the % of the 
   organization that is either A or B. The idea here is that the more homogenous the organization, the less 
   of a social cost there is for being a zealot; in fact, one may even be able to accrue social capital by 
   becoming a zealot. 
    1. Bias = <B_1, B_2, .... ,B_n> <==> Probs = <P_1, P_2, ... ,P_n>
    2. This type of switch will only occur when the speaker is a zealot and the listener is a non-zealot with 
       the same worldview 

    The function mapping degree of homogeneity to probability of switching from non-zealot to zealot will
    be the same for both cases, A --> A' and B --> B'. How should this mapping behave be structured. First, 
    it seems reasonable that there would be a long leading tail. It will only become advantageous, either 
    to accrue social capital or to avoid social destruction, to become a zealot if the organization is highly
    homogenous with respect to your worldview (>80%?). 

    People with high thresholds for homogeneity will likely end up as zealots if the organization tends 
    towards homogeneity in their worldview. 

    We have buckets <5, 10, 15, 20, 25, 30, 35, 40, 45, 50 ... >. These are associated with the following
    probabilities. 

''' 
import math 
import numpy as np
import random 
import argparse 

HP_SIZE = 1000 #number of individuals in hiring pool 
HP_CONFIG = {"B":.2, "B'":.2,"AB":.2,"A":.2,"A'":.2} #fractional representation of individual types in HP

class Individual: 
    def __init__(self):
        #Personal Parameters
        Worldview = "A" #ideology of the individual 
        Zealot = False #boolean indicating if the the individual is a zealot or not 
        Leader = False #boolean indicating if the individual is a leader in the organization (may have multiple
                 #leaders) and thus has hiring power  
        TOPP = .5 #percentage of org of opp ideology at which individual resigns 
        THOM - .5 #percentage of org that is same ideology at which individual resigns 
        
        #Org parameters 
        Organization = None #organization that individual belongs to  
        Org_pos = 0 #index in organization workforce list 
        

    def listen(self, speaker):
        '''
        Consider what happens when an individual is the listener in an interaction. We have various scenarios. 
        Each of these scenarios must be hardcoded:
            1. If speaker is A and listener is B, then the listener is converted to AB 
            2. If speaker is A' and listener is B, then the listener is subject to preference falsification, 
               meaning that they may lie about being a B. That is, they will pretend to be closer to worldview A. 
               We assume that this means that B is acting as an AB, and will therefore be converted to an A. 
            3. If speaker is B' and listener is A, then then, similarly, the listener will lie about being a true 
               A and will pretend to be an AB in the interaction. They will subsequently be converted to a B.
            4. If speaker is A' and listener is A, then the listener will change to A' if the global state of the 
               organization is such that a particular 

            depending on how homogenous in A the organization is, A will turn to A'. It shouldn't 
            be advantageous to switch until the organization is very homogenous in A. There is also
            a question about when it becomes socially |unacceptable| to not be a zealot. There is 
            some interesting dynamics between people leaving because the organization is too 
            homogenous and other people staying because there is social benefit to becoming
            a zealot, or, if the organization is extremely homogenouse, social cost to not becoming one
        '''
        if (speaker.Worldview == "A" and self.Worldview == "B") or (speaker.Worldview == "B" and self.Worldview == "A"): 
            self.Worldview = "AB" 
        elif (speaker.Worldview == "A'" and self.Worldview == "B") or ((speaker.Worldview == "A" or speaker.Worldview == "A'") \
                and self.Worldview == "AB"):
            #preference falsification accounted for 
            self.Worldview = "A"
        elif (speaker.Worldview == "B'" and self.Worldview == "A") or ((speaker.Worldview == "B" or speaker.Worldview == "B'") \
                and self.Worldview == "AB"):
            #preference falsification accounted for 
            self.Woldview = "B" 
        elif speaker.Worldview == "A'" and self.Worldview == "A": 
            pass 
        elif speaker.Worldview == "B'" and self.Worldview == "B": 
            pass
        else: 
            pass 

    #think about what other functionality I might want to give individuals 

class Organization: 
    def __init__(self):
        #Fixed parameters 
        Org_size = 1000
        Worldviews = ["A", "AB", "B"]
        Config =  [.33, .33, .33] #initial fractional rep in org
        A_config = .5 
        B_config = .5
        
        #Fixed HP parameters
        H_config = [.33, .33, .33] #fractional rep in hiring pool 
        HP_size = 5000 
        A_HPconfig = .5 
        B_HPconfig = .5 
        
        #n_* is the current fractional representation of each worldview
        n_A = 0
        n_A2 = 0
        n_AB = 0
        n_B = 0
        n_B2 = 0 

        #N_* is the absolute number of individuals with each worldview 
        N_A = 0
        N_A2 = 0
        N_AB = 0
        N_B = 0
        N_B2 = 0
        
        #Behavioral parameters 
        Mode = "D"  
        Turnover_rate = .01
        Workforce = []
        Num_interactions = 0
        Leader = None 
       
    def populate_org(self):
        #Here, we want to populate the organization with individuals 

        for i in range(Org_size): 
            self.Workforce.append(Individual())
            self.Workforce[i].Org_pos = i 

            #draw TOPP and THOM from random distribution, but set THOM at least as high as TOPP 
            self.Workforce[i].TOPP = np.random.uniform(0,1)
            self.Workforce[i].THOM = np.random.uniform(self.Workforce[i].TOPP,1)

            #set individual's worldview based on organization config 
            self.Workforce[i].Worldview = np.random.choice(self.Worldviews, 1, p = self.Config)
            
            #set leader first individual in list as 0
            if i == 0: 
                self.Workforce[i].Leader = True
                self.Leader = self.Workforce[i]
            
            #creating zealots 
            if self.Workforce[i].Worldview == "B":
                if random.random() < B_config: 
                    self.Workforce[i].Zealot = True 
            elif self.Workforce[i].Worldview == "A": 
                if random.random() < A_config: 
                    self.Workforce[i].Zealot = True 

            #updating global org config to true values  
            self.update_config(self.Workforce[i], "increment") 
       pass 
        
    def populate_HP(self):
        #Here, we want to populate the organization with individuals 
        for i in range(HP_size): 
            self.HP.append(Individual())
            self.HP[i].Org_pos = i 

            #draw TOPP and THOM from random distribution, but set THOM at least as high as TOPP 
            self.HP[i].TOPP = np.random.uniform(0,1)
            self.HP[i].THOM = np.random.uniform(self.HP[i].TOPP,1)

            #set individual's worldview based on organization config 
            self.HP[i].Worldview = np.random.choice(self.Worldviews, 1, p = self.H_config)
            
            #creating zealots 
            if self.HP[i].Worldview == "B":
                if random.random() < B_HPconfig: 
                    self.HP[i].Zealot = True 
            elif self.HP[i].Worldview == "A": 
                if random.random() < A_HPconfig: 
                    self.HP[i].Zealot = True 
    
    def update_config(self, individual, change): 
        #function is meant to update the organizations n_* and N_* 
        #when changes are made (increment, decrement)

        if change == "increment":
            if individual.Worldview == "A":
                if individual.Zealot == True:
                    self.N_A2 += 1
                    self.n_A2 = self.n_A2/self.Org_size 
                else:
                    self.N_A += 1 
                    self.n_A = self.n_A/self.Org_size
            elif individual.Worldview == "AB":
                self.N_AB += 1 
                self.n_AB = self.n_AB/self.Org_size
            elif individual.Worldview == "B":
                if individual.Zealot == True: 
                    self.N_B2 += 1
                    self.n_B2 = self.n_B2/self.Org_size
                else:
                    self.N_B += 1 
                    self.n_B = self.n_B/self.Org_size 

        elif change == "decrement":
             if individual.Worldview == "A":
                if individual.Zealot == True:
                    self.N_A2 -= 1
                    self.n_A2 = self.n_A2/self.Org_size 
                else:
                    self.N_A -= 1 
                    self.n_A = self.n_A/self.Org_size
            elif individual.Worldview == "AB":
                self.N_AB -= 1 
                self.n_AB = self.n_AB/self.Org_size
            elif individual.Worldview == "B":
                if individual.Zealot == True: 
                    self.N_B2 -= 1
                    self.n_B2 = self.n_B2/self.Org_size
                else:
                    self.N_B -= 1 
                    self.n_B = self.n_B/self.Org_size 

    def interact(self):
        #randomnly select two individuals from the workforce 
        listener = self.Workforce[random.randint(1, Org_size-1)]
        speaker = self.Workforce[random.randint(1, Org_size-1)] 
        
        #decrement global state w/ respect to pre-interaction 
        #listener worldview 
        self.update_config(listener, "decrement")

        #interaction takes place 
        listener.listen(speaker)

        #increment global state w/ respect to post-interaction
        #listener worldview 
        self.update_config(listener, "increment")
        self.Num_interactions += 1 
    
    
    def evaluate_polarization(self):
        pass

    def hire_with_probability(self, new_hire, position, probability):
        if random.random() < probability: 
            self.update_config(new_hire, "increment")
            self.Workforce[position ] = new_hire 
            new_hire.Org_pos = position 
    
    def fire_hire(self, leader):
        #depends on mode of hiring (D, SR, ASR) and, therefore, also
        #on the worldveiw of the leader. We have two major assumptions: 
        #1. leader can't distinguish between zealots and non-zealots. This 
        #means that if in SR mode, the leader is as likely to hire a 
        #non-zealot and zealot of the same worldview. 
        #2. hiring pool is pre-filtered for competence 
        #3. hiring only takes place when someone has been fired 
        
        #firing
        empty_pos = random.randint(1, Org_size-1) 
        new_fire = self.Workforce[empty_pos]
        self.update_config(new_fire, "decrement") 

        #Default hiring mode: selecting for pre-existing bias in hiring pool 
        if self.Mode == "D":
            new_hire = HP[random.randint(0, HP_size-1)] 
            self.update_config(new_hire, "increment") 
            self.Workforce[empty_pos] = new_hire
            new_hire.Org_pos = empty_pos
        #Self Replication hiring mode: selects for bias of the leader 
        elif self.Mode == "SR":
            for interview in range(10): 
                candidate = self.HP[random.randint(0, HP_size-1)]
                # [.75, .3, (.05, .1)]
                if self.leader.Worldview == "A":
                    if candidate.Worldview == "A":
                        self.hire_with_probability(candidate, empty_pos, .75)
                        break 
                    if candidate.Worldview == "B": 
                        if candidate.Zealot == True:
                            self.hire_with_probability(candidate, empty_pos, .05) 
                            break
                        else:
                            self.hire_with_probability(candidate, empty_pos, .1) 
                            break  
                    if candidate.Worldview == "AB":
                        self.hire_with_probability(candidate, empty_pos, .3) 
                        break 
                # [(.05, .1), .3, .75]
                elif self.leader.Worldview == "B":
                    if candidate.Worldview == "A": 
                        if candidate.Zealot == True: 
                            self.hire_with_probability(candidate, empty_pos, .05) 
                            break
                        else:
                            self.hire_with_probability(candidate, empty_pos, .1) 
                            break
                    if candidate.Worldview == "B":
                        self.hire_with_probability(candidate, empty_pos, .75)
                        break
                    if candidate.Worldview == "AB":
                        self.hire_with_probability(candidate, empty_pos, .3) 
                        break
                # [.3, .5, .3]
                elif self.leader.Worldview == "AB":
                    if candidate.Worldview == "A":
                        self.hire_with_probability(candidate, empty_pos, .3) 
                        break
                    elif candidate.Worldview == "B":
                        self.hire_with_probability(candidate, empty_pos, .3) 
                        break
                    elif candidate.Worldview == "AB":
                        self.hire_with_probability(candidate, empty_pos, .5) 
                        break 
        #Anti Self-Replication hiring mode: reacting to polarization in organization  
        elif self.Mode == "ASR": 
            pass 
        pass 


def main(): 
    #The purpose here is be able to run simulations from the command line 
    #Eventually, we should be able to automate many simulations with 
    #various parameters to explore how the system depends on them. 
    #For now, though, we just create a command line tool in order to 
    #run sims easily and check how things are working ... 
    

    parser = argparse.ArgumentParser() #creating argument parser
    


if __name__ == "__main__": 
    main() 


'''
TO DO: 
    1. Think more carefully about methods of Individual and Organization. The ones included now are preliminary.
    2. Code the actual behavior of the model --> how does the model evolve? EPOCHs? 

Parameters at disposal of simulation runner:  
    1. List of fractional representations fore each of the worldviews 
    2. Distribution of TOPP in the org
    3. Distribution of THOM in the org 
    4.  


TOPP vs THOM: 

It makes sense that for an individual, they are much less likely to quit if
they are in a community in which they are not the ideological majority than if they are in the ideological
minority. That is, that they are able to tolerate homogeneity more than opposition. So, it makes sense that
THOM >= TOPP. At the same time, however, if THOM = .05 for individual X, then that means if 5% of the 
community has the same worldview as X, then X will resign. This also means, however, by definition, that 
if TOPP = .95. That is, if 95% of the community has the opposite worldview of X, then X will resign. So, 
THOM(X) = .05 --> THOM(X) = .95 --> if X resigns, then (A + A')/N >= .95 or (B + B')/N >= .95, where 
N = Org_Size. Note that this can only happy during extreme polarization. The moderates, therefore, 
act as a cohesive binding that keeps the community from fraying at the edges.

Now, there is the question of what distribtuio

SR Mode: 

what does being in self_replication mode mean? It means that the leader is much more likely to hire someone 
who thinks like him. But, how much more likely? Certainly, they will never hire a zealot with the opposite 
worldview because they would be more outspoken and the interaction would spoil. Might hire AB or non-zealot 
opp, but is most likley to hire someone with the same worldview. What scheme can this be reflected by? 
The most straightforward way to do this is to change the likelhoods associated with choosing each 
worldview (i.e, a different "H_config" when in SR mode). The other way to do this is to set up "interviews"
in which candidates are randomly chosen from the hiring pool, but the likleyhood that worldviews are selected
are different. What should these probabilities be!!? Let's try P(Opp_z) = .05, P(Opp_nz) = .1, P(AB) = .3, 
P(Same) = .75

ASR Mode: 

What does being in anti self-replication mode mean? It means that the leader is trying to maintain ideological
diversity within the organization. 
''' 


