#
#   gradual_rewiring.jl
#

# blah up
function rewire(fun::Function, states::Array{Int,1}, A::Array{Float64,2})
    equal = abs(states * states')
    return A + map(fun, equal)
end

function rewire(fun::Function, i::Int, states::Array{Int,1},
        A::Array{Float64,2})
    A[:,i] = map(j -> fun(states[i], states[j] , A[i,j]), 1:N)
    A[i,:] = A[:,i]'
    return A
end

#function update(states::Array{Int, 1} 

function run( )
    N = 100
    A = ones(N,N) - eye(N)
    tmax = 100
    ep = 0.01
    states = randbit(N)
    for t in 1:tmax
        for i in 1:N
            A = rewire(i -> min(max(x + (x - 0.5) * ep, 0, 1)),
                randi(N), states, A)
        end
        print(A)
    end
end

