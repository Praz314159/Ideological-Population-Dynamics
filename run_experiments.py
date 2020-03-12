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
def run_simulation(Org, epochs):
    
    #plotting vars 
    polarization_vals = []
    fractional_A = []
    fractional_A_Zealots = []
    fractional_B = []
    fractional_B_Zealots  = []
    fractional_Moderates = [] 

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
    for interaction in range(epochs):
        
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
        if Org.num_interactions % 5 == 0:
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

    return polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
            fractional_Moderates 
    pass 

#mainly SR and ASR modes

def plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
        fractional_Moderates):

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
    plt.show()
    pass 

def plot_all(D, SR, ASR):
    
    fig, axs = plt.subplots(3) 
    fig.suptitle("D, SR, ASR") 
    axs[0].plot(D[0], label = "Polarization") 
    axs[0].plot(D[1], label = "A")
    axs[0].plot(D[2], label = "A Zealots") 
    axs[0].plot(D[3], label = "B")
    axs[0].plot(D[4], label = "B Zealots") 
    axs[0].plot(D[5], label = "Moderates") 
    #axs[0].set(xlabel = "Number of Interactions", ylabel = "Fractional Representation in the Organization")
    axs[0].legend()
    
    axs[1].plot(SR[0], label = "Polarization") 
    axs[1].plot(SR[1], label = "A")
    axs[1].plot(SR[2], label = "A Zealots") 
    axs[1].plot(SR[3], label = "B")
    axs[1].plot(SR[4], label = "B Zealots") 
    axs[1].plot(SR[5],label = "Moderates") 
    axs[1].set(ylabel = "Fractional Representation in the Organization")
    #axs[1].legend()
    
    axs[2].plot(ASR[0], label = "Polarization") 
    axs[2].plot(ASR[1], label = "A")
    axs[2].plot(ASR[2], label = "A Zealots") 
    axs[2].plot(ASR[3], label = "B")
    axs[2].plot(ASR[4], label = "B Zealots") 
    axs[2].plot(ASR[5], label = "Moderates") 
    axs[2].set(xlabel = "Number of Interactions")
    #axs[2].legend()   
    
    plt.show()
    pass 

def set_initial_conditions(Org_size, HP_size, config_A, config_B, config_AB, A_config, B_config,\
        Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview): 

    #initialize organization
    Org = Organization() 
    
    #set parameters to user input 
    Org.Org_size = Org_size
    Org.HP_size = HP_size 
    Org.Config = [config_A, config_B, config_AB] 
    Org.A_config = A_config 
    Org.B_config = B_config
    Org.H_config = [Hconfig_A, Hconfig_B, Hconfig_AB]  
    Org.A_HPconfig = A_HPconfig
    Org.B_HPconfig = B_HPconfig

    Org.populate_org()
    #populate hiring pool 
    Org.populate_HP() 
    
    #use custom leader worldview or random
    if Leader_worldview != "No Preference":
        Org.Leader.Worldview = Leader_worldview
    else:
        pass
    
    #return initialized organization
    return Org

def test_hiring_effort():
    pass


def main(): 
    #The purpose here is be able to run simulations from the command line 
    #Eventually, we should be able to automate many simulations with 
    #various parameters to explore how the system depends on them. 
    #For now, though, we just create a command line tool in order to 
    #run sims easily and check how things are working ... 
    
    parser = argparse.ArgumentParser() 
    hiring_mode = parser.add_mutually_exclusive_group(required = True) 
    hiring_mode.add_argument("-d", "--default", nargs = 1, type = int, help = "This is the default hiring mode.\
            When in this mode, the leader of the organization himself has no bias. However, because \
            he has no hiring bias, he selects for whatever bias may be intrisic to the hiring pool.")
    hiring_mode.add_argument("-sr", "--replication", nargs = 1, type = int, help = "This is the self-replication \
            hiring mode. When in this mode, the leader is biased towards hiring candidates with the \
            same worldview as him.") 
    hiring_mode.add_argument("-asr", "--anti_replication", nargs = 1, type = int, help = "This is the anti \
            self-replication hiring mode. When in this mode, no matter what the worldview of the leader \
            is, he attempts to maintain an ideologically diverse, non-polarized organization. This may \
            require him to hire against his worldview.")
    hiring_mode.add_argument("-all", "--all", nargs = 1, type = int, help = "this is the flag that allows \
            you to run the experiment on all modes and plot them side by side in order to compare their \
            behavior.")

    args = parser.parse_args() 
    
    #Now we want to ask the user what he'd like to set each of the main parameters too 
    #in order to run the experiment: size, HP size, Config, A config, B config, HP A config,
    #HP B config
    Org_size = int(input("Number of individuals in organization: "))  
    HP_size = int(input("Hiring pool size: ")) 
    config_A = float(input("Fractional woldview configuration A: "))
    config_B = float(input("Fractional woldview configuration B: ")) 
    config_AB = float(input("Fractional worldview configuration AB: "))  
    A_config = float(input("Fraction of A's that are zealots: "))  
    B_config = float(input("Fraction of B's that are zealots: ")) 
    Hconfig_A = float(input("Fractional woldview HP configuration A: "))
    Hconfig_B = float(input("Fractional woldview HP configuration B: ")) 
    Hconfig_AB = float(input("Fractional worldview HP configuration AB: "))  
    A_HPconfig = float(input("Fraction of hiring pools A's that are zealots: "))
    B_HPconfig = float(input("Fraction of hiring pool B's that are zealots: "))
    Leader_worldview = input("Worldview of leader: ") 
   
    if args.default:
        #set organization params 
        Org = set_initial_conditions(Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
        Org.Mode = "D"
        epochs = args.default[0]
        polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
                fractional_Moderates = run_simulation(Org, epochs)
        plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B,\
                fractional_B_Zealots, fractional_Moderates)
        pass 
    elif args.replication: 
        Org = set_initial_conditions(Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
        Org.Mode = "SR" 
        epochs = args.default[0]
        run_simulation(Org, epochs) 
        polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
                fractional_Moderates = run_simulation(Org, epochs)
        plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B,\
                fractional_B_Zealots, fractional_Moderates)
        pass 
    elif args.anti_replication:
        Org = set_initial_conditions(Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
        Org.Mode = "ASR" 
        epochs = args.default[0] 
        run_simulation(Org, epochs) 
        polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
                fractional_Moderates = run_simulation(Org, epochs)
        plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B,\
                fractional_B_Zealots, fractional_Moderates)
        pass
    elif args.all: 
        Modes = ["D", "SR", "ASR"]
        epochs = args.all[0]
        D = []
        SR = []
        ASR = []
        for mode in Modes:
            Org = set_initial_conditions(Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                    B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
            Org.Mode = mode
            if mode == "D": 
                D = run_simulation(Org, epochs)
            elif mode == "SR": 
                SR = run_simulation(Org, epochs) 
            elif mode == "ASR": 
                ASR = run_simulation(Org, epochs) 
        
        plot_all(D, SR, ASR)

if __name__ == "__main__": 
    main() 


