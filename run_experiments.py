'''
This is a command line tool to run tests using the organization ideological population dynamics model.
The variables that should be controllable with this testing tool are: 
    1. num epochs 
    2. initial org size, configuration 
    3. hiring pool size, configuration 
    4. num candidates during hiring 
    5. TOPP probability distributions
'''
from Organization_Model import Individual
from Organization_Model import Organization 
from Organization_Topo_Model import Individual as Individual_Topo
from Organization_Topo_Model import Organization as Organization_Topo
import matplotlib.pyplot as plt 
import argparse 
import natural_cubic_spline as cs 
import numpy as np 
import sys 


def set_initial_conditions(topology, Org_size, HP_size, config_A, config_B, config_AB, A_config, B_config,\
        Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview): 

    #initialize organization
    if topology == "empty_topology":
        Org = Organization() 
    elif topology == "topology": 
        Org = Organization_Topo() 
    
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
    
    initial_N, initial_n, initial_polarization, initial_TOPP, initial_character = Org.get_statistics()
    #checking configuration before evolution
    print("\nINITIAL STATE: ")
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
            open_position = employee.resign() #print worldview resigning, print position of resignee
            #print("POSITION RESIGNED: ", open_position) 
            if open_position != -1: 
                #print("POSITION RESIGNED: ", open_position) 
                Org.hire(open_position) #print worldview of hire, print position of hiree 
        
        #interaction 
        print("\nINTERACTION: ", interaction) 
        Org.interact() #print the speaker, print the listener pre-interaction, print the listener post-interaction
        
        #Firing 
        if Org.num_interactions % 5 == 0:
            pos_to_fill = Org.fire()
            #print("POSITION FaIRED: ", pos_to_fill)
            Org.hire(pos_to_fill)
 
    final_workforce = Org.Workforce
    final_worldviews = []
    for worker in final_workforce:
        if worker.Zealot == True:
            final_worldviews.append(worker.Worldview + " Zealot")
        else:
            final_worldviews.append(worker.Worldview)
    
    final_N, final_n, final_polarization, final_TOPP, final_character = Org.get_statistics()
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

    print("\nINITIAL WORLDVIEWS: ", initial_worldviews)
    print("\nFINAL WORLDVIEWS: ", final_worldviews)
    
    return polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
            fractional_Moderates, initial_TOPP, final_TOPP, initial_character, final_character 

#mainly SR and ASR modes

def plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
        fractional_Moderates):
    
    #getting cubic spline interpolatitions -- pre-deciding here # of knots 

    # we want to smooth the each of the plots of fractional representations, then we want to 
    # locate specific key points: 1st derivative max, 2nd derivative max, 2nd derivative min 
    # 2nd derivative max corresponds roughly to the tipping point of ideological takeover, 2nd derivative
    # min corresponds roughly to the point at which the takeover is complete. The time between the two 
    # indicates how long the "noticeable radicalization" period lasted, time between start and 2nd 
    #derivative max indicates how long "invisible radicaliZation" period lasted, etc. 

    x = np.asarray([i for i in range(len(polarization_vals))])
    estimations = []
    #polarization_vals
    model_50_P = cs.get_natural_cubic_spline_model(x, np.asarray(polarization_vals), minval = min(x), \
            maxval = max(x), n_knots = 50)
    est_50_P = model_50_P.predict(x)
    estimations.append(est_50_P) 

    #fractional_A
    model_50_A =  cs.get_natural_cubic_spline_model(x, fractional_A,\
            minval = min(x), maxval = max(x), n_knots = 50)
    est_50_A = model_50_A.predict(x)
    estimations.append(est_50_A) 

    #fractional_A_Zealots
    model_50_AZ =  cs.get_natural_cubic_spline_model(x, fractional_A_Zealots,\
            minval = min(x), maxval = max(x), n_knots = 50)
    est_50_AZ = model_50_AZ.predict(x)
    estimations.append(est_50_AZ) 

    #fractional_B
    model_50_B =  cs.get_natural_cubic_spline_model(x, fractional_B,\
            minval = min(x), maxval = max(x), n_knots = 50)
    est_50_B = model_50_B.predict(x)
    estimations.append(est_50_B)

    #fractional_B_Zealot
    model_50_BZ =  cs.get_natural_cubic_spline_model(x, fractional_B_Zealots,\
            minval = min(x), maxval = max(x), n_knots = 50)
    est_50_BZ = model_50_BZ.predict(x)
    estimations.append(est_50_BZ)

    #fractional_Moderates 
    model_50_M =  cs.get_natural_cubic_spline_model(x, fractional_Moderates,\
            minval = min(x), maxval = max(x), n_knots = 50)
    est_50_M = model_50_M.predict(x)
    estimations.append(est_50_M) 
    
    #polarization critical values 
    der_1 = np.gradient(est_50_P)
    der_2 = np.gradient(der_1) 
    max_der_1 = der_1.max() 
    max_der_1_index = np.argmax(der_1) 
    max_der_2 = der_2.max() 
    max_der_2_index = np.argmax(der_2) 
    min_der_2 = der_2.min() 
    min_der_2_index = np.argmin(der_2)
    x_critical = [max_der_2_index, min_der_2_index]
    y_critical = [polarization_vals[max_der_2_index], polarization_vals[min_der_2_index]]

    '''
    critical_vals = []
    for est in estimations: 
        #first derivative 
        der_1 = np.gradient(est)
        der_2 = np.gradient(der_1) 
        max_der_1 = der_1.max() 
        max_der_1_index = np.argmax(der_1) 
        max_der_2 = der_2.max() 
        max_der_2_index = np.argmax(der_2) 
        min_der_2 = der_2.min() 
        min_der_2_index = der_2.argmin(der_2)
        critical_vals.append((max_der_1_index, max_der_2_index, min_der_2_index))
    '''  

    #plotting 
    #plt.plot(polarization_vals, 'b--', label = "Polarization")
    plt.plot(est_50_P, 'b', label = "P Interpolation")
    #plt.plot(der_1, "b+") 
    #plt.plot(der_2, "b*")
    plt.plot(x_critical, y_critical, 'b+', markersize = 20)
    #plt.plot(fractional_A, color = 'r', label = "A")
    plt.plot(est_50_A, 'r', label = "A Interpolation") 
    #plt.plot(fractional_A_Zealots, 'g', label = "A Zealots")
    plt.plot(est_50_AZ, 'g', label = "AZ Interpolation") 
    #plt.plot(fractional_B, color = 'm', label = "B")
    plt.plot(est_50_B, 'm', label = "B Interpolation") 
    #plt.plot(fractional_B_Zealots, color = "c", label = "B Zealots")
    plt.plot(est_50_BZ, 'c', label = "BZ Interpolation") 
    #plt.plot(fractional_Moderates, color = "k", label = "Moderates")
    plt.plot(est_50_M, 'k', label = "M Interpolation") 
    plt.title("Ideological Configuration of Organization Over Time") 
    plt.xlabel("Number of Interactions")
    plt.ylabel("Fractional Representation in the Organization")
    plt.legend()
    plt.show()
    pass 


def cubic_spline_smooth(x, y):

    # we want to smooth the each of the plots of fractional representations, then we want to 
    # locate specific key points: 1st derivative max, 2nd derivative max, 2nd derivative min 
    # 2nd derivative max corresponds roughly to the tipping point of ideological takeover, 2nd derivative
    # min corresponds roughly to the point at which the takeover is complete. The time between the two 
    # indicates how long the "noticeable radicalization" period lasted, time between start and 2nd 
    #derivative max indicates how long "invisible radicaliZation" period lasted, etc. 

    # The number of knots can be used to control the amount of smoothness
    model_6 = get_natural_cubic_spline_model(x, y, minval=min(x), maxval=max(x), n_knots=6)
    model_15 = get_natural_cubic_spline_model(x, y, minval=min(x), maxval=max(x), n_knots=15)
    y_est_6 = model_6.predict(x)
    y_est_15 = model_15.predict(x)


    plt.plot(x, y, ls='', marker='.', label='originals')
    plt.plot(x, y_est_6, marker='.', label='n_knots = 6')
    plt.plot(x, y_est_15, marker='.', label='n_knots = 15')
    plt.legend(); plt.show()
    pass 

def plot_all(D, SR, ASR):
    
    fig, axs = plt.subplots(4) 
    fig.suptitle("D, SR, ASR") 
    #axs[0].plot(D[0], label = "Polarization") 
    axs[0].plot(D[1], label = "A")
    axs[0].plot(D[2], label = "A Zealots") 
    axs[0].plot(D[3], label = "B")
    axs[0].plot(D[4], label = "B Zealots") 
    axs[0].plot(D[5], label = "Moderates") 
    #axs[0].set(xlabel = "Number of Interactions", ylabel = "Fractional Representation in the Organization")
    axs[0].legend()
    
    #axs[1].plot(SR[0], label = "Polarization") 
    axs[1].plot(SR[1], label = "A")
    axs[1].plot(SR[2], label = "A Zealots") 
    axs[1].plot(SR[3], label = "B")
    axs[1].plot(SR[4], label = "B Zealots") 
    axs[1].plot(SR[5], label = "Moderates") 
    axs[1].set(ylabel = "Fractional Representation in the Organization")
    #axs[1].legend()
    
    #axs[2].plot(ASR[0], label = "Polarization") 
    axs[2].plot(ASR[1], label = "A")
    axs[2].plot(ASR[2], label = "A Zealots") 
    axs[2].plot(ASR[3], label = "B")
    axs[2].plot(ASR[4], label = "B Zealots") 
    axs[2].plot(ASR[5], label = "Moderates") 
    #axs[2].set(xlabel = "Number of Interactions")
    #axs[2].legend()   
    
    axs[3].plot(D[0], label = "D Polarization")
    axs[3].plot(SR[0], label = "SR Polarization") 
    axs[3].plot(ASR[0], label = "ASR Polarization")
    axs[3].set(xlabel = "Number of Interactions") 
    axs[3].legend() 

    plt.show()
    pass 

def get_TOPP_dists(initial_workforce, final_workforce):  
    #look at this fucking list compression. Booyakasha. 
    initial_dist = [worker.TOPP for worker in initial_workforce]
    initial_worldview = [worker.Worldview for worker in initial_workforce]
    initial_character = {initial_worldview[i] + str(i) : initial_dist[i] for i in range(len(initial_dist))}
    
    final_dist = [worker.TOPP for worker in final_workforce]
    final_worldview = [worker.Worldview for worker in final_workforce]
    final_character = {final_worldview[i] + str(i) : final_dist[i] for i in range(len(final_dist))}
    
    #for some reason, initial_workforce is not changing to final_workforce 
    #
    if initial_workforce == final_workforce: 
        print("TOPP not changed")
        print("Initial Character: ", initial_character)
        print("\nFinal Character: ", final_character)
    else: 
        print("TOPP changed")
        changes = [final_dist[i] for i in range(len(final_dist)) if final_dist[i] != initial_dist[i]]

    return initial_dist, final_dist  

def plot_TOPP_dist(initial_TOPP, final_TOPP):
    #getting TOPP values before and after simulation 
    #Note that before should look normal 
    #initial_dist, final_dist = get_TOPP_dists(initial_workforce, final_workforce) 

    # plt.plot(1,1,1)
    plt.hist([initial_TOPP, final_TOPP], 100, label = ['initial', 'final'])#, facecolor = ['g','b'])
    #plt.hist(initial_dist, 100, density = True, label = 'initial')
    #plt.hist(final_dist, 100, density = True, label = 'final')
    plt.legend(loc = 'upper right') 
    plt.xlabel("TOPP")
    plt.ylabel("Number of Individuals") 
    plt.title("TOPP Distribution in Workforce") 
    
    plt.show() 
   
def plot_all_TOPP_dists(D, SR, ASR):   
    #getting information for all modes to plot 
    D_initial_TOPP = D[6]
    D_final_TOPP = D[7] 
    SR_initial_TOPP = SR[6]
    SR_final_TOPP = SR[7] 
    ASR_initial_TOPP = ASR[6] 
    ASR_final_TOPP = ASR[7] 

    #creating 3 subplots and immediately unpacking output data 
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharey=True) 
    fig.suptitle("TOPP Distribution in Workforce")
    
    #default plot  
    ax1.hist([D_initial_TOPP, D_final_TOPP], 100, density = True)#, facecolor = ['g','b']) 
    #SR plot 
    ax2.hist([SR_initial_TOPP, SR_final_TOPP], 100, density = True)#, facecolor = ['g','b']) 
    ax2.set(ylabel = "Number of Individuals")
    #ASR plot 
    ax3.hist([ASR_initial_TOPP, ASR_final_TOPP], 100, density = True)#, facecolor = ['g','b']) 
    ax3.set(xlabel = "TOPP") 
    plt.show() 

def test_hiring_effort():
    pass

def main(): 
    #The purpose here is be able to run simulations from the command line 
    #Eventually, we should be able to automate many simulations with 
    #various parameters to explore how the system depends on them. 
    #For now, though, we just create a command line tool in order to 
    #run sims easily and check how things are working ... 
    
    parser = argparse.ArgumentParser() 
    
    #this lets the user decide what type of topology he wants the organization to be endowed with 
    parser.add_argument("--type", default = "empty_topology", type = str, choices = ["empty_topology", "topology"], \
            required = True, help = "This is the network topology you'd like the organization to be endowed with") 

    #This argument tells the program what information to display (i.e, what experiment is being run)  
    parser.add_argument("--info", default = "Subpopulations", type = str, choices = ["TOPP", "Subpopulations"],\
            required = True, help = "This is the type of information you'd like to gather from the experiment.")
    
    hiring_mode = parser.add_mutually_exclusive_group(required = True) 
    hiring_mode.add_argument("-d", "--default", nargs = 1, type = int, help = "This is the default hiring mode.\
            When in this mode, the leader of the organization himself has no bias. However, because \
            he has no hiring bias, he selects for whatever bias may be intrisic to the hiring pool." )
    hiring_mode.add_argument("-sr", "--replication", nargs = 2, type = int, help = "This is the self-replication \
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
        #set initial conditions
        Org = set_initial_conditions(args.type, Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
        Org.Mode = "D"
        epochs = args.default[0]

        #run simulation 
        polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
                fractional_Moderates, initial_TOPP, final_TOPP, initial_character, final_character \
                = run_simulation(Org, epochs)
        
        ################# Monkey fix for polarization-epoch dict ###################### 
        polarization_dict = {}
        for i in range(len(polarization_vals)):
            polarization_dict.update({i: polarization_vals[i]})
        
        ############################################################################### 
        
        #get info 
        if args.info == "Subpopulations": #default 
            print(polarization_dict) 
            plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, \
                    fractional_B_Zealots, fractional_Moderates)
        elif args.info == "TOPP":
            print("INITIAL CHARACTER: ", initial_character) 
            print("\nFINAL CHARACTER: ", final_character) 
            plot_TOPP_dist(initial_TOPP, final_TOPP)
        pass 
    elif args.replication:
        #set org params 
        Org = set_initial_conditions(args.type, Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
        Org.Mode = "SR" 
        epochs = args.default[0] 
        
        #run simulation 
        polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
                fractional_Moderates, initial_workforce, final_workforce = run_simulation(Org, epochs)
        
        #get info 
        if args.info == "Subpopulations": #default 
            plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, \
                    fractional_B_Zealots, fractional_Moderates)
        elif args.info == "TOPP":
            plot_TOPP_dist(initial_workforce, final_workforce)
    
        pass 
    elif args.anti_replication:
        #set params 
        Org = set_initial_conditions(args.type, Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
        Org.Mode = "ASR" 
        epochs = args.default[0] 
        
        #run_simulation 
        polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, fractional_B_Zealots, \
                fractional_Moderates = run_simulation(Org, epochs)
        
        #get info 
        if args.info == "Subpopulations": #default 
            plot_single(polarization_vals, fractional_A, fractional_A_Zealots, fractional_B, \
                    fractional_B_Zealots, fractional_Moderates)
        elif args.info == "TOPP":
            plot_TOPP_dist(initial_workforce, final_workforce)
        pass
    elif args.all: 
        Modes = ["D", "SR", "ASR"]
        epochs = args.all[0]
        D = []
        SR = []
        ASR = []
        for mode in Modes:
            Org = set_initial_conditions(args.type, Org_size, HP_size, config_A, config_B, config_AB, A_config, \
                    B_config, Hconfig_A, Hconfig_B, Hconfig_AB, A_HPconfig, B_HPconfig, Leader_worldview)
            Org.Mode = mode
            if mode == "D": 
                D = run_simulation(Org, epochs)
            elif mode == "SR": 
                SR = run_simulation(Org, epochs) 
            elif mode == "ASR": 
                ASR = run_simulation(Org, epochs) 
        
        #get info
        if args.info == "Subpopulations": 
            plot_all(D, SR, ASR)
        elif args.info == "TOPP": 
            plot_all_TOPP_dists(D, SR, ASR) 

if __name__ == "__main__": 
    main() 


