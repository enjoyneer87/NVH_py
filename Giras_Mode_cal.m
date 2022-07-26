% 개발 희망사항
% Draw the dimension : 계산을 위해 값을 어차피 넣으니 그 dimension 시각화도 함께
% analytical Modal 계산

% Minimun Requirement 
%  :  analytical Modal 계산


%% 5.3.5 example Dimension and Material parameter

%%%  Dimension
model.D_lin=0.16; %[m]
model.D1_out=0.233 ;
model.L_i=0.1975; %[m]
c_t=5.87; % stator tooth width [mm]
b_14= 3; %stator slot opening [mm]
h_c=8.42; % thichness of stator yoke[mm]
h_ov=48; %length of winding over hang [mm]
D_f=0.246; %diameter of frame [m]
L_f=0.359; %length of frame [m]

s_1=36 % The number of Stator teeth(Slots) <br>
c_t=c_t % the tooth width  <br> above
h_t=5 % tooth height

%% Mass of Part
D_c=0.112*2 % stator core Mean diameter
D_c=D1_out-h_c
M_t=10.27   % mass of all stator teeth
M_w=11.45   % mass of the stator winding
M_c=8.58    % stator core 무게 [kg] % mass of the stator core cylinder (yoke) 
M_i=0.57    % mass of insulation

%% Material Paremter 

% specific mass densit
rho_c=7700   %specific mass density of laminations [kg/m**3]
rho_w=8890   %specific mass density of copper [kg/m**3]
rho_f=2700   %specific mass density of frame(aluminium) [kg/m**3]

% moudlus of elesticity
E_c=200*10^9            % moudlus of elesticity of laminations [Pa]
E_w=9.4*10^9            % moudlus of elesticity of winding with insulation [Pa]
E_f=71*10^9             % moudlus of elesticity of frame(aluminium) [Pa]

% Poisson ratio 
v_c=0.3                  %Poisson ratio of lamination
v_w=0.35                 %Poisson ratio of copper
v_f=0.33                 %Poisson ratio of frame(aluminium) 

%% %%% Eq (5.1) Amplitude of vibration displacements of mode_date $m$
% m : spatial order
% j : temporal order
m=1
mode_date(m).w_m=[200:200:2000] % angular natural frequency of the mode_date m 
mode_date(m).w_r=[2 %  angular frequency of the force component of the order r
m=1
mode_date(m).f_m=mode_date(m).w_m/(2*pi)
mode_date(m).f_r=mode_date(m).w_r/(2*pi)


% mode_date(i).zeta_m %  modal damping ratio

%D_1in=2*stator.Rint % Inner Diameter of the statr core 
                    % Machine.LamSlotWind.Rint
%L_i=stator.L1 % the effective 


%% temporary data 
mode_date(m).Pm_r=10 % Magnitude of the magnetic pressure of the order r (eq2.115, 2.116, 2.117)
% j=1 : spatial order r
j=1;
Force(j).Fm = pi*model.D_lin*model.L_i*mode_date(m).Pm_r % amplitude of force 
M=100 % Mass (kg) of the cylindrical shell
%%
% $A_{m}=\frac{F_{m} / M}{\sqrt{\left(\omega_{m}^{2}-\omega_{r}^{2}\right)^{2}+4 \zeta_{m}^{2} \omega_{r}^{2} \omega_{m}^{2}}}$ 



%Eq 5.1
% Amplitude of vibration displacements of mode_date m
% Am=Fm/M/sqrt(pow(pow(w_m,2)-pow(w_r,2),2)+4*pow(zeta_m,2)*pow(w_r,2)*pow(w_m,2)) 
mode_date_cal(m).Am=Force(j).Fm/M/sqrt((mode_date(m).w_m^2-mode_date(m).w_r^2)^2+4*mode_date(m).zeta_m^2*mode_date(1).w_r^2*mode_date(m).w_m^2);



%Do not run
%python list 

%Eq 5.3 
% 
% zeta_m=1/(2*pi)*(2.76*10^(-5)*f_m[i]+0.062)
% 
% w_m=[1,2,3,4,5,6];
% w_r=[1,2,3,4,5,6];
% 
% %Eq 5.2
% hm=[1,2,3,4,5,6];
% 
% w_m[i]=f_m[i]*(2*pi) % angular natural frequency of the mode_date m 
% w_r[j]=f_r[j]*(2*pi) % angular frequency of the force component of the order r
% 
% %Eq 5.4
% Fm[i] = pi*D_1in*L_i*Pm_r[j] % amplitude of force 
% Am[i]=Fm[i]/(M*pow(w_m[i],2))*hm[i]
% 
% %Am1=Am
% %second term
% %Am=pi*D_1in*L_i/(M*w_m**2)*Pm_r*hm
% 
% Am[0]=Am
% 
% %Eq (5.5)
% %First term
% V_m[i]=w_r[j]*Am[i]
% %V_m1=V_m
% %second term
% V_m[i]=2*pi*f_r[j]*pi*D_1in*L_i/(M*w_m[i]**2)*Pm_r*hm[i]
% 
% %python dictionaries
% 
% %pandas series , Dataframe

%%
%Eq 5.2 Magnification factor
%First term
hm=Am/(Fm/(M*pow(w_m,2)))
mode_date(m).hm=mode_date_cal(m).Am/(Force(m).Fm/(M*mode_date(m).w_m^2));
%Second term

%hm=1/pow((1-((f_r/f_m)^2))^2+(2*zeta_m*(f_r/f_m))^2,1/2)
print(hm)

