using Turing, Distributions, StatsPlots, Random, DataFrames
plotfont = "Computer Modern"; # Same font as TeX documents for consistency  # hide
default(dpi = 300,            # Crank this up for nicer plots 
        size = (800,600),     # Plot size # hide
        grid = false,         # Gridlines 
        linewidth=2,          # Thicker lines 
        framestyle= :orgin,   # Box around outside of plot (:box, :semi, :orgin, axis ) 
        label=nothing,        # Lines by default aren't included in legend, stops y1 ... yn spam. 
        fontfamily=plotfont, 
        titlefontsize = 20, 
        guidefontsize = 13) 


function NegativeBinomial2(mean, dispersion)
    var = mean + 1 / dispersion * mean^2
    p = (var - mean) / var


    return NegativeBinomial(dispersion, 1 - p)
end

mean(rand(NegativeBinomial2(9,0.1), 100000))

@model function chain_binom(inc, pop, δt)
    dispersion ~ Exponential(4)
    β = 0.2
    p_inf ~ Beta(1,1)
    I_init ~ Binomial(pop, p_inf)

    I = Vector(undef, length(inc))
    S = Vector(undef, length(inc))
    S[1] = pop

    I[1] = I_init
    S[1] = pop - I[1]

    inc[1] ~  NegativeBinomial2(I[1], dispersion)
    for t in 2:length(inc)
        I[t] ~ Binomial(S[t-1], -expm1(-β * I[t-1]))
        S[t] = S[t-1] - I[t]
        if I[t] > 0
            inc[t] ~ NegativeBinomial2(I[t], dispersion)
        else
            inc[t] ~ NegativeBinomial2(1e-30, dispersion)
        end
    end
    return I
end

chain = sample(chain_binom(zeros(5), 20, 1), Prior(), 100)

gq =  generated_quantities(chain_binom(zeros(5), 20, 1), chain)
p = plot();
for i in 1:100
    plot!(gq[i], opacity = 0.1, color = :red)
end
p

