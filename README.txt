I was inspired to create this project after witnessing an attempted hostile ideological takeover
of a prominent non-profit (TY SOP). In fact, the situation is pending. It just so happened that this 
took place immediately after I had read a number of papers regarding ideological population dynamics.
One simple model, in particular, that I took a liking to and that this work builds upon, is Steven
Strogatz's "Encouraging Moderation", which I've included here.

Here is a rough description of the model. 

MODEL ASSUMPTIONS: 

1. No correlation between incompetency and ideology 
2. 3 basic hiring modes: Default (D), Leadership Self-Replication (SR), Anti Leadership Self-Replication (ASR)
3. Individuals change their mind through speaker-listener interactions. Hiring thus potentially depends on the 
   worldview of the organization's leader. 
   
   SR Mode:  

   what does being in self_replication mode mean? It means that the leader is much more likely to hire someone 
   who thinks like him. But, how much more likely? Certainly, they will never hire a zealot with the opposite 
   worldview because they would be more outspoken and the interaction would spoil. Might hire AB or non-zealot 
   opp, but is most likley to hire someone with the same worldview. What scheme can this be reflected by? 
   The most straightforward way to do this is to change the likelhoods associated with choosing each 
   worldview (i.e, a different "H_config" when in SR mode). The other way to do this is to set up "interviews"
   in which candidates are randomly chosen from the hiring pool, but the likleyhood that worldviews are selected
   are different. What should these probabilities be!!? Let's try P(Opp_z) = .05, P(Opp_nz) = .1, P(AB) = .3, 
   P(Same) = .75

   ASR Mode: 

   What does being in anti self-replication mode mean? It means that the leader is trying to maintain ideological
   diversity within the organization. This means that we need a way to measure the polarization in the organization. 
   If the polarization is above a certain threshold, then ASR moves from hiring in a default behavior to 
   counter-acting the polarization by hiring individuals that will move the configuration of the organization 
   towards a uniform distribution. The key questions here are: 
        1. How will polarization be measured?
        2. What threshold must be exceeded in order for ASR mode to counteract the polarization?  
   
   
   We have the following hiring assumptions: 
        1. leader can't distinguish between zealots and non-zealots. This means that if in SR mode, the leader is
           as likely to hire a non-zealot and zealot of the same worldview. 
        2. hiring pool is pre-filtered for competence 
        3. hiring only takes place when someone has been fired 
        
4. When an individual engages in an interaction as a listener, they only move one position in the direction 
   of the speaker.
5. Every individual within the organization has complete knowledge of the organization state -- that is, 
   what everybody thinks at any given point in time. This is perhaps the most unrealistic assumption, since  

MODEL FUNCTIONALITY  

1. We have the following general rules:

    A,A' |  B  |  AB
    A,A' |  AB |  A
    B    |  A  |  AB
    B    |  AB |  B

    Note that this is modulated by preference falsification. Consider what happens when an individual is the 
    listener in an interaction. We have various scenarios:

        1. If speaker is A and listener is B, then the listener is converted to AB 
        2. If speaker is A' and listener is B, then the listener is subject to preference falsification, 
           meaning that they may lie about being a B. That is, they will pretend to be closer to worldview A. 
           We assume that this means that B is acting as an AB, and will therefore be converted to an A. 
        3. If speaker is B' and listener is A, then then, similarly, the listener will lie about being a true 
           A and will pretend to be an AB in the interaction. They will subsequently be converted to a B.
        4. If speaker is A' and listener is A, then the listener will change to A' if the global state of the 
           organization is such that a particular 

    depending on how homogenous in A the organization is, A will turn to A'. It shouldn't be advantageous to 
    switch until the organization is very homogenous in A. There is also a question about when it becomes 
    socially |unacceptable| to not be a zealot. There is some interesting dynamics between people leaving 
    because the organization is too homogenous and other people staying because there is social benefit to 
    becoming a zealot, or, if the organization is extremely homogenous, social cost to not becoming one.

2.  Each individual has TOPP --> this is the percentage of the organization that is of the opposite ideology of 
    the individual at which the individual resigns. TOPP is a measure of an individual's tolerance for being in the 
    minority. 

3.  Any organization will have a natural steady turn over rate. We assume that individuals won't be fired for 
    ideological reasons unless the leader is a zealot. In the normal case, once an individual leaves the organization
    (incompetence, surpassed threshold), they are replaced by someone from the hiring pool. Here are some factors to 
    consider: 
        1. The HP might be ideologically biased --> note that unbiased hring (D mode) will select for this bias 
        2. If in SR mode, then bias of leader compounds the HP bias 
        3. If in ASR mode, then bias of leader will counteract HP bias 

4.  We have a global scaling of probabilities with which A --> A' and B --> B' that is based on the % of the 
    organization that is either A or B. The idea here is that the more homogenous the organization, the less 
    of a social cost there is for being a zealot; in fact, one may even be able to accrue social capital by 
    becoming a zealot. 
        1. Bias = <B_1, B_2, .... ,B_n> <==> Probs = <P_1, P_2, ... ,P_n>
        2. This type of switch will only occur when the speaker is a zealot and the listener is a non-zealot with 
       the same worldview 

    The function mapping degree of homogeneity to probability of switching from non-zealot to zealot will
    be the same for both cases, A --> A' and B --> B'. How should this mapping behave be structured. First, 
    it seems reasonable that there would be a long leading tail. It will only become advantageous, either 
    to accrue social capital or to avoid social destruction, to become a zealot if the organization is highly
    homogenous with respect to your worldview (>80%?). 

    People with high thresholds for homogeneity will likely end up as zealots if the organization tends 
    towards homogeneity in their worldview. 

    We have buckets <5, 10, 15, 20, 25, 30, 35, 40, 45, 50 ... >. These are associated with the following
    probabilities: <.01, .02, .05, .07, .1, .135, .17, .205, .4, .45, .51, .58, .66, .75, .85, .95, .96, .97, 
    .98. .99> 


