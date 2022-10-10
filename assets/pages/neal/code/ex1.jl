# This file was generated, do not modify it. # hide
# Plot size # hide

p = plot(layout = 2, size = (800, 600)); # hide
scatter!(simple_chain["x[1]"], simple_chain[:y], color = :red, opacity = 0.3, subplot = 1); # hide
title!("Original Parametrization", subplot = 1) # hide
scatter!(reparam_chain[1, 1:end], reparam_chain[10, 1:end], color = :blue, opacity = 0.3, subplot= 2); # hide
title!("Reparametrized", subplot = 2)     # Plot size # hide) # hide

scatter!(divergences_naive_param[!, "x[1]"], # hide
         divergences_naive_param[!, :y], # hide
         markershape = :x, # hide
         subplot = 1, # hide
         color = :aquamarine,# hide
         opacity = 0.8,# hide
         label = "divergence")# hide

savefig(joinpath(@OUTPUT, "neal2.svg")) # hide