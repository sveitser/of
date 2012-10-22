close all; clear all;
ps = [0.5:0.005:0.55];    
ps = sort(ps);
mfit = zeros(size(ps));
mdata = zeros(size(ps));
mu = zeros(size(ps));
lc = zeros(size(ps));
uc = zeros(size(ps));

for i=1:length(ps);
   p = ps(i);
   try
        d=load(['../data/N_2700_p_',num2str(p),'.dat']);
   catch
       break
   end

   [parms, confs] = gevfit(d)
   
   args = num2cell(parms);
   mfit(i) = gevstat(args{:});
   mdata(i) = mean(d);
   mu(i) = parms(3)
   lc(i) = confs(1,3);
   uc(i) = confs(2,3);
end

figure
ax1 = gca;
hold on
[ax, h1, h2] = plotyy(ps,mu,ps,mdata,@(x,y) ...
    errorbar(x,y,lc-mu,uc-mu,'x'), @(x,y) plot(x,y,'or'));
ylabel('\mu')
xlabel('p')
axes(ax(2));
hold on
xlim([0.4975,0.5525])
linkaxes(ax,'x')
legend('Location parameter \mu','Location','NorthWest');
plot(ps,mfit,'sg','Parent',ax(2));

legend('Fit mean: \mu + \sigma (\Gamma(1+\xi)-1) / \xi','Empirical mean')
title('Generalized Extreme Value Fit Location Parameter \mu with 95% Confidence Intervals')
xlabel('p')
ylabel('m')
box on
