+++
title = "Kieran Graphs"
hascode = true
date = Date(2019, 3, 22)
rss = "neal"
+++
@def tags = ["syntax", "code"]


# General strategy:

Consider a graph, e.g.

```julia:./code/main
using Graphs, Plots, GraphRecipes, Random # Imports # hide
gr() # set backend # hide
plotfont = "Computer Modern"; # Same font as TeX documents for consistency  # hide

default(dpi = 300,            # Crank this up for nicer plots # hide
        size = (800,600),     # Plot size # hide
        grid = false,         # Gridlines # hide
        linewidth=2,          # Thicker lines # hide
        framestyle= :orgin,   # Box around outside of plot (:box, :semi, :orgin, axis ) # hide
        label=nothing,        # Lines by default aren't included in legend, stops y1 ... yn spam. # hide
        fontfamily=plotfont, # hide
        titlefontsize = 20, # hide
        guidefontsize = 13) # hide

simple_graph_1 = path_graph(5) # hide
add_edge!(simple_graph_1, 1, 3); # hide
add_edge!(simple_graph_1, 3, 5); # hide


graphplot(simple_graph_1, # hide
          names = ["01","02","03","04","05"], # hide
          markercolor = :mintcream, # hide
          markersize = 0.2, # hide
          method = :stress); # hide
title!("Simple Graph") # hide

savefig(joinpath(@OUTPUT, "g1.svg")) # hide
```
\fig{g1}

In general, we're going to use the `:circular` method for displaying graphs. This is because the other methods, e.g. `:stress` are stochastic, and they mess up the hack we're using to visualize walks on graphs. So the above graph changes to:


```julia:./code/main
graphplot(simple_graph_1, # hide
          names = ["01","02","03","04","05"], # hide
          markercolor = :mintcream, # hide
          markersize = 0.2, # hide
          method = :circular); # hide
title!("Simple Graph, Alternate Visualization") # hide

savefig(joinpath(@OUTPUT, "g2.svg")) # hide
```
\fig{g2}

This looks a little odd, but it's still the same graph we looked at yesterday. We can easily sample a random walk on this graph from a fixed starting point, e.g. a random walk of length `4` is shown below:


```julia:./code/main

Random.seed!(3) # hide

function makewalksub(nodes::Vector{Int64}) # hide
    sg = DiGraph(10, 0) # numnodes vertices, zero edges # hide
    for index in eachindex(nodes)[2:end] # hide
        add_edge!(sg, nodes[index - 1], nodes[index]); # hide
    end # hide
    return sg # hide
end # hide


rw = randomwalk(simple_graph_1, 1, 4) # start at node 1, walk of length 4 # hide
sub = makewalksub(rw) # hide


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

savefig(joinpath(@OUTPUT, "g3.svg"))  # hide
```
\fig{g3}

We're going to sample a random walk of length `n` for `n` large, e.g. $100'000$ or whatever. From this, we're going to get out a vector of visited nodes, e.g. `[1 2 3 2 1 ...]`. We're going to loop over this vector, returning every primitive even walk that is a subset of this larger walk. Explicitly:

```julia:./code/main
function extractevenwalks(walk::Vector{Int64})
    # This set will store all of our simple even walks. 
    finalset = Set()
    # This set is used for validation because I'm lazy
    validation = Set()

    # Loop over every node in the walk, except for the last one
    for (i1, v1) in enumerate(walk[1:end-1])

        # Wipe set we use to store edges
        edges = Set()

        # For every node, loop over every node after that node in the walk. 
        for (i2, v2) in enumerate(walk[i1 + 1:end])

            # record edge
            edge = Set([walk[i1 + i2 - 1], walk[i1 + i2]])

            # If we've already traversed along this edge, break.
            if edge ∈ edges
                break;
            else
                push!(edges, edge)
            end

            # Check if we've completed a loop.
            if v1 == v2

                # Propose this as a candidate.
                candidate = walk[i1:i2 + i1]

                # If it's even, continue. 
                if length(candidate) % 2 != 0
                    # If it's new, add it to our set
                    if Set(candidate[1:end-1]) ∈ validation
                        break
                    else
                        push!(finalset, candidate)
                        push!(validation, Set(candidate[1:end-1]))
                    end
                    break;
                end
            end
        end
    end
    # Return our set of walks
    return finalset
end
```

This code doesn't accept walks which traverse back along edges we've already visited. We can test this out on the above graph with a walk of length `40`:


```julia:./code/main

n = 40000
rw = randomwalk(simple_graph_1, 1, n) # start at node 1, walk of length n

@show ewset = extractevenwalks(rw) # hide
```

\output{./code/main}

Which can be plotted as:


```julia:./code/main
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
```

\fig{g4}

Which is the desired result. 










