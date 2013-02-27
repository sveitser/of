#
#   gradual_rewiring.jl
#

function rewire(fun::Function, states::Array{Int,1}, A::Array{Float64,2})
    equal = abs(states * states')
    return A + map(fun, equal)
end

function rewire(fun::Function, i::Int, states::Array{Int,1},
                A::Array{Float64,2})
    A[:, i] = [fun(states[i], states[j] , A[i, j]) for j in 1:length(states)]
    A[i, :] = A[:, i]'
    A[i, i] = 0
    return A
end

function update(states::Array{Int, 1}, A::Array{Float64,2}, m::Float64)
   i = randi(length(states))
   m -= states[i] / length(states)
   states[i] = iround(sign(mean(A[:,i] .* states)))
   if states[i] == 0
       states[i] = 2 * randbit() - 1
   end
   m += states[i] / length(states)
end

function connected_components(A)
    B = A .> eps()
    D = diagm(sum(B,1))
    L = D - B 
    val, vec = eig(L)
    println(sort(abs(val)))
    return sum(abs(val) .< 1e-9)
end

function run()
    N = 100
    A = zeros(N,N)
     
    tmax = 100
    ep = 0.1
    states = 2 * randbit(N) - 1
    m = mean(states)
    r = 0.1
    for t in 1:tmax * N
        if rand() < r
            rewire((a, b, l) -> min(max(l + a * b * ep, 0), 1),
                   randi(N), states, A)
        else
            update(states, A, m)
            if m < 1 / N || m > 1 - 1 / N
                break
            end
        end
    end
    println("m: ",m)
    c = connected_components(A)
    println("components: ", c)
end

