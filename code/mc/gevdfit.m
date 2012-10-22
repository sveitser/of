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
        d=load(['N90_p_',num2str(p),'.dat']);
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
%errorbar(ps,mu,lc-mu,uc-mu,'x')
[ax, h1, h2] = plotyy(ps,mu,ps,mdata,@(x,y) plot(x,y,'x'))
axes(ax(1)); hold on;
errorbar(ps,mu,lc-mu,uc-mu,'x');
axes(ax(2)); hold on;
ylabel('\mu')
xlabel('p')
legend('Location parameter \mu','Location','NorthWest');
%ax2 = axes('Position',get(ax1,'Position'),...
%       'XAxisLocation','top',...
%       'YAxisLocation','right',...
%       'Color','none',...
%       'XColor','k','YColor','k');
%linkaxes([ax1 ax2],'x');
%hold on
plot(ax(2),ps,mdata,'or','Parent',ax2);
plot(ax(2),ps,mfit,'sg','Parent',ax2);

legend('Fit mean: \mu + \sigma (\Gamma(1+\xi)-1) / \xi','Empirical mean')
title('Generalized Extreme Value Fit Location Parameter \mu with 95% Confidence Intervals')
xlabel('p');
ylabel('m');

box on
axis('tight')
