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
from Organization_model import Individual
from Organizaation_model import Organization












