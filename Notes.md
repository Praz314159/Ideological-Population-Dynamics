##################################################################
Notes on IPM being developed 
##################################################################
4/16/20: 




4/15/20: I was playing around with different network layouts. It turns out that the Spectral Theoreme is pretty usueful.
By positioning nodes using the eigenvalues of the Laplacian of the small world network, we get some implicit structure 
that reflects graph characteristics like connectedness, cut sparseness. (https://www.semanticscholar.org/paper/Drawing-
graphs-by-eigenvectors%3A-theory-and-practice-Koren/64d8c8099fef68bdfd7bab4c57b9c5e5f5aa21a6). This visualization gave 
me a few interesting ideas. 

1. The leader of the organization can be defined as the node in the graph with the minimum degree >= 1. (This should always 
be the case, since one of the graph preprocessing steps should be removal of isolated nodes.) Next, some type of hierarchy of 
influence can be established by assigning a "influence weight" to nodes that descends (exponentially?) with distance
from the "leader" node. So, different individuals at different levels of seniority will have different levels of influence 
over the dynamics of the organization. One question is whether or not this will become too similar to statistical physics 
approaches to belief dynamics like classic Ising Models (see Reference Papers). Another question is how weights will be 
incorporated into interactions. Clearly, the model will transition from deterministic to probabilistic. So "influence" 
means that A will change B with rho probability? Perhaps this can be used to model "group interactions" where different 
individuals have different levels of influence? This idea, I think, has some potential. 

2. If there are multiple least degree nodes, then perhaps they can all be given hiring power. Perhaps, one strategy for 
maintaining ideological diversity is to have multiple leaders of different worldviews, all of whom are hiring in a 
biased way. This way, instead of relying on a single individual who has to check his own bias, the responsibility of 
institutional discomfirmation is distributed among the organization's leadership. 

4/11/20: Reading about different network topologies: 

1. Dunbar's Number: This is the number of close social relationships that humans can maintain at a given point.
Number was extrapolated by anthropologist Robin Dunbar (British) in the 1990s from the results obtained through 
study of other primates. Correlation was noticed between primate brain size and average social group size. Number
was determined to be 150 stable relationships for humans. 

https://en.wikipedia.org/wiki/Dunbar%27s_number

2. Percolation Theory: Simple analogy is that percolation theory describes the behavior of water flowing through a
structure. Really, it's the mathematical theory regarding the behavior of connected clusters in a random graph. 
Given an infinite lattice, ther percolation threshold p_c is defined as the concentration (occupation
probability) p at which an infinite cluster appears. That is a cluster that "percolates" from one boundary of the 
lattice to another. Various lattice structures have different percolation thresholds. Does rate of homogenization
vary with percolation threshold? See Christensen refference text (Imperial College). Site percolation problem vs 
bond percolation problem. Consider conditions on the 1d lattice (p_c = 1) --> simple conditions, maybe some clues 
here about organizational structure?   

https://en.wikipedia.org/wiki/Percolation_theory
http://web.mit.edu/ceder/publications/Percolation.pdf

3. Small World Network (Watts and Strogatz): characterized by small average path length, triadic closures, 
local clustering, and hubs. (Triadic closures is a concept in social network theory, first suggested by German 
sociologist Georg Simmel --> if a strong ties A-B and A-C exist, then there is a strong tie B-C. The concept 
was later popularized by Mark Granovetter). Strogatz model accounts for clustering while retaining the short average 
path lengths of the Erdos-Renyi model. This is done by interpolating between randomized structure close to ER graphs
and regular ring lattice. Although the Strogatz model produces a reasonable description of many networks, it produces 
an unrealistic degree distribution. Real networks are often "scale free" (degree distribution follows power law)
and inhomogenious in degree (hubs and scale-free distribution).

Small world network is characterized   
 
https://en.wikipedia.org/wiki/Small-world_network#Properties_of_small-world_networks
https://en.wikipedia.org/wiki/Triadic_closure
https://en.wikipedia.org/wiki/Watts%E2%80%93Strogatz_model
https://en.wikipedia.org/wiki/Scale-free_network
https://www.springer.com/journal/10588 --> journal to possibly publish in 

4/8/20: I feel like I'm now making some serious progress. I made a number of refinements that make the model
more "up-to-date". They are: 

1. Making the interaction rules explicit 
2. Changin the default hiring schem to guarantee that a candidate is hired. Previously, with the tolerance check,
there was no guarantee that a single candidate randomly selected would pass the tolerance check. Now, the hirer
continuously screens candidates until a candidate that passes the tolerance check is found. The first candidate 
that passes the tolerance check is hired. 
3. The TOPP distribution is changed from a normal distribution with mean .5 and std .1 to a beta distribution 
with alpha = 1  and beta = 4. This is, intuitively, a bit more realistic.
4. Resignation rules are changed. "A"s and "B"s no longer consider "AB"s as "opposition". Further, "AB"s only
resign in response to polarization levels. This along with the change in distribution drasitcally reduced 
the number of resignations.  

More importantly, though, my conversation with Jonathan Haidt, along with my dive into statistical physics models 
for belief propagation has inspired the next steps for this project. Firstly, my conception of zealots has been 
incorrect. I have been conceptualizing, until this point, zealots as individuals whose minds will not change. This
is, in fact, not the case. Zealots and individuals who make life difficult for those who disagree with them. They
cause those who disagree with them to either go into hiding or to leave the organization. I somehow need to find a
way for this to be manifested in my model. When do individuals go into hiding and when will they leave the org? 
Does this depend on the state of the organization? How does this play out when there are two zealot populations 
that are in conflict with one another? 

The other important step I'd like to take is underlaying the organization with a network topology that determines
the structure of interactions. Clearly, not all organizations are densely connected. They may have densely 
connected components such as teams, but only is small non-profits or like organizations will this be the case. 

3/19/20: I've taken an interest in tracking the TOPP distribution changes over time. I've build out the CMI for 
simulation running in order to accomodate this. But, for some reason -- I'm not sure why yet -- the TOPP 
distribution isn't showing any change between the intitial workforce and the final workforce. What's going on??!! 

3/12/20-3/13/20: Fixed point analysis is proving extremely challenging. Getting fixed points of nonlinear system 
of diffeqs with degree >3 is incredibly difficult. I'll be on the lookout for computational methods. For now, though
I'm going to focus on developing a precise mathematical language for the model. That way, when I do get back to 
analysis of the construction, things will be easier. 

There are a few additional changes I've made to the model. Firstly, it has become apparent to me that including two
two tolerance values TOPP and THOM is unnecessary. Assuming that THOM = 1 for all individuals is not unreasonable 
given the tribal nature of human beings. Having resignation dependent solely on a single tolerance also allows 
for mathematical simplification. The question, of course, is with what distribution to characterize TOPP in the 
workforce. Intuitively, a beta distribution with properly chosen parameters seems reasonable. However, TOPP 
definitionally acts like a proxy for disagreeability. The distribution of disagreeability in a general American
population is known. More research is needed here, but I'm fairly certain it acts like a normal distribution 
with characteristic std and mean. THOM has thus been removed. 

Finally, I have been able to build out a base working command line interface for running simulations. I can run
default, self-replication, and anti-self-replication mode, tracking and plotting fractional subpopulation
values for each. More importantly, I can plot all three against eachother for the same initial conditions. This 
gives a good visualization of how the different hiring strategies affect the ideological makeup of the organization.

3/10/20: I'm now conducting a fixed point analysis of the system of nonlinear differential equations. 
It looks like the easy fixed point analysis given in the Strogatz paper won't be applicable here. 
However, it might be possible to conduct a generalized stability analysis using methods involving 
eigenanalysis of the Jacobian. I also was able to think a bit more carefully about the system of 
differential equations I orginally drew up. I realized several flaws which have now been corrected.

3/7/20: For the past few days, I have been working on the mathematical characterization of the system.
There are multiple areas in which things are illdefined. Perhaps I should have begun with the 
mathematical characterization then implemented the model to validate analytical results. In 
particular, I have finally come up with what I think is a workable metric for polarization that is 
constructed, first, using an average of three values that tell us how distant from being equal each 
subpopulation is relative to the others. Note that this average, which we'll call rho_0 is in [0,inf).
 Because we want the polarization value to be in the interval [0,1), we take Polarization = 
2/pi*arctan(rho_0). Now polarization is increasing as rho_0 increases and converges to a limit of 1 
on [0,inf).

2/29/20: Ran a test today that confirmed that the salient variable in anti-self replication here is 
how exhaustive the search for moderates is. If the hiring pool is sufficiently compromised, then if 
the search isn't exhaustive enough, then the organization will end up hiring As and Bs instead of 
moderates. More accurately, the organization will hire with the same bias as the hiring pool, and 
polarization will steadly increase. 

2/27/20: For some reason, when in ASR mode, whenever a new AB is hired, he is hired to the same 
position. In one case it was position 99. It looks like when ASR mode is entered, any AB will 
always resign. We therefore get stuck in a rut, where the same position resigned by an AB is
filled by an AB who then resigns again. There is a choice here about whether or not to assume that the
the state of the organization is transparent to the hiring pool or not. If we make this assumption,
then an individual will not enter the organization if either of his tolerances -- TOPP or THOM --
are exceeded. This avoids the problem, however, of individuals with the same worldview being hired
for then resigning from the same position. This can be solved simply by only hiring individuals who
are able to "handle" the current state of the organization. Or, rather, by assuming that, since
the state of the organization is visible to the hiring pool, there is some self-selection force 
causing only individuals who have the ability to withstand the current state of the organization 
to submit themselves for candidacy. 

When we assume this selective force, born of the prior assumption of "organizational visibility to 
hiring pool", the long term dynamics of the organization change. The organization's polarization
is kept in check, hovering at around .6, which is the threshold used to trigger conscious hiring of
ABs. In the opposite case, the predominant worldview and the opposite worldview zealots converge to
roughly .5, while everything else converges to 0. 

2/21/20: The code is now fully debugged and working. The main error fixed today was particularly 
frustrating, although I learned quite a bit from it: 

I originally updated the configuration of the organization's workforce using an update_config() 
function. Statistical information about the workforce was stored as fields (n_*, N_*, polarization,
 etc.). The update_config() function then either incremented or decremented the count of individual
 with a particular worldview when a change in the workforce took place -- hiring, firing, 
interaction, resignation. It's unclear why, but this resulted in an out-of-sync issue between the 
statistical information about the workforce and the workforce itself. Particular worldviews would 
be detected in the workforce and selected for resignation or firing even when the count with respect
 to their worldview had been driven to zero already. This meant that worldview counts were negative
 given enough epochs. This was solved simply by simplifying the organization class with a 
get_statistics() function that reads in the workforce list and operates on it directly to recover 
all the relevant statistical information. get_statistics() was then called whenever the statistical
 information was required. This allowed the statistics and the workforce list (assuming the 
workforce list was updated correctly) to always be in sync. 

So, it looks like the model is now fully operational, and I can move on to the finer details. In 
particular: 
	1. Building a command line interface that I can use to efficiently run experiments 
	2. Developing a proper metric for polarization w/ range [0,1] that increases as components 
become more segregated 
	3. Finding the proper distributions for TOPP and THOM (in particular, think about TOPP for 
moderates and THOM for zealots)  
	4. Probabilities for SR and ASR	
	5. Developing the differential equations that predict the behavior we see 
	6. Building a pygame functionality so that the dynamics of the model can be visualized 

In addition, it is probably time to drop all the notes made thus far into a word doc and 
linguistically flush out the model. This will be a good way to get the ball rolling on the paper 
whose publication, I'm sure, is inevitable. Ha, laughable.   

2/18/20: I've gotten the model to run. However, there are a few bugs that need to be worked out:
	1. For some reason the update function is not worked as I'd like it to. It seems to be 
misbehaving when interactions, firings, hirings, and resignations occur. When individuals are added
to the organization's workforce, we have 1K individuals. This should remain constant. For some 
reason, though, it isn't. This means, likely, that I'm not decrementing everywhere I should be. 
Perhaps in the resignation function? 
	2. For some reason, negative n_* values were being achieved. This doesn't make any sense, 
since for this to happen, a resignation or interaction-as-listener needs to take place for a 
worldview that isn't represented in the organization. That is, a non-existent individual is having 
his mind changed or is resigning or is being fired from the organization. 

It's good, however, that the model is at least working. Up next, once these bugs are fixed, is 
parameter tuning, which I'm excited about. What distribution should be used for the threshold 
parameters? Further, what should be threshold buckets be for zealot_resistance_probabilities? And, 
finally, what is a better measure for polarization than simple 1-n_AB? These are all good questions
that need to be answered. Once they are, then I can develop a nice interface with which to nicely 
run experiments
