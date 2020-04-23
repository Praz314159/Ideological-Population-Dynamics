











<h2>Motivation</h2> 

After witnessing the attempted hostile ideological takeover of a prominent global non-profit, 
I became interested in understanding how an organization might become ideologically homogenous,
and, more importantly, how it might become overrun by zealots. This project is an attempt to model 
the ideological population dynamics of an organization in which individual are interacting, 
resigning, being fired, and being hired. The model I've developed is an extension of the model proposed
by applied mathematician Steven Strogatz in his paper "Encouraging Moderation." The paper is included in
the "Reference Papers" folder. Although my model follows the same paradigm as Strogatz's, it does involve
novel mathematical contributions such as, for example, a polarization metric that construes polarization 
as how "separated" the subpopulations (defined by worldview) comprising the organization are. 

The applications of this model, I realize now, are quite impactful. Increasingly, certain sectors such as 
tech, non-profit, and higher education, are becoming ideologically homogenous. However, ideological 
homogeneity is highly undesirable in an organization. Ideally, an organization will have a diversity of 
well-informed opinions so that new challenges can be approached from different perspectives that "check"
the biases of each other, allowing convergence upon the best or least-bad solution. Formally, this type 
of intellectual culture is known as "institutionalized disconfirmation." It is precisely the norm that 
has allows good quality research to flourish in institutions of higher education and it is also the norm
that is most under threat. Interestingly, the ideological population dynamics of entire industries, which are 
simply densely connected collections of organizations, can be simulated using the modelling framework I propose here. 

Further, if one expands one's view of an "organization" to a democratic nation, it is possible (with some modification)
to model the effects of mass disinformation campaigns that flood the virtual public square with large numbers of 
"zealots" posing as citizens. 

The main thrust of this research is to uncover effective strategies for counteracting the general tendency towards 
polarization -- conceptualized here as "component separation", a recapitulation of entropy -- and protecting a culture of 
institutionalized disconfirmation. 

<h2>File Descriptions</h2>

The files/folders in this repository are as follows: 

1. **Organization_model.py**: This is contains the two major classes that comprise the model, namely, "Individual" and
   "Organization", which is composed of individuals. 
2. **run_experiments.py**: This is the command line interface that allows one to easily run simulations that test various
   parameters. 
3. **Characteristic_Eqs_Solver.m**: This is a MatLab script meant to solve, for various initial conditions, the system of 
   differential equations that fully characterizes the ideological population dynamics of an organization. 
4. **"Mathematical Characterization of System"**: This is a PDF that contains a more rigorous mathematical description of the
   model. This document is currently in progress. 
5. **Reference Papers**: This folder contains academic literature that has informed this research. 
6. **Resultes-Figures**: This folder contains various plots that have been generated from simulations over the course of this project. 
7. **Notes.txt**: This document is a "progress journal" of sorts, that contains my thoughts during development. 

<h1> Model Description </h1>   

<h2> Model Assumptions </h2>  

1. No correlation between incompetency and ideology 
2. 3 basic hiring modes: Default (D), Leadership Self-Replication (SR), Anti Leadership Self-Replication (ASR)
   
   SR Mode: what does being in self_replication mode mean? It means that the leader is much more likely to hire 
   someone who thinks like him. But, how much more likely? Certainly, they will never hire a zealot with the 
   opposite worldview because they would be more outspoken and their interaction would spoil. He might hire a 
   moderate or non-zealot with the opposite worldview, but is most likley to hire someone with the same worldview. 
   What 
   scheme can this be reflected by? The most straightforward way to do this is to change the likelhoods associated 
   with choosing each worldview (i.e, a different "H_config" when in SR mode). The other way to do this is to set up 
   "interviews"in which candidates are randomly chosen from the hiring pool, but the likleyhood that a candidate with
   each worldview is selected will be different. The question, of course, is What these probabilities should be. 
   I've chosen P(Opp_z) = .05, P(Opp_nz) = .1, P(AB) = .3, P(Same) = .75, but these are slightly arbitrary. Is there
   a way to determine more realistic values? 

   **ASR Mode**: What does being in anti self-replication mode mean? It means that the leader is trying to maintain 
   ideological diversity within the organization. We thus need a way to measure the polarization in the organization. 
   The polarization metric will allow us to measure how well our anti-polarization ASR strategy is working. Ideally, 
   we'd like to test different strategies to see which hiring strategy is most effective in mitigating polarization.
   In general, ASR hiring mode kicks in once polarization has exceeded a certain critical threshold, at which point 
   hiring moves from default behavior to an anti-polarization strategy that, generally, hires individuals in such a 
   way that will move the configuration of the organization towards a univform distribution. The key questions here are: 
        1. How will polarization be measured?
        2. What threshold must be exceeded in order for ASR mode to counteract the polarization?  
   
   We have the following hiring assumptions: 
        1. The leader can't distinguish between zealots and non-zealots. This means that if in SR mode, the leader is
           as likely to hire a non-zealot and zealot of the same worldview. 
        2. The hiring pool is pre-filtered for competence.  
        3. Hiring only takes place when someone has resigned or been fired. Thus the size of the organization stays constant.
 
3. Individuals change their mind through speaker-listener interactions. This is how the model is evolved.        
4. When an individual engages in an interaction as a listener, they only move one position in the direction 
   of the speaker. 
5. Every individual within the organization has complete knowledge of the organization state -- that is, 
   what everybody thinks at any given point in time.  

MODEL FUNCTIONALITY  

1. <center>

   |Speaker|Listener|Final|
   |-------|--------|-----|
   |  A,A' |  B     |  AB |
   |  A,A' |  AB    |  A  |
   |  B    |  A     |  AB |
   |  B    |  AB    |  B  |

   </center> 

   Note that this is modulated by preference falsification. Consider what happens when an individual is the 
   listener in an interaction. We have various scenarios:

     1. If speaker is A and listener is B, then the listener is converted to AB 
     2. If speaker is A' and listener is B, then the listener is subject to preference falsification, 
        meaning that they may lie about being a B. That is, they will pretend to be closer to worldview A. 
        We assume that this means that B is acting as an AB, and will therefore be converted to an A by the
	interaction. 
     3. If speaker is B' and listener is A, then then, similarly, the listener will lie about being a true 
        A and will pretend to be an AB in the interaction. They will subsequently be converted to a B.
     4. If speaker is A' and listener is A, then the listener will change to A' if the global state of the 
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
 
      1. Bias = <B_1, B_2, .... ,B_n> <==> Probs = <P_1, P_2, ... ,P_n>
      2. This type of switch will only occur when the speaker is a zealot and the listener is a non-zealot with 
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
   be of a competing worldview for an individual to resigns. TOPP is a measure of an individual's tolerance for being    
   in the minority. This can be conceptualized, in psychometric terms, as how "disagreeable" an individual is. I've given 
   TOPP a normal distribution in the organization's workforce. However, the question of which distribution is the right one to 
   use should be revisited. Intuition suggests that perhaps a beta distribution with carefully selected parameters is the 
   better option. 

3. Any organization will have a natural steady turn over rate. We assume that individuals won't be fired for 
   ideological reasons unless the leader is a zealot. In the normal case, once an individual leaves the organization
   (incompetence, surpassed threshold), they are replaced by someone from the hiring pool. Here are some factors to 
   consider: 

      1. The hiring pool might be ideologically biased --> note that unbiased hring (D mode) will select for this bias 
      2. If in SR mode, then the bias of the leader will compound the hiring pool bias 
      3. If in ASR mode, then the bias of the leader will counteract the hiring pool bias 

