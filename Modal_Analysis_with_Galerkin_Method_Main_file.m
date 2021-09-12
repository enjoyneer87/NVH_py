%....................................................
%		Sep.26 to Dec22, 2010. Ramin Shamshiri		.
% 				University of Florida 				.
%					ramin.sh@ufl.edu				.
%....................................................

% The purpose of this program is to perform modal analysis for a two-degrees 
% of freedom tractor suspension system. Galerkin's method over "ne" individual 
% elements of time domain [t1,t2], was used to numerically solve the two
% uncoupled resulting 2nd-oder ODEs. 

%==========================================================================
% Original suspension model:
%               M*d2x    +   B*dx     +   K*x=0          t1<t<t2
% where x=[xs,xw]
% Boundary conditions: 
%       xs (t1 )=xs1 , xs (t2 )=xs2,  xw (t1 )=xw1 , xw (t2 )=xw2
%==========================================================================

%==========================================================================
% Modal equations:
%           d2(Etta1)  +    Bg_diag(1,1)*d(Etta1)    +   (Omega1^2)*(Etta1)=0
%           d2(Etta2)  +    Bg_diag(2,2)*d(Etta2)    +   (Omega2^2)*(Etta2)=0
% Boundary conditions in modal coordinates: 
%       Etta1=Fi1'*M*xs
%       Etta2=Fi2'*M*xs
%       BC=[Etta1 Etta2]
%==========================================================================
%==========================================================================
% The output of this program:
% 1- The solution of Etta1(t), Etta1'(t), Etta1"(t)
% 2- The solution of Etta2(t), Etta2'(t), Etta2"(t)

%=============================Program Begin================================
clear all

% Tractor suspension springs coefficients   (N/m)
k1=5349;                k2=7489;
K=[k1+k2 -k2;-k2 k2];

% Tractor suspension masses     (kg)
m1=3200;                 m2=236;
M=[m1 0;0 m2];

% Tractor suspension damping coefficients
b1=0;                   b2=0;       % Undamped situation
B=[b1+b2 -b2;-b2 b2];

% Calculating ? and Normalized eigenvectors matrices
[V,D]=eig(K,M);
omega1=sqrt(D(1,1));    % omega1
omega2=sqrt(D(2,2));    % omega2
Omega=[omega1 omega2];

% Normalized eigenvectors
U1=[V(1,1)/V(1,1);V(2,1)/V(1,1)];
U2=[V(1,2)/V(1,2);V(2,2)/V(1,2)];

% Calculating ?1 and ?2 by applying the largest entry normalization method
fi1=(1/max(U1))*U1;
fi2=(1/max(U2))*U2;
fi=[fi1 fi2];

% Verify the answers 
fi1'*M*fi2;     % This value should yield zero

% Calculating generalized M and K
M1=fi1'*M*fi1;
M2=fi2'*M*fi2;

K1=fi1'*K*fi1;
K2=fi2'*K*fi2;

% Eigenvector Mass orthonormalization
% Now we renormalize fi1 and fi2 by calculating ? matrix, to get unit generalized masses

Fi1=sqrt(1/M1)*fi1;     % Fi1
Fi2=sqrt(1/M2)*fi2;     % Fi2
Fi=[Fi1 Fi2];           % Fi=[Fi1 Fi2]

Mg=Fi'*M*Fi;
Bg=Fi'*B*Fi;
Kg=Fi'*K*Fi;


% Diagonalization of Bg using Rayleigh quotient
Bg_diag=[(fi1'*B*fi1)/(fi1'*fi1) 0;0 (fi2'*B*fi2)/(fi2'*fi2)];

% Calculating ?1,  ?2, the effective modal damping
S1=Bg_diag(1,1)/(2*omega1);     % S1
S2=Bg_diag(2,2)/(2*omega2);     % S2


%% Beging solving modal equations
% d2?1  +    Bg_diag(1,1)*d?1    +   (omega1^2)*?1=0
% d2?2  +    Bg_diag(2,2)*d?2    +   (omega2^2)*?2=0

% Number of individual elements in Galerkin method
ne=3072;

etta=zeros(ne+1,2);         % Initiating etta1 and etta2
d_etta=zeros(ne+1,2);       % Initiating d_etta1 and d_etta2
d2_etta=zeros(ne+1,2);      % Initiating d2_etta1 and d2_etta2

% Boundary conditions of the suspension masses in the time domain [t1,t2]
t1=0;           t2=12;          dt=0.0001;

% xs1(t1)=xs1, xs2(t2)=xs2
xs1=0.10;       xs2=0;      
xs=[xs1;xs2];
% xw1(t1)=xw1, xw2(t2)=xw2
xw1=0.20;       xw2=0;     
xw=[xw1;xw2];

% BC after modal transformation:
etta1=Fi'*M*xs;     % ?1=?1'*M*xs
etta2=Fi'*M*xw;     % ?2=?2'*M*xw
BC=[etta1 etta2];

for q=1:2
   
% Coefficients of equation: ax"(t)+bx'(t)+cx(t)=0
a=Mg(q,q);       b=Bg_diag(q,q);      c=Omega(q)^2;    

%% Begin Approximate solution via Galerkin method over each individual element 

% Define element length
le = (t2-t1)/ne; 
% Define t matrix: t=t1:t2
t=t1:le:t2;
t=t';

% Building matrices arrays
K1 = (a/le) * [1,-1;-1,1];      % K1 matrix corresponding to the x"(t)
K2 =  b*[-1/2 1/2;-1/2 1/2];    % K2 matrix corresponding to the x'(t)
K3 =  -c*le*[1/3 1/6;1/6 1/3];  % K3 matrix corresponding to the x(t)
Ke = K1+K2+K3;                  % Element stiffness Matrix

%*****************Begin Assembly Global stiffness matrix*******************
k = zeros(ne+1);
for i=1:ne+1
  for j=1:ne +1
      if (i==j)
          if(i==1)
              k(i,j)=Ke(1,1);
          elseif(i==ne+1)
              k(i,j)=Ke(2,2);
          else
              k(i,j)=Ke(1,1)+Ke(2,2);
          end
      elseif(i==j+1)
          k(i,j)=Ke(1,2);
      elseif(j==i+1)
          k(i,j)=Ke(2,1);
      else
          k(i,j)=0;
      end
  end
end
%********************End Assembly Global stiffness matrix******************

%The Global f Matrix
f = zeros(ne+1,1);
%BC apply xs(t1) = x1
f(1,1) = BC(1,q);
%BC apply xs(t2) = x2
f(ne+1,1) = BC(2,q);

% Display the Global stifness matrix before striking row
K_Global=k;

%Striking first and last rows
for i=2:ne+1
  k(1,i) = 0;
  k(ne+1,i) = 0;
end
k(1,1) = 1;
k(ne+1,ne+1) = 1;


% Display the solvable stifness matrix 
K_strike=k;


%solving the system and finding the modal displacement, etta1(t) and etta2(t)
etta(:,q)=inv(k)*f;

% calculating etta'(t)
for i=1:ne
    d_etta(i,q)=(etta(i+1,q)-etta(i,q))/le;
end

% calculating etta"(t)
for i=2:ne
    d2_etta(i,q)=(d_etta(i+1,q)-d_etta(i,q))/le;
end

end

%% End of solving modal equations


%% Begin calculating displacements, velocity and acceleration

% Calculating x1(t) and x1(t), displacements of the corresponding suspension mass
x1_t=Fi(1,1)*etta(:,1)+Fi(1,2)*etta(:,2);     
x2_t=Fi(2,1)*etta(:,1)+Fi(2,2)*etta(:,2);     

% Sending Displacement values to workspace
assignin('base', 'x1_t', x1_t);       % Sending x1_t to workspace
assignin('base', 'x2_t', x2_t);       % Sending x2_t to workspace

% calculating x1'(t) and x2'(t)
dx1_t=zeros(ne+1,1);
dx2_t=zeros(ne+1,1);
for i=1:ne
    dx1_t(i,1)=(x1_t(i+1)-x1_t(i))/le;
    dx2_t(i,1)=(x2_t(i+1)-x2_t(i))/le;
end
assignin('base', 'dx1_t', dx1_t);       % Sending dx1_t to workspace
assignin('base', 'dx2_t', dx2_t);       % Sending dx2_t to workspace



% calculating x1"(t) and x2"(t)
d2x1_t=zeros(ne+1,1);
d2x2_t=zeros(ne+1,1);
for i=2:ne
    d2x1_t(i,1)=(dx1_t(i+1)-dx1_t(i))/le;
    d2x2_t(i,1)=(dx2_t(i+1)-dx2_t(i))/le;
end
assignin('base', 'd2x1_t', d2x1_t);       % Sending d2x1_t to workspace
assignin('base', 'd2x2_t', d2x2_t);       % Sending d2x2_t to workspace

%% End calculating displacements, velocity and acceleration


%% Begin plotting the results

% Plotting etta1(t) and etta2(t) 
figure1 = figure('Color',[1 1 1],'units','normalized','outerposition',[0 0 1 1]);
subplot(3,2,1)
plot(t,etta(:,1), 'Color','r', 'LineWidth',2);  hold on
xlabel('Time (sec)','FontSize',12);
ylabel('etta(t)   (m)','FontSize',12);
subplot(3,2,1)
plot(t,etta(:,2), '--', 'Color','b', 'LineWidth',2);  hold on
legend1 = legend(subplot(3,2,1),'show');
legend('etta1(t)','etta2(t)')

% Plotting d_etta1(t) and d_etta2(t) 
subplot(3,2,3)
plot(t,d_etta(:,1), 'Color','r', 'LineWidth',2);  hold on
xlabel('Time (sec)','FontSize',12);
ylabel('detta(t)   (m/s)','FontSize',12);
subplot(3,2,3)
plot(t,d_etta(:,2), '--', 'Color','b', 'LineWidth',2);  hold on
legend1 = legend(subplot(3,2,3),'show');
legend('detta1(t)','detta2(t)')

% Plotting d2_etta1(t) and d2_etta2(t) 
subplot(3,2,5)
plot(t,d2_etta(:,1), 'Color','r', 'LineWidth',2);  hold on
xlabel('Time (sec)','FontSize',12);
ylabel('d2etta(t)   (m^2/s)','FontSize',12);
subplot(3,2,5)
plot(t,d2_etta(:,2), '--', 'Color','b', 'LineWidth',2);  hold on
legend1 = legend(subplot(3,2,5),'show');
legend('d2etta1(t)','d2etta2(t)')


% Plotting mass displacements, x1(t) and x2(t) 
subplot(3,2,2)
plot(t,x1_t, 'Color','r', 'LineWidth',2);  hold on
xlabel('Time (sec)','FontSize',12);
ylabel('x(t) (m)','FontSize',12);
subplot(3,2,2)
plot(t,x2_t, '--', 'Color','b', 'LineWidth',2);  hold on
legend1 = legend(subplot(3,2,2),'show');
legend('x1(t)','x2(t)')

% Plotting mass displacements, dx1(t) and dx2(t) 
subplot(3,2,4)
plot(t,dx1_t,  'Color','r', 'LineWidth',2);  hold on
xlabel('Time (sec)','FontSize',12);
ylabel('dx(t) (m)','FontSize',12);
subplot(3,2,4)
plot(t,dx2_t, '--', 'Color','b', 'LineWidth',2);  hold on
legend1 = legend(subplot(3,2,4),'show');
legend('dx1(t)','dx2(t)')

% Plotting mass displacements, d2x1(t) and d2x2(t) 
subplot(3,2,6)
plot(t,d2x1_t, 'Color','r', 'LineWidth',2);  hold on
xlabel('Time (sec)','FontSize',12);
ylabel('d2x(t) (m)','FontSize',12);
subplot(3,2,6)
plot(t,d2x2_t, '--', 'Color','b', 'LineWidth',2);  hold on
legend1 = legend(subplot(3,2,6),'show');
legend('d2x1(t)','d2x2(t)')

%% End of plotting the results

