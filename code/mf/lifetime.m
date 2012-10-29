function lambda = lifetime(p, N)

L = zeros(N + 1);

ms = 0:N - 1;
binos = arrayfun(@(m) binopdf(m, N - 1, p), ms);
binosums = cumsum(binos);

for i=1:N
    L(i, i+1) = death(i);
    L(i+1, i) = birth(i - 1);
    if i < N
        L(i+1, i+1) = -(birth(i) + death(i));
    end
end

lambdas = abs(eig(L));
lambda = min(lambdas(lambdas > eps));

    function b = birth(M)
        if M == 0,
            b = 0;
        else
            b = (N-M)/N * binosums(M);
        end
    end

    function d = death(M)
        if M == N,
            d = 0;
        else
            d = M / N * binosums(N - M );
        end
    end
end
