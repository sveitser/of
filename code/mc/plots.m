ps = [0.3,0.31,0.32,0.5];
st = 'rkmbgc';
for i=1:length(ps);
   p = ps(i);
   d=load(['p_',num2str(p),'.dat']);
   [f, x] = ecdf(d);
   hold on;
   plot(x,f,st(i));
   leg{i} = ['p = ',num2str(p)];
end

legend(leg)
set(gca,'xscale','log')
xlabel('t')
ylabel('F(t)')