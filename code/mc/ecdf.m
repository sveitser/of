close all; clear all;
ps = [0.285,0.29,0.3,...
      0.5,0.95];
figure;
hold all;
ps = sort(ps);
mfit = zeros(size(ps));
mdata = zeros(size(ps));
mu = zeros(size(ps));
lc = zeros(size(ps));
uc = zeros(size(ps));

st = 'xod+^sxod+^sxod+^sxod+^s';
for i=1:length(ps);
   p = ps(i);
   try
        d=load(['p_',num2str(p),'.dat']);
   catch
       break
   end
   
   [f, x, fl, fu] = ecdf(d);
   plot(x,f,st(i));
   
   leg{i} = ['p = ',num2str(p)];
end

%%% ecdf plot
legend(leg)
set(gca,'xscale','log')
axis('tight')
ylabel('ECDF')
xlabel('p')
