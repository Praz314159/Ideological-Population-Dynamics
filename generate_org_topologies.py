''' 
This collection of functions is meant to allow easy generation of common organization network topologies.
Generating network topologies is important for a number of reasons. The most obvious one is that 
organizations do not simply have fully connected topologies, in which everyone interacts with everyone else. 
The truth is that there will be some degree of compartmentalization -- both vertical and horizontal -- in the 
structure of the organization. 

We will use networkX in order to build these topologies.

The general idea here is to generate a graph. The graph represents the organization. Each node in the graph
is an employee. Edges represent relationships. Employees can only communicate with those nodes they share edges 
with. This requires some changes to be made to the way interactions take place. One individual will be randomly
chosen. Then, a random individual with whom the first individual has a relationship (shares an edge) 

''' 
import matplotlib.pyplot as plt 
import networkx as nx 
from Organization_Model import Individual
from Organization_Model import Organization
import numpy as np 

#demonstrating that clustering coefficient increases with k neighbors ring lattic parameters 
organization_size = 200 
rewiring_probability = .3 
clustering_coefficients = [] 
for neighboring_connections in range(2, int(organization_size / 2)):
    K_coefficients = []
    for i in range(5): 
        graph = nx.watts_strogatz_graph(organization_size, neighboring_connections, rewiring_probability)
        clustering_coefficient = nx.average_clustering(graph) 
        K_coefficients.append(clustering_coefficient) 
    
    print("K = ", neighboring_connections, ": ", K_coefficients) 
    avg_K_clustering = sum(K_coefficients)/len(K_coefficients) 
    clustering_coefficients.append(avg_K_clustering)  

plt.plot(clustering_coefficients) 
plt.xlabel("K") 
plt.ylabel("Average Clustering Coefficient") 
plt.title("Watts-Strogatz Small World Networks: K vs Clustering Coefficient") 
plt.show()




'''
now we want to look at how clustering coefficient affects polarization rates there's a question here about how to 
measure polarization rates, because there are cascade points after which polarization quickly jumps. One option
is to take the average slope over the entire simulation lifespan. This is fairly straght forward, we take 
(p_final-p_initial)/num_epochs. Ok, maybe this is the wrong approach. 

What are the features of a simulation subpopulation graph. (1) initial rise (2) cascade point (3) slope following 
cascade point (usually 0). Clustering coefficient could have the following affects: (1) change is initial rise -- 
perhaps a slower increase (i.d, smaller slope) (2) move the cascade point later (more likely as clustering
cefficient rises) (3) change dynamics after cascade point, but I don't know how. 

We can define the cascade point as as sudden increase in slope. The elbow point is hard to locate because "sudden
increase" is ill-defined. Well, I guess the next step has just revealed itself. I need investigate the change in 
slope at qualitatively validated cascade points in order to get an idea for what a reasonable increase to expect 
looks like. 

''' 












