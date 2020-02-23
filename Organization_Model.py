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
    probabilities: <.01, .02, .05, .07, .1, .135, .17, .205, .4, .45, .51, .58, .66, .75, .85, .95, .96, .97, .98. .99> 

''' 
import math 
import numpy as np
import random 
import argparse 
from matplotlib import pyplot as plt 

class Individual: 
    def __init__(self):
        #Personal Parameters
        self.Worldview = "A" #ideology of the individual 
        self.Zealot = False #boolean indicating if the the individual is a zealot or not 
        self.Leader = False #boolean indicating if the individual is a leader in the organization (may have multiple
                 #leaders) and thus has hiring power  
        self.TOPP = .5 #percentage of org of opp ideology at which individual resigns 
        self.THOM = .5 #percentage of org that is same ideology at which individual resigns 
        #self.Zealot_resistance_buckets = [.05, .1, .15, .2, .25, .3, .35, .4, .45., .5, .55, .6, .65, .7,. 75, .8, .85, .9 \
        #        .95, 1]
        self.Zealot_resistance_probabilities =  [.01, .03, .05, .07, .1, .135, .17, .205, .4, .45, .51, .58, .66, .75, .85,\
                .95, .96, .97, .98, .99]

        #Org parameters 
        self.Organization = None #organization that individual belongs to  
        self.Org_pos = 0 #index in organization workforce list 
        
    def resign(self): 
        empty_pos = -1
        n = self.Organization.get_statistics()[1] 
        if self.Worldview == "A":
            if n.get("n_A") + n.get("n_A2") > self.THOM:
                empty_pos = self.Organization.accept_resignation(self) 
            elif n.get("n_B") + n.get("n_B2") > self.TOPP: 
                empty_pos = self.Organization.accept_resignation(self)
        elif self.Worldview == "AB":
            if n.get("n_AB") < .1*(1-n.get("n_AB")):
                empty_pos = self.Organization.accept_resignation(self) 
            elif n.get("n_AB") > self.THOM: 
                empty_pos = self.Organization.accept_resignation(self)  
        elif self.Worldview == "B": 
            if n.get("n_B") + n.get("n_B2") > self.THOM:
                empty_pos = self.Organization.accept_resignation(self)
            elif n.get("n_B") + n.get("n_B2") > self.TOPP: 
                empty_pos = self.Organization.accept_resignation(self) 
        
        return empty_pos 

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
            a zealot, or, if the organization is extremely homogenous, social cost to not becoming one
        '''    
        n = self.Organization.get_statistics()[1]
        N = self.Organization.get_statistics()[0]

        if (speaker.Worldview == "A" and speaker.Zealot == False and self.Worldview == "B" and self.Zealot == False ) \
                or (speaker.Worldview == "B" and speaker.Zealot == False and self.Worldview == "A" and self.Zealot == False): 
            self.Worldview = "AB" 
        elif ((speaker.Worldview == "A" and speaker.Zealot == True) and ((self.Worldview == "B" or self.Worldview == "AB") and \
                self.Zealot == False)) or (speaker.Worldview == "A" and speaker.Zealot == False and self.Worldview == "AB" \
                and self.Zealot == False):
            self.Worldview = "A" 
        elif ((speaker.Worldview == "B" and speaker.Zealot == True) and ((self.Worldview == "A" or self.Worldview == "AB")\
                and self.Zealot == False)) or (speaker.Worldview == "B" and speaker.Zealot == False and self.Worldview == "AB"\
                and self.Zealot == False): 
            self.Worldview == "B"
        elif speaker.Worldview == "A" and speaker.Zealot == True and self.Worldview == "A" and self.Zealot == False:
            #the key is that we have access to the global state of the organization, which means that we 
            #do indeed know how homogenous the organization is in A, for example. 
            #bucket = math.floor((n.get("n_A") + n.get("n_A2"))/.05) 
            if math.floor((n.get("n_A") + n.get("n_A2"))/.05) == 0: 
                bucket = 0
            else: 
                bucket = math.floor((n.get("n_A") + n.get("n_A2"))/.05) - 1  
            '''     
            print("\nSpeaker: ", speaker.Worldview, " Listener: ", self.Worldview)
            print("Bucket: ", bucket)
            
            print("A: ", N.get("N_A"))
            print("A Zealots: ", N.get("N_A2")) 
            print("B: ", N.get("N_B"))
            print("B Zealots: ", N.get("N_B2")) 
            print("Total Moderates: ", N.get("N_AB"))
            '''
            #getting likelhood that A --> A' 
            prob_switch = self.Zealot_resistance_probabilities[bucket]

            #A --> A' with assigned probability 
            if random.random() < prob_switch:
                self.Zealot == True 
        elif speaker.Worldview == "B" and speaker.Zealot == True and self.Worldview == "B" and self.Zealot == False:
            if math.floor((n.get("n_B") + n.get("n_B2"))/.05) == 0: 
                bucket = 0
            else: 
                bucket = math.floor((n.get("n_B") + n.get("n_B2"))/.05) - 1
            '''
            print("\nSpeaker: ", speaker.Worldview, " Listener: ", self.Worldview)
            print("Bucket: ", bucket)
            
            print("A: ", N.get("N_A"))
            print("A Zealots: ", N.get("N_A2")) 
            print("B: ", N.get("N_B"))
            print("B Zealots: ", N.get("N_B2")) 
            print("Total Moderates: ", N.get("N_AB"))
            '''
           
            #getting likelhood that B --> B' 
            prob_switch = self.Zealot_resistance_probabilities[bucket]

            #B --> B' with assigned probability 
            if random.random() < prob_switch:
                self.Zealot == True
        else: 
            pass 

        return 

    #think about what other functionality I might want to give individuals 

class Organization: 
    def __init__(self):
        #Fixed parameters 
        self.Org_size = 1000
        self.Worldviews = ["A", "AB", "B"]
        self.Config =  [.33, .34, .33] #initial fractional rep in org
        self.A_config = .1 
        self.B_config = .1
        
        #Fixed HP parameters
        self.H_config = [.33, .34, .33] #fractional rep in hiring pool 
        self.HP_size = 5000 
        self.A_HPconfig = .1 
        self.B_HPconfig = .1 
        
        #Behavioral parameters 
        self.Mode = "D"  
        self.Turnover_rate = .01 #probably don't need 
        self.Workforce = []
        self.HP = []
        self.Num_interactions = 0
        self.Leader = None 
        #self.polarization = self.n_A + self.n_A2 + self.n_B + self.n_B2 
       
    def populate_org(self):
        #Here, we want to populate the organization with individuals 

        for i in range(self.Org_size): 
            self.Workforce.append(Individual())
            self.Workforce[i].Org_pos = i 
            self.Workforce[i].Organization = self
            
            #draw TOPP and THOM from normal distribution, but set THOM at least as high as TOPP 
            self.Workforce[i].TOPP = np.random.normal(0.5, .1) #chose normal distribution 
            self.Workforce[i].THOM = np.random.uniform(self.Workforce[i].TOPP,1) 
            #does choosing uniformly greater than points drawn from normal distribution give a normal distribution? 

            #set individual's worldview based on organization config 
            self.Workforce[i].Worldview = np.random.choice(self.Worldviews, 1, p = self.Config)[0]
            
            #set leader first individual in list as 0
            if i == 0: 
                self.Workforce[i].Leader = True
                self.Leader = self.Workforce[i]
            
            #creating zealots 
            if self.Workforce[i].Worldview == "B":
                if random.random() < self.B_config: 
                    self.Workforce[i].Zealot = True 
            elif self.Workforce[i].Worldview == "A": 
                if random.random() < self.A_config: 
                    self.Workforce[i].Zealot = True 
        return  
        
    def populate_HP(self):
        #Here, we want to populate the organization with individuals 
        for i in range(self.HP_size): 
            self.HP.append(Individual())
            self.HP[i].Org_pos = i 

            #draw TOPP and THOM from random distribution, but set THOM at least as high as TOPP 
            self.HP[i].TOPP = np.random.uniform(0,1)
            self.HP[i].THOM = np.random.uniform(self.HP[i].TOPP,1)

            #set individual's worldview based on organization config 
            self.HP[i].Worldview = np.random.choice(self.Worldviews, 1, p = self.H_config)[0]
            
            #creating zealots 
            if self.HP[i].Worldview == "B":
                if random.random() < self.B_HPconfig: 
                    self.HP[i].Zealot = True 
            elif self.HP[i].Worldview == "A": 
                if random.random() < self.A_HPconfig: 
                    self.HP[i].Zealot = True 
        return 
  
    def interact(self):
        #randomnly select two individuals from the workforce 
        listener = self.Workforce[random.randint(1, self.Org_size-1)]
        speaker = self.Workforce[random.randint(1, self.Org_size-1)] 
        
        #print("LISTENER: ", listener.Worldview, " SPEAKER: ", speaker.Worldview) 
 
        listener.listen(speaker)
        self.Num_interactions += 1 
        '''
        N = self.get_statistics()[0]
        print("A: ", N.get("N_A"))
        print("A Zealots: ", N.get("N_A2")) 
        print("B: ", N.get("N_B"))
        print("B Zealots: ", N.get("N_B2")) 
        print("Total Moderates: ", N.get("N_AB"))
        '''    
           
        return 
    
    def evaluate_polarization(self):
        #this method is for when a more sophisticated evaluation of 
        #polarization is developed 
        pass

    def hire_with_probability(self, new_hire, position, probability):
        hired = False 
        if random.random() < probability:
            hired = True 
            self.Workforce[position] = new_hire 
            new_hire.Org_pos = position
            new_hire.Organization = self
            
            N = self.get_statistics()[0]
            print("\nHiring: ", new_hire.Worldview, " Hiring for Position: ", position) 
            print("A: ", N.get("N_A"))
            print("A Zealots: ", N.get("N_A2")) 
            print("B: ", N.get("N_B"))
            print("B Zealots: ", N.get("N_B2")) 
            print("Total Moderates: ", N.get("N_AB"))
            
        return hired
        
    def fire(self): 
        empty_pos = random.randint(1, self.Org_size-1)
        new_fire = self.Workforce[empty_pos]
        '''
        N = self.get_statistics()[0]
        print("\nFiring: ", new_fire.Worldview, " Firing for Position: ", empty_pos)
        print("A: ", N.get("N_A"))
        print("A Zealots: ", N.get("N_A2")) 
        print("B: ", N.get("N_B"))
        print("B Zealots: ", N.get("N_B2")) 
        print("Total Moderates: ", N.get("N_AB"))
        ''' 
        
        return empty_pos 
   
    def accept_resignation(self, new_resignation): 
        empty_pos = new_resignation.Org_pos 
        '''
        N = self.get_statistics()[0]
        print("\nResignation: ", new_resignation.Worldview, " Firing for Position: ", empty_pos)
        print("A: ", N.get("N_A"))
        print("A Zealots: ", N.get("N_A2")) 
        print("B: ", N.get("N_B"))
        print("B Zealots: ", N.get("N_B2")) 
        print("Total Moderates: ", N.get("N_AB"))
        ''' 
        return empty_pos

    def hire(self, empty_pos):
        #depends on mode of hiring (D, SR, ASR) and, therefore, also
        #on the worldveiw of the leader. We have two major assumptions: 
        #1. leader can't distinguish between zealots and non-zealots. This 
        #means that if in SR mode, the leader is as likely to hire a 
        #non-zealot and zealot of the same worldview. 
        #2. hiring pool is pre-filtered for competence 
        #3. hiring only takes place when someone has been fired 
        
        #Default hiring mode: selecting for pre-existing bias in hiring pool 
        if self.Mode == "D":
            new_hire = self.HP[random.randint(0, self.HP_size-1)]
            self.hire_with_probability(new_hire, empty_pos, 1) 

        #Self Replication hiring mode: selects for bias of the leader 
        elif self.Mode == "SR":
            #print("\nENTERING SR MODE")
            #possible we keep interviewing until we find someone ... 
            for interview in range(50): 
                candidate = self.HP[random.randint(0, self.HP_size-1)]
                #print("CANDIDATE ", interview, " Worldview: ", candidate.Worldview)
                
                # [.75, .3, (.05, .1)]
                if self.Leader.Worldview == "A":
                    if candidate.Worldview == "A":
                        if self.hire_with_probability(candidate, empty_pos, .75) == True:
                            break
                        else:
                            continue 
                    elif candidate.Worldview == "B": 
                        if candidate.Zealot == True:
                            #print("\n\n\nBEING A BITCH")
                            if self.hire_with_probability(candidate, empty_pos, .05) == True:
                                break
                            else:
                                continue
                        else:
                            if self.hire_with_probability(candidate, empty_pos, .1) == True:
                                break
                            else:
                                continue 
                    elif candidate.Worldview == "AB":
                        #print("\n\n\nBEING A BITCH")
                        if self.hire_with_probability(candidate, empty_pos, .3) == True:
                            break
                        else:
                            continue
                    
                # [(.05, .1), .3, .75]
                elif self.Leader.Worldview == "B":
                    if candidate.Worldview == "A": 
                        if candidate.Zealot == True:
                            #print("\n\n\nBEING A BITCH")
                            if self.hire_with_probability(candidate, empty_pos, .05) == True:
                                break
                            else:
                                continue
                        else:
                            #print("\n\n\nBEING A BITCH")
                            if self.hire_with_probability(candidate, empty_pos, .1) == True:
                                break
                            else:
                                continue
                    elif candidate.Worldview == "B":
                        #print("\n\n\nBEING A BITCH")
                        if self.hire_with_probability(candidate, empty_pos, .75) == True:
                            break
                        else:
                            continue
                    elif candidate.Worldview == "AB":
                        #print("\n\n\nBEING A BITCH")
                        if self.hire_with_probability(candidate, empty_pos, .3) == True:
                            break
                        else:
                            continue 
                        
                # [.3, .5, .3]
                elif self.Leader.Worldview == "AB":
                    if candidate.Worldview == "A":
                        #print("\n\n\nBEING A BITCH")
                        if self.hire_with_probability(candidate, empty_pos, .3)  == True: 
                            break
                        else:
                            continue 
                    elif candidate.Worldview == "B":
                        #print("\n\n\nBEING A BITCH")
                        if self.hire_with_probability(candidate, empty_pos, .3)  == True: 
                            break
                        else:
                            continue 
                    elif candidate.Worldview == "AB":
                        #print("\n\n\nBEING A BITCH")
                        if self.hire_with_probability(candidate, empty_pos, .5)  == True: 
                            break
                        else:
                            continue  
        
        #Anti Self-Replication hiring mode: reacting to polarization in organization  
        elif self.Mode == "ASR":
            #generate 10 candidates
            candidates = []
            has_moderate = False

            #selecting 20 candidates to interview
            for i in range(100): 
                candidates.append(self.HP[random.randint(0, self.HP_size-1)])
                if candidates[i].Worldview == "AB":
                    has_moderate = True 
            print("HAS MODERATE: ", has_moderate)
            n = self.get_statistics()[1]
            N = self.get_statistics()[0]
            polarization = self.get_statistics()[2] 

            #polarization threshold set to .75
            if polarization < .7:
                #if the polarization is tolerable, choose random 
                new_hire = self.HP[random.randint(0, self.HP_size-1)] 
                self.hire_with_probability(new_hire, empty_pos, 1) 
            else: 
                for candidate in candidates:
                    #if a moderate is a candidate, then hire him 
                    if has_moderate == True and candidate.Worldview == "AB": 
                        if self.hire_with_probability(candidate, empty_pos, 1) == True:
                            break
                        else:
                            continue
                    elif has_moderate == False and n.get("n_A") + n.get("n_A2") > n.get("n_B") + n.get("n_B2") and candidate.Worldview == "B":
                        if self.hire_with_probability(candidate, empty_pos, 1) == True:
                            break
                        else:
                            continue
                    elif has_moderate == False and n.get("n_A") + n.get("n_A2") < n.get("n_B") + n.get("n_B2") and candidate.Worldview == "A": 
                        if self.hire_with_probability(candidate, empty_pos, 1) == True: 
                            break
                        else:
                            continue
                    elif has_moderate == False and n.get("n_A") + n.get("n_A2") == n.get("n_B") + n.get("n_B2") and (candidate.Worldview == "A" or candidate.Worldview == "B"): 
                        if self.hire_with_probability(candidate, empty_pos, 1) == True:
                            break
                        else:
                            continue
        return


    def validate(self): 

        N = {"N_A": 0, "N_A2": 0, "N_B": 0, "N_B2": 0, "N_AB": 0}
        for worker in self.Workforce:
            wv = worker.Worldview
            char = "2" if worker.Zealot else ''
            N["N_"+wv+char] += 1
        for k in N.keys():
            count = getattr(self, k)
            if count != N[k]: 
                raise ValueError("COUNT: ", count, " !=", N[k], "for Worldview: ", k)
            else: 
                continue 
        
        return   

    def get_statistics(self): 
        N = {"N_A": 0, "N_A2": 0, "N_B": 0, "N_B2": 0, "N_AB": 0}
        for worker in self.Workforce:
            wv = worker.Worldview
            char = "2" if worker.Zealot else ''
            N["N_"+wv+char] += 1
        
        n = {"n_A": N.get("N_A")/self.Org_size, "n_A2": N.get("N_A2")/self.Org_size, "n_B": N.get("N_B")/self.Org_size,\
                "n_B2": N.get("N_B2")/self.Org_size, "n_AB": N.get("N_AB")/self.Org_size}
        
        #print("n dict: ", n)
        #polarization = #n.get("n_AB")/
        polarization = (n.get("n_A") + n.get("n_A2") + n.get("n_B") + n.get("n_B2"))  

        return N, n, polarization


def main(): 
    #The purpose here is be able to run simulations from the command line 
    #Eventually, we should be able to automate many simulations with 
    #various parameters to explore how the system depends on them. 
    #For now, though, we just create a command line tool in order to 
    #run sims easily and check how things are working ... 
    
    #plotting vars 
    polarization_vals = []
    fractional_A = []
    fractional_A_Zealots = []
    fractional_B = []
    fractional_B_Zealots  = []
    fractional_Moderates = [] 
    
    #using default mode 
    Org = Organization() #initialize organization
   
    #using non default settings
    Org.Mode = "ASR"
    Org.Org_size = 100 
    Org.HP_size = 500 
    Org.Config = [.1, .1, .8] #initial fractional rep in org
    Org.A_config = .5 
    Org.B_config = .7
    Org.H_config = [.2, .2, .6] #fractional rep in hiring pool  
    Org.A_HPconfig = .1 
    Org.B_HPconfig = .8 
    
    Org.populate_org() #population organization with individuals
    Org.Leader.Worldview = "B" #setting leader's worldview
    Org.populate_HP() #populated hiring pool with individuals 
    

    initial_workforce = Org.Workforce
    initial_worldviews = []
    for worker in initial_workforce:
        if worker.Zealot == True: 
            initial_worldviews.append(worker.Worldview + " Zealot")
        else:
            initial_worldviews.append(worker.Worldview)

    initial_n = Org.get_statistics()[1]
    initial_N = Org.get_statistics()[0]
    initial_polarization = Org.get_statistics()[2]
    
    #print("initial n: ", initial_n)
    #checking configuration before evolution
    print("INITIAL STATE: ")
    print("Hiring Mode: ", Org.Mode)
    print("Fractional Total A: ", initial_n.get("n_A") + initial_n.get("n_A2"))
    print("Fractional A: ", initial_n.get("n_A")) 
    print("Fractional A Zealots: ", initial_n.get("n_A2"))
    print("Total A: ", initial_N.get("N_A") + initial_N.get("N_A2")) 
    print("Fractional Total B: ", initial_n.get("n_B") + initial_n.get("n_B2")) 
    print("Fractional B: ", initial_n.get("n_B"))
    print("Fractional B Zealots: ", initial_n.get("n_B2"))
    print("Total B: ", initial_N.get("N_B") + initial_N.get("N_B2")) 
    print("Fractional Moderates :", initial_n.get("n_AB"))
    print("Total Moderates: ", initial_N.get("N_AB")) 
    print("Leader :", Org.Leader.Worldview)
    print("Polarization: ", initial_polarization) 
    
    #evolve model with 100 interactions
    for interaction in range(1000):
        
        N = Org.get_statistics()[0]
        n = Org.get_statistics()[1]
        polarization = Org.get_statistics()[2]

        polarization_vals.append(polarization)
        fractional_A.append(n.get("n_A"))
        fractional_A_Zealots.append(n.get("n_A2"))
        fractional_B.append(n.get("n_B")) 
        fractional_B_Zealots.append(n.get("n_B2"))
        fractional_Moderates.append(n.get("n_AB")) 
        
        if N.get("N_A") + N.get("N_A2") + N.get("N_B") + N.get("N_B2") + N.get("N_AB") != Org.Org_size \
                or N.get("N_A") < 0 or N.get("N_A2") < 0 or N.get("N_B") < 0 or N.get("N_B2") < 0 \
                or N.get("N_AB") < 0:
            print("Something isn't adding up!")
            break 

        #anyone who wants to resign can resign 
        for employee in Org.Workforce:
            #sometimes resignations are taking place without a hiring. This means 
            #that open_position == -1. Why is this happening? 
            open_position = employee.resign()
            if open_position != -1: 
                Org.hire(open_position)
        
        #interaction 
        #print("INTERACTION: ", interaction)
        Org.interact()

        #hiring and firing every 10 interactions 
        if Org.Num_interactions % 5 == 0:
            pos_to_fill = Org.fire() 
            Org.hire(pos_to_fill)
    
    final_workforce = Org.Workforce
    final_worldviews = []

    for worker in final_workforce:
        if worker.Zealot == True:
            final_worldviews.append(worker.Worldview + " Zealot")
        else:
            final_worldviews.append(worker.Worldview)

    print("INITIAL WORLDVIEWS: ", initial_worldviews)
    print("\nFINAL WORLDVIEWS: ", final_worldviews)
    
    final_N = Org.get_statistics()[0]
    final_n = Org.get_statistics()[1]
    final_polarization = Org.get_statistics()[2]

    #checking configuration after evolution
    print("\nFINAL STATE: ")
    print("Hiring Mode: ", Org.Mode)
    print("Fractional Total A: ", final_n.get("n_A") + final_n.get("n_A2"))
    print("Fractional A: ", final_n.get("n_A")) 
    print("Fractional A Zealots: ", final_n.get("n_A2"))
    print("Total A: ", final_N.get("N_A") + final_N.get("N_A2")) 
    print("Fractional Total B: ", final_n.get("n_B") + final_n.get("n_B2")) 
    print("Fractional B: ", final_n.get("n_B"))
    print("Fractional B Zealots: ", final_n.get("n_B2"))
    print("Total B: ", final_N.get("N_B") + final_N.get("N_B2")) 
    print("Fractional Moderates :", final_n.get("n_AB"))
    print("Total Moderates: ", final_N.get("N_AB")) 
    print("Leader :", Org.Leader.Worldview)
    print("Polarization: ", final_polarization)


    txt = "Mode = " + str(Org.Mode) + "| Leader Worldview = " + Org.Leader.Worldview + "| Org Size = " +\
            str(Org.Org_size) + "| Initial Org Config = " + str(Org.Config) + "| Fraction of A Zealots = " + \
            str(Org.A_config) + "| Fraction of B Zealots = " + str(Org.B_config) + "| Hiring Pool Size = " + \
            str(Org.HP_size) + "| Initial HP Config = " + str(Org.H_config) + "| Fraction of HP A Zealots = " +\
            str(Org.A_HPconfig) + "| Fraction of HP B Zealots = " + str(Org.B_HPconfig)

    plt.plot(polarization_vals, label = "Polarization")
    plt.plot(fractional_A, label = "A")
    plt.plot(fractional_A_Zealots, label = "A Zealots")
    plt.plot(fractional_B, label = "B")
    plt.plot(fractional_B_Zealots, label = "B Zealots")
    plt.plot(fractional_Moderates, label = "Moderates")
    plt.title("Ideological Configuration of Organization Over Time") 
    plt.xlabel("Number of Interactions")
    plt.ylabel("Fractional Representation in the Organization")
    plt.legend()
    plt.text(.5, -0.2, txt, horizontalalignment = "center") 
    #plt.legend()
    plt.show()
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
diversity within the organization. This means that we need a way to measure the polarization in the organization. 
If the polarization is above a certain threshold, then ASR moves from hiring in a default behavior to counter-acting
the polarization by hiring individuals that will move the configuration of the organization towards a uniform 
distribution. The key questions here are: 
    1. How will polarization be measured
    2. What threshold must be exceeded in order for ASR mode to counteract the polarization 
''' 


