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

Model Functionality:  

 1. We have the following general rules: 
 A,A' |  B  |  AB
 A,A' |  AB |  B
 B    |  A  |  AB
 B    |  AB |  B

 2. Each individual has 2 threshold values
    1. TOPP --> this is the percentage of the organization that is of the opposite ideology of the individual at 
                which the individual resigns. TOPP is a measure of an individual's tolerance for being in the
                minority. 
    2. THOM --> this is the percentage of the organization that is of the same ideology of the individual at which
                the individual resigns. THOM is a measure of an individual's absolute tolerance for ideological 
                homogeneity 
    Normally, THOM >= TOPP. We make this reasonable simplifying assumption 

3. Any organization will have a natural steady turn over rate. We assume that individuals won't be fired for 
  ideological reasons unless the leader is a zealot. In the normal case, once an individual leaves the organization
  (incompetence, surpassed threshold), they are replaced by someone from the hiring pool. Here are some factors to 
  consider: 
    1. The HP might be ideologically biased --> note that unbiased hring (D mode) will select for this bias 
    2. If in SR mode, then bias of leader compounds the HP bias 
    3. If in ASR mode, then bias of leader will counteract HP bias 

4. We have a global scaling of probabilities with which A --> A' and B --> B' that is based on the % of the 
   organization that is either A or B. The idea here is that the more homogenous the organization, the less 
   of a social cost there is for being a zealt; in fact, one may even be able to accrue social capital by 
   becoming a zealot. 
    1. Bias = <B_1, B_2, .... ,B_n> <==> Probs = <P_1, P_2, ... ,P_n>
    2. This type of switch will only occur when the speaker is a zealot and the listener is a non-zealot with 
       the same worldview 

''' 
#Globals --> these should all be inputs 
ORG_SIZE = 1000 #number of individuals in organization 
ORG_CONFIG = {"B":.2, "B'":.2,"AB":.2,"A":.2,"A'":.2} #fractional representation of individual types in organization
ORG_MODE = "D" 
TURNOVER_RATE = .01 #natural turnover rate in the organization per epoch 

HP_SIZE = 1000 #number of individuals in hiring pool 
HP_CONFIG = {"B":.2, "B'":.2,"AB":.2,"A":.2,"A'":.2} #fractional representation of individual types in HP

class Individual: 
    def __init__(self):
        Worldview = 'A' #ideology of the individual 
        Zealot = False #boolean indicating if the the individual is a zealot or not 
        Leader = False #boolean indicating if the individual is a leader in the organization (may have multiple
                 #leaders) and thus has hiring power  
        TOPP = .5 #percentage of org of opp ideology at which individual resigns 
        THOM - .5 #percentage of org that is same ideology at which individual resigns 
        
    def speak(self, speaker): 
        pass 

    def listen(self, speaker): 
        pass 
    
    #think about what other functionality I might want to give individuals 

class Organization: 
    def __init__(self): 
        Size = ORG_SIZE 
        Config = ORG_CONFIG 
        Mode = ORG_MODE 
        F = TURNOVER_RATE 

    def interact(self, individual_1, individual_2): 
        pass 

    def hire(self, leader): 
        pass 

    def fire(self): 
        pass 


'''
TO DO: 
    1. Think more carefully about methods of Individual and Organization. The ones included now are preliminary.
    2. Code the actual behavior of the model --> how does the model evolve? EPOCHs? 
''' 


