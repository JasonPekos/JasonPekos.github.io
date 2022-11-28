#=
Neal's funnel
https://mc-stan.org/docs/2_29/stan-users-guide/reparameterization.html#ref-papa-et-al:2007
=#
using Turing, StatsPlots, Distributions, DataFrames, RCall

gr() # set backend



@model function Neal()
    y ~ Normal(0,3)
    x ~ arraydist([Normal(0, exp(y/2)) for i in 1:9])
end

simple_chain = sample(Neal(), NUTS(), 10_000)

p = plot(layout = 2);
scatter!(simple_chain["x[1]"], simple_chain[:y], color = :red, opacity = 0.3, subplot = 1);
title!("Original Parametrization", subplot = 1)

################################################################################### REPARAM

@model function Neal2()
    # raw draws
    y_raw ~ Normal(0,1)
    x_raw ~ arraydist([Normal(0, 1) for i in 1:9])

    # transform:
    y = 3*y_raw
    x = exp.(y./2) .* x_raw

    # return:
    return [x; y]
end

rawer_chain = sample(Neal2(), NUTS(), 10_000)
raw_chain = Turing.MCMCChains.get_sections(rawer_chain, :parameters)

reparam_chain = reduce(hcat, generated_quantities(Neal2(), raw_chain))

sum(simple_chain[:numerical_error])

divergences_reparam = rawer_chain[:numerical_error]
divergences_naive_param = filter(row -> row.numerical_error == 1, DataFrame(simple_chain))

scatter!(divergences_naive_param[!, "x[1]"],
         divergences_naive_param[!, :y],
         subplot = 1, markershape = :x,
         color = :aquamarine,
         opacity = 0.8)

scatter!(reparam_chain[1, 1:end],
         reparam_chain[10, 1:end],
         color = :blue, opacity = 0.3,
         subplot= 2);
title!("Reparametrized", subplot = 2)



