'''
This is a command line tool to run tests using the organization ideological population dynamics model.
The variables that should be controllable with this testing tool are: 
    1. num epochs 
    2. initial org size, configuration 
    3. hiring pool size, configuration 
    4. num candidates during hiring 
    5. THOM, TOPP probability distributions 
    6. 
    7.
    8.
    9.
    10.
'''
from Organization_model import Individual
from Organization_model import Organization 

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
    Org.Org_size = 1000 
    Org.HP_size = 5000 
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
    pass 

if __name__ == "__main__": 
    main() 


