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
        Worldview = "A" #ideology of the individual 
        Zealot = False #boolean indicating if the the individual is a zealot or not 
        Leader = False #boolean indicating if the individual is a leader in the organization (may have multiple
                 #leaders) and thus has hiring power  
        TOPP = .5 #percentage of org of opp ideology at which individual resigns 
        THOM - .5 #percentage of org that is same ideology at which individual resigns 
        is_listeneer = False 

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
        Org_size = 1000 
        Worldviews = ["A", "A'", "AB", "B", "B'"]
        Config =  [.2, .2, .2, .2, .2} ]#initial fractional representation of each worldview
        
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
        
        Mode = "D"  
        Turnover_rate = .01
        Workforce = []
        Num_interact = 0
        Leader = None 
       
    def populate(self):
        #Here, we want to populate the organization with individuals
        leader = random.randint(0, Org_size) 

        for i in range(Org_size): 
            self.Workforce.append(Individual())
            #draw TOPP and THOM from random distribution, but set THOM at least as high as TOPP 
            self.Workforce[i].TOPP = np.random.uniform(0,1)
            self.Workforce[i].THOM = np.random.uniform(self.Workforce[i].TOPP,1)

            #set individual's worldview based on organization config 
            self.Workforce[i].Worldview = np.random.choice(self.Worldviews, 1, p = self.Config)
            
            #set leader if the right individual
            if i == leader: 
                self.Workforce[i].Leader = True
                self.Leader = self.Workforce[i]
            
            if self.Workforce[i].Worldview == "B'" or self.Workforce[i].Worldview == "A'": 
                self.Workforce[i].Zealot = True 

            #updating global org config to true values  
            self.update_config(self.Workforce[i], "increment") 

       pass 
    
    def update_config(self, individual, change): 
        #function is meant to update the organizations n_* and N_* 
        #when changes are made (increment, decrement)

        if change == "increment":
            if individual.Worldview == "A":
                N_A += 1 
                n_A = Org_size/n_A
                pass 
            elif individual.Worldview == "A'": 
                N_A2 += 1 
                n_A2 = Org_size/n_A2
                pass 
            elif individual.Worldview == "AB":
                N_AB += 1 
                n_AB = Org_size/n_AB
                pass 
            elif individual.Worldview == "B": 
                N_B += 1 
                n_B = Org_size/n_B
                pass 
            elif individual.Worldview == "B'": 
                N_B2 += 1 
                n_B2 = Org_size/n_B2
                pass 

        elif change == "decrement":
            if individual.Worldview == "A":
                N_A -= 1 
                n_A = Org_size/n_A
                pass 
            elif individual.Worldview == "A'": 
                N_A2 -= 1 
                n_A2 = Org_size/n_A2
                pass 
            elif individual.Worldview == "AB":
                N_AB -= 1 
                n_AB = Org_size/n_AB
                pass 
            elif individual.Worldview == "B": 
                N_B -= 1 
                n_B = Org_size/n_B
                pass 
            elif individual.Worldview == "B'": 
                N_B2 -= 1 
                n_B2 = Org_size/n_B2
                pass
            pass 

        pass 

    def interact(self):
        #randomnly select two individuals from the workforce 
        listener = self.Workforce[random.randint(0, Org_size)]
        speaker = self.Workforce[random.randint(0, Org_size)] 
        
        #decrement global state w/ respect to pre-interaction 
        #listener worldview 
        self.update_config(listener, "decrement")

        #interaction takes place 
        listener.listen(speaker)

        #increment global state w/ respect to post-interaction
        #listener worldview 
        self.update_config(listener, "increment")

        pass 

    def hire(self, leader):
        #if in default mode 

        pass 

    def fire(self): 
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
''' 


