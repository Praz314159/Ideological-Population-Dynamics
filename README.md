
<h2>Motivation</h2> 

After witnessing the attempted hostile ideological takeover of a prominent global non-profit, 
I became interested in understanding how an organization might become ideologically homogenous,
and, more importantly, how it might become overrun by zealots. This project is an attempt to model 
the ideological population dynamics of an organization in which individual are interacting, 
resigning, being fired, and being hired. The model I've developed is an extension of the model proposed
by applied mathematician Steven Strogatz in his paper "Encouraging Moderation." The paper is included in
the "Reference Papers" folder. Although my model follows the same paradigm as Strogatz's, it contains noteworthy
differences. For example, I assume that there exists a subpopulation of zealots associated with both the 
prevailing worldview and the insurgent worldview. The subpopulation of zealots associated with the prevailing 
worldview approximates an entrenched establishment whose interests align with preservation of the status quo. I have
also made an effort to incorporate known social psychological phenomena such as preference falsification and 
disagreeability. This effort to make the model consistent with the current psychological literature required
an amendment to Strogatz's conception of "zealot", which is best summed up by the Churchillian definition, someone 
"who never changes [his] mind, and never changes the subject." The most significant modifications, however, are
related to the specific challenge of modeling an organization rather than a community, which admits hiring
and firing dynamics. Novel mathematical contributions include a polarization metric that construes polarization 
as how "separated" the subpopulations (defined by worldview) comprising the organization are; a system of differential
equations and its numerical solution, describing the ideological population dynamics of an organization; and an
analysis of how various organization social network topologies affect ideological population dynamics. In particular, 
simulations were run on various random network types with respect to topological properties such as clustering 
coefficients in order to understand which networks are most robust against component separation. Preliminary 
results suggest that as clustering increases, prevasive homogenization decreases. However, individual clusters
become locally homogenous. This may lead to increased intergroup hatred and conflict, despite lower global 
polarization.  

The applications of this model, I realize now, are quite impactful. Increasingly, certain sectors such as 
tech, non-profit, and higher education, are becoming ideologically homogenous. However, ideological 
homogeneity is highly undesirable in an organization. Ideally, an organization will have a diversity of 
well-informed opinions so that new challenges can be approached from different perspectives that "check"
the biases of each other, allowing convergence upon the best or least-bad solution. Formally, this type 
of intellectual culture is known as "institutionalized disconfirmation." It is precisely the norm that 
has allows good quality research to flourish in institutions of higher education and it is also the norm
that is most under threat. Interestingly, the ideological population dynamics of entire industries, which are 
simply densely connected collections of organizations, can be simulated using the modelling framework I propose here. 
Further, if one expands one's view of an "organization" to a democratic nation, it is possible (with some 
modification) to model the effects of mass disinformation campaigns that flood the virtual public square with large 
numbers of "zealots" posing as citizens. 

The main thrust of this research is to uncover effective strategies for counteracting the general tendency towards 
polarization -- conceptualized here as "component separation", a recapitulation of entropy -- and protecting a 
culture of institutionalized disconfirmation. 

<h2>File Descriptions</h2>

The files/folders in this repository are as follows: 

1. **Organization_model.py**: This is contains the two major classes that comprise the model, namely, "Individual" 
   and "Organization", which is composed of individuals. 
2. **run_experiments.py**: This is the command line interface that allows one to easily run simulations that test 
   various parameters. 
3. **Characteristic_Eqs_Solver.m**: This is a MatLab script meant to solve, for various initial conditions, the 
   system of differential equations that fully characterizes the ideological population dynamics of an organization. 
4. **"Mathematical Characterization of System"**: This is a PDF that contains a more rigorous mathematical 
   description of the model. This document is currently in progress. 
5. **Reference Papers**: This folder contains academic literature that has informed this research. 
6. **Resultes-Figures**: This folder contains various plots that have been generated from simulations over the 
   course of this project. There are two types of plots included. The first is a plot of the fractional 
   representation of each ideological subpopulation over time. These plots generally validate the viability of the 
   anti-polarization strategy I've implemented. The second is a plot of the change in TOPP distribution over the 
   workforce. This is particularly interesting because it shows that the organization will become not only 
   highly polarized, even homogenous, but will also become overrun by very disagreeable people.  
7. **Notes.txt**: This document is a "progress journal" of sorts, that contains my thoughts during development. 

<h1> Model Description </h1>   

Below is a rough outline of the model. 

<h2> Model Assumptions </h2>  

1. No correlation between incompetency and ideology 
2. There are three basic hiring modes: Default (D), Leadership Self-Replication (SR), Anti Leadership 
   Self-Replication (ASR). 

   **D Mode**: The meaning of default mode should be fairly self-evident. The leader has no bias in hiring, and will 
   Therefore, the leader will select candidate with exactly the same bias admitted by the hiring pool. 
   
   **SR Mode**: In self-replication mode, the leader is much more likely to hire a candidate that shares his 
   worldview. How much more likely, then, is the question at hand. The most straightforward way to do this is to 
   change the likelhoods associated with choosing each worldview (i.e, a different "H_config" when in SR mode). But 
   this requires actually modifying the hiring pool, which is both unrealistic and computationally expensive. The 
   other way to do this is to set up "interviews", for which candidates are randomly chosen from the hiring pool, 
   but the likleyhood that a candidate with each worldview is selected will be different. I've chosen P(Opp_z) = 
   .05, P(Opp_nz) = .1, P(AB) = .3, P(Same) = .75, but these are slightly arbitrary. Is there a way to determine 
   more realistic values? Notice that a possible strategy for mitigating polarization is designating multiple leaders
   with hiring power of different worldviews.  

   **ASR Mode**: In anti self-replication mode, the leader is trying to maintain ideological diversity within the 
   organization. We thus need a way to measure the polarization in the organization. The polarization metric will 
   allow us to measure how well our anti-polarization ASR strategy is working. Ideally, we'd like to test different 
   strategies to see which hiring strategy is most effective in mitigating polarization. In general, ASR hiring mode 
   kicks in once polarization has exceeded a certain critical threshold, at which point hiring moves from default 
   behavior to an anti-polarization strategy that, generally, hires individuals in such a way that will move the 
   configuration of the organization towards a uniform distribution. The key questions here are: 
  
   **Hiring Assumptions**:
	* The leader can't distinguish between zealots and non-zealots. This means that if in SR mode, the leader is
          as likely to hire a non-zealot and zealot of the same worldview
	* Either the leader knows the worldview and tolerance to opposition (see below) of every candidate he
          interviews or each candidate has full knowledge of the state of the organization. 
	* The hiring pool is pre-filtered for competence. 
	* Hiring only takes place when someone has resigned or been fired. Thus the size of the organization stays 
          constant.
 
3. Individuals change their mind through speaker-listener interactions. This is how the model is evolved.        
4. Every individual within the organization has complete knowledge of the organization state. That is, 
   everybody knows what everyone else thinks at any given point in time.  

<h2>Model Functionality</h2>   

1. <center>

   |Speaker|Listener|Final|
   |-------|--------|-----|
   |  A    |  B     |  AB |
   |  A,A' |  AB    |  A  |
   |  A'   |  B     |  A  |
   |  B    |  A     |  AB |
   |  B,B' |  AB    |  B  |
   |  B'   |  A     |  B  |

   </center> 

   Note that this is modulated by preference falsification. Consider what happens when an individual is the 
   listener in an interaction. We have various scenarios:
	* If speaker is A and listener is B, then the listener is converted to AB 
	* If speaker is A' and listener is B, then the listener is subject to preference falsification, meaning that
	  they may lie about being a B. That is, they will pretend to be closer to worldview A. We assume that this 
	  means that B is acting as an AB, and will therefore be converted to an A by the interaction. 
	* If speaker is B' and listener is A, then then, similarly, the listener will lie about being a true 
          A and will pretend to be an AB in the interaction. They will subsequently be converted to a B.
	* If speaker is A' and listener is A, then the listener will change to A' if the global state of the 
          organization is such that the cost of becoming a zealot is sufficiently reduced. 

   We specify scendario 4 further. Depending on how homogenous in A the organization is, A will turn to A'. 
   It shouldn't be advantageous to switch until the organization is very homogenous in A. There is also a 
   question about when it becomes socially unacceptable to not be a zealot. There is some interesting dynamics 
   between people leaving because the organization is too homogenous and other people staying because there is 
   social benefit to becoming a zealot, or, if the organization is extremely homogenous, social cost to not becoming 
   one.

   We have a global scaling of probabilities with which A --> A' and B --> B' that is based on the % of the 
   organization that is either A or B. The idea here is that the more homogenous the organization, the less 
   of a social cost there is for being a zealot; in fact, one may even be able to accrue social capital by 
   becoming a zealot:
	* Bias = <B_1, B_2, .... ,B_n> <==> Probs = <P_1, P_2, ... ,P_n>
	* This type of switch will only occur when the speaker is a zealot and the listener is a non-zealot with 
          the same worldview 

   The function mapping degree of homogeneity to probability of switching from non-zealot to zealot will
   be the same for both cases, A --> A' and B --> B'. How should this mapping behave? First, 
   it seems reasonable that there would be a long leading tail. It will only become advantageous, either 
   to accrue social capital or to avoid social destruction, to become a zealot if the organization is highly
   homogenous with respect to your worldview (>80%?). People with high thresholds for homogeneity will likely 
   end up as zealots if the organization tends towards homogeneity in their worldview. 

   We have buckets <5, 10, 15, 20, 25, 30, 35, 40, 45, 50 ... >. These are associated with the following
   probabilities: <.01, .02, .05, .07, .1, .135, .17, .205, .4, .45, .51, .58, .66, .75, .85, .95, .96, .97, 
   .98. .99>

   Although I'd have like to use a continuous map here, for the sake of convenience, I've used discretized
   buckets.  

2. Each individual has TOPP, or "tolerance to opposition" value. This is the percentage of the organization that must
   be of a competing worldview for an individual to resigns. TOPP is a measure of an individual's tolerance for being   in the minority. This can be conceptualized, in psychometric terms, as how "disagreeable" an individual is. I've 
   given TOPP a normal distribution in the organization's workforce. However, the question of which distribution is 
   the right one to use should be revisited. Intuition suggests that perhaps a beta distribution with carefully 
   selected parameters is the better option. 

3. Any organization will have a natural steady turn over rate. We assume that individuals won't be fired for 
   ideological reasons unless the leader is a zealot. In the normal case, once an individual leaves the organization
   (incompetence, surpassed threshold), they are replaced by someone from the hiring pool. Here are some factors to 
   consider: 
	* The hiring pool might be ideologically biased. 
	* If in SR mode, then the bias of the leader will compound the hiring pool bias. 
	* If in ASR mode, then the bias of the leader will counteract the hiring pool bias. 

