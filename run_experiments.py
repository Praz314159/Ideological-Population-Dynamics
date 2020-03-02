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
from Organization_Model import Individual
from Organization_Model import Organization 
import matplotlib.pyplot as plt
import argparse 

#this is a normal simulation that only looks at n_A, n_A', n_AB, n_B, n_B' 
def run_simulation( ):
    pass 

#mainly SR and ASR modes 
def test_hiring_effort(): 

def main(): 
    #The purpose here is be able to run simulations from the command line 
    #Eventually, we should be able to automate many simulations with 
    #various parameters to explore how the system depends on them. 
    #For now, though, we just create a command line tool in order to 
    #run sims easily and check how things are working ... 
    
    parser = argparse.ArgumentParser() 
    hiring_mode = parser.mutually_exclusive_group() 
    hiring_mode.add_argument("-d", "--default", nargs = 0, help = "This is the default hiring mode.\
            When in this mode, the leader of the organization himself has no bias. However, because \
            he has no hiring bias, he selects for whatever bias may be intrisic to the hiring pool.")
    hiring_mode.add_argument("-sr", "--replication", nargs = 0, help = "This is the self-replication \
            hiring mode. When in this mode, the leader is biased towards hiring candidates with the \
            same worldview as him.") 
    hiring_mode.add_argument("-asr", "--anti_replication", nargs = 0, help = "This is the anti \
            self-replication hiring mode. When in this mode, no matter what the worldview of the leader \
            is, he attempts to maintain an ideologically diverse, non-polarized organization. This may \
            require him to hire against his worldview.")

    #we distinguish between parameters that should remain constant and those that we are interested
    #to get results from. The parameters that should remain constant (e.g, Org_Size) will be entered 
    #from input() rather than nargs

    Org.Org_size = input("Organization Size: " ) 
    Org.HP_size = input("Hiring Pool Size:  ") 
    THOM_distribution = input("THOM distribution: ") 
    TOPP_distribution = input("TOPP distribution: ") 
    







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
    for interaction in range(100):
        
        N = Org.get_statistics()[0]
        n = Org.get_statistics()[1]
        polarization = Org.get_statistics()[2]

        polarization_vals.append(polarization)
        fractional_A.append(n.get("n_A"))
        fractional_A_Zealots.append(n.get("n_A2"))
        fractional_B.append(n.get("n_B")) 
        fractional_B_Zealots.append(n.get("n_B2"))
        fractional_Moderates.append(n.get("n_AB")) 
        
        #anyone who wants to resign can resign 
        for employee in Org.Workforce:
            #sometimes resignations are taking place without a hiring. This means 
            #that open_position == -1. Why is this happening? 
            open_position = employee.resign()
            #print("POSITION RESIGNED: ", open_position) 
            if open_position != -1: 
                #print("POSITION RESIGNED: ", open_position) 
                Org.hire(open_position)
        
        #interaction 
        #print("INTERACTION: ", interaction)
        Org.interact()

        #hiring and firing every 10 interactions 
        if Org.Num_interactions % 5 == 0:
            pos_to_fill = Org.fire()
            #print("POSITION FIRED: ", pos_to_fill)
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
    #plt.text(0, -0.2, txt) 
    #plt.legend()
    plt.show()

if __name__ == "__main__": 
    main() 


