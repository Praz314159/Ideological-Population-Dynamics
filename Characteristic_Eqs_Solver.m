 
%constants 
%hiring pool configuration
%hiring pool A 
h_A_t = .33; 
h_A_config = .5; 
h_A_z = h_A_config*h_A_t; 
h_A = h_A_t*(1-h_A_config);
%hiring pool B
h_B_t = .33;
h_B_config = .5; 
h_B_z = h_B_config*h_B_t; 
h_B_ = h_B_t*(1-h_B_config); 
%hiring pool moderates 
h_AB = .34; 

%rho_* constants 
zealot_resistences = [.01, .03, .05, .07, .1, .135, .17, .205, .4, .45, ...
    .51, .58, .66, .75, .85, .95, .96, .97, .98, .99];

%Firing rate constant 
F = .1; 

%TOPP distribution --> for this, we have to assume that there is no 
%tolerance screening in the hiring process. This means that the 
%tolerance distribution won't change within the organization. And we can 
%assume for all time that the distribution is normal. 

%here we just need to define the mean and standard deviation (take care in
%function call). This is cannonical normal distribution. Could also use 
%beta distribution, but this is a good starting point. 
TOPP = @(x,m,s) exp(-((x-m).^2)/(2*s.^2)) / (s*sqrt(2*pi));

%system of differential equations 
syms n_A(t) n_A_z(t) n_AB(t) n_B(t) n_B_z(t)

ode1 = diff(n_A) == n_A*n_AB + n_A_z*(n_AB + n_B) - ...
    rho(n_A, n_A_z, zealot_resistences)*n_A*n_A_z - ...
    resign(n_A, .5, .1)*n_A + (resign(n_A, .5, .1) + resign(n_A_z, .5, .1)... 
    + resign(n_AB, .5, .1) + resign(n_B, .5, .1) + resign(n_B_z, .5, .1))...
    *n_A*h_A - F*n_A + F*h_A;     

ode2 = diff(n_B) == n_B*n_AB + n_B_z*(n_AB + n_A) - ...
    rho(n_B, n_B_z, zealot_resistences)*n_B*n_B_z - ...
    resign(n_B, .5, .1)*n_B + (resign(n_A, .5, .1) + resign(n_A_z, .5, .1)... 
    + resign(n_AB, .5, .1) + resign(n_B, .5, .1) + resign(n_B_z, .5, .1))...
    *n_B*h_B - F*n_B + F*h_B;

ode3 = diff(n_A_z) == rho(n_A, n_A_z, zealot_resistences)*n_A*n_A_z - ... 
    resign(n_A_z, .5, .1)*n_A_z + (resign(n_A, .5, .1) + resign(n_A_z, .5, .1)... 
    + resign(n_AB, .5, .1) + resign(n_B, .5, .1) + resign(n_B_z, .5, .1))*...
    n_A_z*h_A_z - F*n_A_z + F*h_A_z;

ode4 = diff(n_B_z) == rho(n_B, n_B_z, zealot_resistences)*n_B*n_B_z - ... 
    resign(n_A_z, .5, .1)*n_B_z + (resign(n_A, .5, .1) + resign(n_A_z, .5, .1)... 
    + resign(n_AB, .5, .1) + resign(n_B, .5, .1) + resign(n_B_z, .5, .1))*...
    n_B_z*h_B_z - F*n_B_z + F*h_B_z;

ode5 = diff(n_AB) == 1 - (n_A + n_A_z + n_B + n_B_z); 

odes = [ode1; ode2; ode3; ode4; ode5]; 
%S = dsolve(odes);  
%need to set initial conditions
A_config = .5; 
B_config = .5;
A_t = .33; 
B_t = .33; 
cond1 = n_A(0) == A_t*A_config;   
cond2 = n_A_z(0) == A_t*(1-A_config); 
cond3 = n_B(0) == B_t*B_config; 
cond4 = n_B_z(0) == B_t*(1-B_config); 
cond5 = n_AB(0) == .34; 
conds = [cond1; cond2; cond3; cond4; cond5];

[n_Asol(t), n_A_zsol(t), n_ABsol(t), n_Bsol(t), n_B_zsol(t)] = dsolve(odes, conds);

%helper functions 
%mapps probability values to organization states 
function output = rho(n_w, n_w_z, zealot_resistences) 
n_w_total = n_w + n_w_z; 
index = ceil(100*(n_w_total/5));  
p_switch = zealot_resistences(index);  
output = p_switch; 
end  

%here we want the integral of normal distribution from n_w to infintiy 
function output = resign(n_w, mean, std) 
output = integral(@(x) TOPP(x, mean, std), n_w, inf); 
end 
