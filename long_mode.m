n=0;
m=2;
L=5;
x00=0;
xll=1;
x22=2;
x33=3;
x44=4; 
x55=5;
ti=1;
i=1;
dtheta=2*pi/50;
dtime=2*pi/20;


for time=0:dtime:2*pi-.0001
    for theta=0:dtheta:2*pi-.0001
        x0(1,i)=x00+.1*cos(m*pi/L*x00)*cos(n*theta)*cos(time);
        y0(1,i)=sin(theta);
        z0(1,i)=cos(theta);
        x1(1,i)= xll+.1*cos(m*pi/L*xll)*cos(n*theta)*cos(time);
        y1(1,i)=sin(theta);
        z1(1,i)=cos(theta);

        x2(1,i)=x22+.1*cos(m*pi/L*x22)*cos(n*theta)*cos(time);
        y2(1,i)=sin(theta);
        z2(1,i)=cos(theta);

        x3(1,i)=x33+.1*cos(m*pi/L*x33)*cos(n*theta)*cos(time);
        y3(1,i)=sin(theta);
        z3(1,i)=cos(theta);
        x4(1,i)=x44+.1*cos(m*pi/L*x44)*cos(n*theta)*cos(time);
        y4(1,i)=sin(theta);
        z4(1,i)=cos(theta);
        x5(1,i)=x55+.1*cos(m*pi/L*x55)*cos(n*theta)*cos(time);
        y5(1,i)=sin(theta);
        z5(1,i)=cos(theta);
        i=i+1;
   end
    
view([-15 10]);
figrue(1);
    set(1,'Position',[150,150,700,500]);
    set(1,'Visible','off');
    axis([-l L+l -2 2 -2 2]);
    axis manual
    hold on
pl=plot3(x0,y0,z0,'r','LineStyle','none','Marker','.','EraseMode','xor');
p2=plot3(x1,y1,z1,'b', 'LineStyle','none','Marker','.','EraseMode','xor');
p3=plot3(x2,y2,z2,'g','LineStyle','none','Marker','.','EraseMode','xor');
p4=plot3(x3,y3,z3,'r','LineStyle','none','Marker','.','EraseMode','xor');
p5=plot3(x4,y4,z4,'b','LineStyle','none','Marker','.','EraseMode','xor');
p6=plot3(x5,y5,z5,'g','LineStyle','none','Marker','.','EraseMode','xor');
%     grid on;
%     hold off;
%     F(:,ti)= getframe;
%     hold off;
%     ti=ti+l;
%     i=l;
% %     delete(pl,p2,p3,p4,p5,p6);
end

% close((l));
% pause(2);
% view([-15 10]);
% figure(1);
% set(l,Position',[150,150,700,500]);
% axis([-l L+l -2 2 -2 2]);
% axis manual;
% xlabel=(Y);
% movie(F, 5,50);
%% 

% n=l;
% m=l;
% dtheta=2*pi/50;
% dtime=2*pi/20;
% L=5;
% x00=0;
% xll=l;
% x22=2;
% x33=3;
% x44=4;
% x55=5;
% ti=l;
% i=l;
% for time=0:dtime:2*pi-.0001
% for theta=0:dtheta:2*pi-.0001
% x0(l,i)=x00;
% yO(l,i)=sin(.1 *sin(m*pi/L*xOO)*sin(n*theta)*cos(time)+theta);
% zO(l,i)=cos(.1 *sin(m*pi/L*xOO)*sin(n*theta)*cos(time)+theta);
% xl(l,i)=xll;
% yl(l,i)=sin(.1*sin(m*pi/L*xll)*sin(n*theta)*cos(time)+theta);
% zl(l,i)=cos(.1 *sin(m*pi/L*xll)*sin(n*theta)*cos(time)+theta);
% x2(l,i)=x22;
% y2(l,i)=sin(.1 *sin(m*pi/L*x22)*sin(n*theta)*cos(time)+theta);
% z2(l,i)=cos(.1*sin(m*pi/L*x22)*sin(n*theta)*cos(ume)+theta);
% x3(l,i)=x33;
% y3(l,i)=sin(.1 *sin(m*pi/L*x33)*sin(n*theta)*cos(time)+theta);
% z3(l,i)=cos(.1*sin(m*pi/L*x33)*sin(n*theta)*cos(time)+theta);
% x4(l,i)=x44;
% y4(l,i)=sin(.1*sin(m*pi/L*x44)*sin(n*theta)*cos(time)+theta);
% z4(l,i)=cos(.1*sin(m*pi/L*x44)*sin(n*theta)*cos(time)+theta);
% x5(l,i)=x55;
% y5(l,i)=sin(.1*sin(m*pi/L*x55)*sin(n*theta)*cos(time)+theta);
% z5(l,i)=cos(.1*sin(m*pi/L*x55)*sin(n*theta)*cos(time)+theta);
% i=i+l;
% end
% view([-15 10])
% Figure(l);
% set(l/Position',[150,150,700,500]);
% set(l,'VisibleVoff');
% axis([-l L+l -2 2 -2 2]);
% axis manual
% hold on
% pl=plot3(x0,y0,z0,'r','LineStyle','none','Marker','.','VEraseMode','xor');
% p2=plot3(xl,yl,zl,'b', 'LineStyle','none','Marker','.','EraseMode','xor');
% p3=plot3(x2,y2,z2,'g','LineStyle','none','Marker','.','EraseMode','xor');
% p4=plot3(x3,y3,z3,'r','LineStyle','none','Marker','.','EraseMode','xor');
% p5=plot3(x4,y4,z4,'b','LineStyle','none','Marker','.','EraseMode','xor');
% p6=plot3(x5,y5,z5,'g','LineStyle','none','Marker','.','EraseMode','xor');
% grid on
% hold off
% F(:,ti)=getframe(l,[91,55,700,500]);
% ti=ti+l;
% i=l;
% delete(pl,p2,p3,p4,p5,p6);
% end
% close((l))
% pause(2)
% view([-15 10])
% Figure(1);
% set(l,Position',[150,150,700,500]);
% axis([-l L+l -2 2 -2 2]);
% axis manual
% xlabel=('x');
% movie(F, 10,50);
% %clear all