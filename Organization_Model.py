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
   of a social cost there is for being a zealot; in fact, one may even be able to accrue social capital by 
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
        Worldview = "A" #ideology of the individual 
        Zealot = False #boolean indicating if the the individual is a zealot or not 
        Leader = False #boolean indicating if the individual is a leader in the organization (may have multiple
                 #leaders) and thus has hiring power  
        TOPP = .5 #percentage of org of opp ideology at which individual resigns 
        THOM - .5 #percentage of org that is same ideology at which individual resigns 
        is_listener = False 

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
        if (speaker.Worldview == "A" and lister.Worldview == "B") or (speaker.Worldview == "B" and lister.Worldview == "A"): 
            listener.Worldview = "AB" 
        elif (speaker.Worldview == "A'" and listener.Worldview == "B") or ((speaker.Worldview == "A" or speaker.Worldview == "A'") \
                and listener.Worldview == "AB"):
            #preference falsification accounted for 
            listener.Worldview = "A"
        elif (speaker.Worldview == "B'" and listener.Worldview == "A") or ((speaker.Worldview == "B" or speaker.Worldview == "B'") \
                and listener.Worldview == "AB"):
            #preference falsification accounted for 
            listener.Woldview = "B" 
        elif speaker.Worldview == "A'" and listener.Worldview == "A": 
            pass 
        elif speaker.Worldview == "B'" and listener.Worldview == "B": 
            pass 

    #think about what other functionality I might want to give individuals 

class Organization: 
    def __init__(self): 
        Size = ORG_SIZE 
        Config = ORG_CONFIG 
        Mode = ORG_MODE 
        F = TURNOVER_RATE 
    
    def initialize(self): 


    def interact(self, individual_1, individual_2):
        #this function should randomly select two individuals to interact 
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


