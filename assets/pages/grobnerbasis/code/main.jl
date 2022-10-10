# This file was generated, do not modify it. # hide
sub = makewalksub(first(ewset)) # hide


graphplot(simple_graph_1, # hide
          names = ["01","02","03","04","05"], # hide
          markercolor = :mintcream, # hide
          markersize = 0.2, # hide
          method = :circular); # hide


graphplot!(sub, # hide
          names = ["01","02","03","04","05"],# hide
          markercolor = :mintcream,    # hide
          markersize = 0.2,      # hide
          edgecolor = :red,    # hide
          method = :circular, # hide
          linewidth = 3);    # hide
title!("Random Walk on Simple Graph")    # hide

savefig(joinpath(@OUTPUT, "g4.svg"))  # hide