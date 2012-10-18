#
# opinion formation 
#
N = 900
dN = 1 / N
tmax = 20
n = 3
p = 0.4
q = 1 - p
eta = 10

normalize(x) = x * eta / N

p = normalize(p)
q = normalize(q)

s = zeros(Int32, N)

for i = 1:n
    s[1 + int((i - 1) * N / n):i * int(N / n)] = i
end


m = zeros(n) + 1/n
mt = zeros(tmax+1,n)
mt[1,:] = m

for i = 1:tmax
    for j = 1:N
        a = randi(N)
        oa = s[a]
        r = rand(N)
        same_op = (s - oa) .== 0
        v = p * same_op + q * !same_op
        neis = r .< v
        neiops = s[neis]
        nop = zeros(n)
        for k = 1:n
            nop[k] = sum(neiops .== k)
        end
        
        maxop_ar = find(nop .>= max(nop))
        
        if length(maxop_ar) > 1
            continue
        else
            maxop = maxop_ar[1]
            m[oa] -= dN
            m[maxop] += dN
            s[a] = maxop
        end
        
    end
        
    mt[i + 1,:] = m
    println(m)

end

for i = 1:n
    plot(mt[:,i])
end
