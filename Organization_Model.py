'''
Organizational population dynamics model in python 
This is a python model meant to demonstrate how hiring can be used as a mechanism to mitigate 
ideological homogeneity within an organization and, conversely, how it can be used as a mechanism
to create an organization full of zealots. TY SEEDS OF PEACE!!!! 
''' 
import math 
import numpy as np
import random 
import argparse 
from matplotlib import pyplot as plt 
import statistics 

class Individual: 
    def __init__(self):
        #Personal Parameters
        self.Worldview = None #ideology of the individual 
        self.Zealot = False #boolean indicating if the the individual is a zealot or not 
        self.Leader = False #boolean indicating if the individual is a leader in the organization (may have multiple
                      #leaders) and thus has hiring power  
        self.TOPP = .5 #percentage of org of opp ideology at which individual resigns 
        self.Zealot_resistance_probabilities =  [.01, .03, .05, .07, .1, .135, .17, .205, .4, .45, .51, .58, .66, .75,\
                .85,.95, .96, .97, .98, .99]

        #Org parameters 
        self.Organization = None #organization that individual belongs to  
        self.Org_pos = 0 #index in organization workforce list 
        
    def resign(self): 
        empty_pos = -1
        n = self.Organization.get_statistics()[1] 
        if self.Worldview == "A":
            if 1- (n.get("n_A") + n.get("n_A2")) > self.TOPP:
                empty_pos = self.Organization.accept_resignation(self) 
        elif self.Worldview == "AB":
            if 1-n.get("n_AB") > self.TOPP:
                empty_pos = self.Organization.accept_resignation(self) 
        elif self.Worldview == "B": 
            if 1-(n.get("n_B") + n.get("n_B2")) > self.TOPP:
                empty_pos = self.Organization.accept_resignation(self)
       
        return empty_pos 

    def listen(self, speaker):
        preference_falsification = False 
        n = self.Organization.get_statistics()[1]
        N = self.Organization.get_statistics()[0]
        '''
        if (speaker.Worldview == "A" and speaker.Zealot == False and self.Worldview == "B" and self.Zealot == False ) \
                or (speaker.Worldview == "B" and speaker.Zealot == False and self.Worldview == "A" and self.Zealot ==\
                False): 
                    self.Worldview = "AB" 

        elif ((speaker.Worldview == "A" and speaker.Zealot == True) and ((self.Worldview == "B" or self.Worldview ==\
                "AB") and self.Zealot == False)) or (speaker.Worldview == "A" and speaker.Zealot == False and\
                self.Worldview == "AB" and self.Zealot == False):
                    self.Worldview = "A"

        elif ((speaker.Worldview == "B" and speaker.Zealot == True) and ((self.Worldview == "A" or self.Worldview ==\
                "AB") and self.Zealot == False)) or (speaker.Worldview == "B" and speaker.Zealot == False and\
                self.Worldview == "AB" and self.Zealot == False): 
                    self.Worldview == "B"
        ''' 
        if (speaker.Worldview == "A" and speaker.Zealot == False) and (self.Worldview == "AB"): 
            self.Worldview = "A" 
        elif (speaker.Worldview == "A" and speaker.Zealot == False) and (self.Worldview == "B" and self.Zealot == False): 
            self.Worldview = "AB"
        elif (speaker.Worldview == "B" and speaker.Zealot == False) and (self.Worldview == "A" and self.Zealot == False): 
            self.Worldview = "AB"
        elif (speaker.Worldview == "B" and speaker.Zealot == False) and (self.Worldview == "AB"): 
            self.Worldview == "B"
        elif (speaker.Worldview == "B" and speaker.Zealot == True) and (self.Worldview == "A" and self.Zealot == False): 
            self.Worldview = "B"
            preference_falsification = True 
        elif (speaker.Worldview == "B" and speaker.Zealot == True) and (self.Worldview == "AB"): 
            self.Worldview = "B"
        elif (speaker.Worldview == "A" and speaker.Zealot == True) and (self.Worldview == "AB"): 
            self.Worldview = "A" 
        elif (speaker.Worldview == "A" and speaker.Zealot == True) and (self.Worldview == "B" and self.Zealot == False): 
            self.Worldview = "A" 
            preference_falsification = True 
        elif (speaker.Worldview == "A" and speaker.Zealot == True) and (self.Worldview == "A" and self.Zealot == False):
            #the key is that we have access to the global state of the organization, which means that we 
            #do indeed know how homogenous the organization is in A, for example. 
            #bucket = math.floor((n.get("n_A") + n.get("n_A2"))/.05) 
            if math.floor((n.get("n_A") + n.get("n_A2"))/.05) == 0: 
                bucket = 0
            else: 
                bucket = math.floor((n.get("n_A") + n.get("n_A2"))/.05) - 1  
    
            #getting likelhood that A --> A' 
            prob_switch = self.Zealot_resistance_probabilities[bucket]

            #A --> A' with assigned probability 
            if random.random() < prob_switch:
                self.Zealot == True 
        elif (speaker.Worldview == "B" and speaker.Zealot == True) and (self.Worldview == "B" and self.Zealot == False):
            if math.floor((n.get("n_B") + n.get("n_B2"))/.05) == 0: 
                bucket = 0
            else: 
                bucket = math.floor((n.get("n_B") + n.get("n_B2"))/.05) - 1
           
            #getting likelhood that B --> B' 
            prob_switch = self.Zealot_resistance_probabilities[bucket]

            #B --> B' with assigned probability 
            if random.random() < prob_switch:
                self.Zealot == True
        else: 
            pass 

        return preference_falsification

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
        self.Workforce = []
        self.HP = []
        self.Leader = None 
        self.num_interactions = 0
      
    def populate_org(self):
        #Populate the organization with individuals 

        for i in range(self.Org_size): 
            self.Workforce.append(Individual()) #creates employee
            self.Workforce[i].Org_pos = i #sets position of employee in organization 
            self.Workforce[i].Organization = self #sets organization of employee to organization 
            
            #draw TOPP and THOM from normal distribution, but set THOM at least as high as TOPP 
            self.Workforce[i].TOPP = np.random.normal(0.5, .1) #choose normal distribution 
           
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
            self.HP[i].TOPP = np.random.uniform(0.5,1)
            #self.HP[i].THOM = np.random.uniform(self.HP[i].TOPP,1)

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
        
        print("Speaker Worldview: ", speaker.Worldview)
        print("Speaker Zealot: ", speaker.Zealot) 
        print("Initial Listener Worldview: ", listener.Worldview)
        print("Listener Zealot: ", listener.Zealot)
        
        preference_falsification = listener.listen(speaker)
        print("Final Listener Worldview: ", listener.Worldview)
        print("Preference Falsification: ", preference_falsification) 
        self.num_interactions += 1          
        return 
    
    #no screening for tolerance
    def hire_with_probability_no_screen(self, new_hire, position, probability):
        hired = False
        if random.random() < probability: 
            hired = True 
            self.Workforce[position] = new_hire 
            new_hire.Org_pos = position 
            new_hire.Organization = self 
            
            print("\nNEW HIRE") 
            print("Position: ", position)
            print("Worldview: ", new_hire.Worldview) 

        return hired 

    #screening for tolerance 
    def hire_with_probability(self, new_hire, position, probability):
        hired = False 
        if random.random() < probability:
            n = self.get_statistics()[1]
            # only hire if candidate can handle the current org state
            # the problem here is that in default mode, the probability that random candidate
            # from hiring pool will be hired is 1. But, what happens if they can't handle the 
            # org state? Then we have to look for another candidate to hire ... how is this 
            # dealt with? For now, when we are in default mode, we use hire_with_no_screen 
            if new_hire.Worldview == "A":     
                if 1 - (n.get("n_A") + n.get("n_A2")) <= new_hire.TOPP: 
                    hired = True 
                    self.Workforce[position] = new_hire 
                    new_hire.Org_pos = position
                    new_hire.Organization = self
                    print("\nNEW HIRE") 
                    print("Position: ", position)
                    print("Worldview: ", new_hire.Worldview) 

            elif new_hire.Worldview == "AB":
                if 1 - n.get("n_AB") <= new_hire.TOPP:
                    hired = True 
                    self.Workforce[position] = new_hire 
                    new_hire.Org_pos = position
                    new_hire.Organization = self
                    print("\nNEW HIRE") 
                    print("Position: ", position)
                    print("Worldview: ", new_hire.Worldview) 

            elif new_hire.Worldview == "B": 
                if 1 - (n.get("n_B") + n.get("n_B2")) <= new_hire.TOPP: 
                    hired = True 
                    self.Workforce[position] = new_hire 
                    new_hire.Org_pos = position
                    new_hire.Organization = self
                    print("\nNEW HIRE") 
                    print("Position: ", position)
                    print("Worldview: ", new_hire.Worldview) 

        return hired
        
    def fire(self): 
        empty_pos = random.randint(1, self.Org_size-1)
        new_fire = self.Workforce[empty_pos]
        
        print("\nFIRING") 
        print("Position: ", empty_pos) 
        print("Worldview: ", new_fire.Worldview) 
        return empty_pos 
   
    def accept_resignation(self, new_resignation): 
        empty_pos = new_resignation.Org_pos 
        
        print("\nRESIGNATION")
        print("Position: ", empty_pos) 
        print("Worldview: ", new_resignation.Worldview) 
        return empty_pos

    def hire(self, empty_pos):
        #Default hiring mode: selecting for pre-existing bias in hiring pool 
        if self.Mode == "D":
            new_hire = self.HP[random.randint(0, self.HP_size-1)]
            self.hire_with_probability(new_hire, empty_pos, 1) 

        #Self Replication hiring mode: selects for bias of the leader 
        elif self.Mode == "SR":
            #print("\nENTERING SR MODE")
            #possible we keep interviewing until we find someone ... 
            for interview in range(10): 
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
                        if self.hire_with_probability(candidate, empty_pos, .3) == True:
                            break
                        else:
                            continue
                    
                # [(.05, .1), .3, .75]
                elif self.Leader.Worldview == "B":
                    if candidate.Worldview == "A": 
                        if candidate.Zealot == True:
                            if self.hire_with_probability(candidate, empty_pos, .05) == True:
                                break
                            else:
                                continue
                        else:
                            if self.hire_with_probability(candidate, empty_pos, .1) == True:
                                break
                            else:
                                continue
                    elif candidate.Worldview == "B":
                        if self.hire_with_probability(candidate, empty_pos, .75) == True:
                            break
                        else:
                            continue
                    elif candidate.Worldview == "AB":
                        if self.hire_with_probability(candidate, empty_pos, .3) == True:
                            break
                        else:
                            continue 
                        
                # [.3, .5, .3]
                elif self.Leader.Worldview == "AB":
                    if candidate.Worldview == "A":
                        if self.hire_with_probability(candidate, empty_pos, .3)  == True: 
                            break
                        else:
                            continue 
                    elif candidate.Worldview == "B":
                        if self.hire_with_probability(candidate, empty_pos, .3)  == True: 
                            break
                        else:
                            continue 
                    elif candidate.Worldview == "AB":
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
            for i in range(50): 
                candidates.append(self.HP[random.randint(0, self.HP_size-1)])
                if candidates[i].Worldview == "AB":
                    has_moderate = True 

            n = self.get_statistics()[1]
            N = self.get_statistics()[0]
            polarization = self.get_statistics()[2] 
            
            if polarization < .5:
                #if the polarization is tolerable, choose random 
                new_hire = self.HP[random.randint(0, self.HP_size-1)] 
                self.hire_with_probability(new_hire, empty_pos, 1) 
            else:
                if has_moderate == True:
                    for candidate in candidates:
                        if candidate.Worldview == "AB": 
                            self.hire_with_probability(candidate, empty_pos, 1) 
                            break
                        else:
                            pass
                else:
                    for candidate in candidates:
                        if n.get("n_A") + n.get("n_A2") > n.get("n_B") + n.get("n_B2") and candidate.Worldview == "B":
                            self.hire_with_probability(candidate, empty_pos, 1)
                            break 
                        elif n.get("n_A") + n.get("n_A2") < n.get("n_B") + n.get("n_B2") and candidate.Worldview == "A":
                            self.hire_with_probability(candidate, empty_pos, 1) 
                            break
                        elif n.get("n_A") + n.get("n_A2") == n.get("n_B") + n.get("n_B2"):
                            self.hire_with_probability(candidate, empty_pos, 1)
                            break 
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
        
        n_A = n.get("n_A") + n.get("n_A2")
        n_B = n.get("n_B") + n.get("n_B2") 
        n_AB = n.get("n_AB")
        
        #Zero checking 
        if n_B == 0: 
            alpha = 1000
        else: 
            alpha = abs(1 - (n_A/n_B)) 

        if n_AB == 0:
            beta = 1000 
            gamma = 1000 
        else: 
            beta = abs(1 - (n_A/n_AB)) 
            gamma = abs(1 - (n_B/n_AB))

        ratios = [alpha, beta, gamma] 
        mean_ratios = statistics.mean(ratios) 
        polarization = (2/math.pi)*np.arctan(mean_ratios)  
        TOPP = [worker.TOPP for worker in self.Workforce]
        Worldviews = [worker.Worldview for worker in self.Workforce]
        character = {Worldviews[i] + str(i): TOPP[i] for i in range(len(Worldviews))}

        return N, n, polarization, TOPP, character 
