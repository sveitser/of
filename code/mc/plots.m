close all; clear all;
figure;
%ps = [0.3,0.305,0.3075,0.309,0.31,0.311,0.3125,0.315];
ps = [0.29,0.295,0.299,0.2999,0.3,0.3001,0.301];
hold all;
for i=1:length(ps);
   p = ps(i);
   d=load(['p_',num2str(p),'.dat']);
   [f, x] = ecdf(d);
   plot(x,f);
   leg{i} = ['p = ',num2str(p)];
end

legend(leg)
set(gca,'xscale','log')
xlabel('t')
ylabel('F(t)')