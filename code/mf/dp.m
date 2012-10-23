%
%   plots meanfield time derivative of m
%
clear all; close all;
p=0:0.01:1;
m=0:0.01:1;
dpm=zeros(length(m),length(p));
for i=1:length(p)
    for j=1:length(m)
        dpm(i,j) = (1-m(j))*heaviside(m(j)-p(i)) - m(j)*heaviside(1-p(i)-m(j));
    end
end

figure
pcolor(p,m,dpm);
shading flat
xlabel('m')
ylabel('p')