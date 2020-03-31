%differential equations 
%syms u(t) v(t) w(t)
%n_A = diff(u) == 
%n_A_z 
%n_AB
%n_B
%n_B_z 



%dn_A/dt = n_A*n_AB + n_A_z(n_AB + n_B) - rho_A*n_A*n_A_z - r_A*n_A +
%r*n_A*h_A - F*n_A + F*h_A

% r = r_A + r_A_z + r_AB + r_B_z 
% 

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

%we want resignation values. But, these are indefinite integrals 
r_A = 
r_A_z = 
r_AB = 
r_B = 
r_B_z = 



syms n_A(t) n_A_z(t) n_AB(t) n_B(t) n_B_z(t)

ode1 = diff(n_A) == n_A*n_B + n_A_z*(n_AB + n_B) - 