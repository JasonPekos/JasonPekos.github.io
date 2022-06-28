+++
title = "neal.md"
hascode = true
date = Date(2019, 3, 22)
rss = "neal"
+++
@def tags = ["syntax", "code"]


# Reparametrization

A full implementation of the code here can be found at [this gist](https://gist.github.com/JasonPekos/65638ff5d19ef2eafb772f8242b911c8).
## What's going on in Stan?

The Stan user's guide has a [helpful section on reparametrization](https://mc-stan.org/docs/2_29/stan-users-guide/reparameterization.html). It's not immediately clear how to implement some of these examples in Turing --- a Stan model is structed as follows:

```stan
data {
  
}
transformed data {
  
}
parameters {
  
}
transformed parameters { # Look here !
  
}
model {
  
}
```

With a specific block for tracking transformed variables. As far as I can tell, no such option exists in Turing. Here's what I've settled on so far: 

## Turing implementation

We can set up the classic Neal's funnel example in Turing like this:

```julia:./code/ex1
using Turing, StatsPlots, Distributions, DataFrames # hide
gr() # set backend # hide

@model function Neal()
    y ~ Normal(0,3)
    x ~ arraydist([Normal(0, exp(y/2)) for i in 1:9])
end
```

Where sampling with the default `NUTS()` option returns:

```julia:./code/ex1
using Turing, StatsPlots, Distributions, DataFrames # hide
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

simple_chain = sample(Neal(), NUTS(), 1000) # hide

scatter(simple_chain["x[1]"], simple_chain[:y], color = :red, opacity = 0.3, subplot = 1); # hide
title!("Original Parametrization", subplot = 1) # hide 

savefig(joinpath(@OUTPUT, "neal1.svg")) # hide
```
\fig{neal1}



Reparametrizing can be done in Turing as follows:

```julia:./code/ex1
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
```

Where we use the `generated_quantities()` function to pull out the transformed variables:

```julia:./code/ex1
raw_chain = Turing.MCMCChains.get_sections(sample(Neal2(),
                                           NUTS(), 1000),
                                           :parameters)

reparam_chain = reduce(hcat, generated_quantities(Neal2(), raw_chain))
```

Plotting, we can see that this allows much better exploration of the funnel:

```julia:./code/ex1
p = plot(layout = 2); # hide
scatter!(simple_chain["x[1]"], simple_chain[:y], color = :red, opacity = 0.3, subplot = 1); # hide
title!("Original Parametrization", subplot = 1) # hide
scatter!(reparam_chain[1, 1:end], reparam_chain[10, 1:end], color = :blue, opacity = 0.3, subplot= 2); # hide
title!("Reparametrized", subplot = 2) # hide

savefig(joinpath(@OUTPUT, "neal2.svg")) # hide
```
\fig{neal2}


The above code does the following:
- In our model `Neal2()`, we transform the variables, and then ask the model to return the resulting output. 
- `generated_quantities()` then takes in a `chains` object, notes what we sampled for our untransformed variables, and then runs the model forward with those values, outputting whatever is in the `return` statement for each sample in our chain.
- We squash this down into a matrix for easier plotting.

This seems pretty rough, but it's the best I've got. 
