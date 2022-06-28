# This file was generated, do not modify it. # hide
p = plot(layout = 2); # hide
scatter!(simple_chain["x[1]"], simple_chain[:y], color = :red, opacity = 0.3, subplot = 1); # hide
title!("Original Parametrization", subplot = 1) # hide
scatter!(reparam_chain[1, 1:end], reparam_chain[10, 1:end], color = :blue, opacity = 0.3, subplot= 2); # hide
title!("Reparametrized", subplot = 2) # hide

savefig(joinpath(@OUTPUT, "neal2.svg")) # hide