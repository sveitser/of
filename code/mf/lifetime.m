function lambda = lifetime(p, N)

L = zeros(N);

for i=1:N-1
    L(i, i+1) = death(p, N, i);
    L(i+1, i) = birth(p, N, i - 1);
    if N < N-1
        L(i+1, i+1) = -(birth(p, N, i) + death(p, N, i));
    end
end

L

end

function b = birth(p, N, M)
    ns = 0: M - 1;
    b = (N - M) / N * sum(arrayfun(@(n) B(N - 1, p, n), ns));
end

function d = death(p, N, M)
   ns = 0:N - M - 1;
   d = M/N * sum(arrayfun(@(n) B(N - 1, p, n), ns));
end

function b = B(N, p, l)
    b = nchoosek(N,l) * p^l * (1-p)^(N-l);
end