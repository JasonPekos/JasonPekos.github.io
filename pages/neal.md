+++
title = "neal.md"
hascode = true
date = Date(2019, 3, 22)
rss = "neal"
+++
@def tags = ["syntax", "code"]


# Reparametrization (and some Divergence Diagnostics) in Turing

A full implementation of the code here can be found at [this gist](https://gist.github.com/JasonPekos/65638ff5d19ef2eafb772f8242b911c8).
## What's going on in Stan?

The Stan user's guide has a [helpful section on reparametrization](https://mc-stan.org/docs/2_29/stan-users-guide/reparameterization.html). It's not immediately clear how to implement some of these examples in Turing --- a Stan model is structed as follows:

```Stan
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
Random.seed!(111) # hide

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

simple_chain = sample(Neal(), NUTS(), 5000) # hide

scatter(simple_chain["x[1]"], simple_chain[:y], color = :red, opacity = 0.3, subplot = 1); # hide
title!("Original Parametrization", subplot = 1) # hide 

savefig(joinpath(@OUTPUT, "neal1.svg")) # hide
```
\fig{neal1}

### Divergence Diagnostics in Turing

Turing tags [divergent transition](https://mc-stan.org/docs/reference-manual/divergent-transitions.html) with `numerical_error == 1`. We can quickly check if our chain has any divergences with:

```julia:./code/ex1
sum(simple_chain[:numerical_error])
```

Indicating that we have:
\show{ex1}

divergences. We can add divergences indicators to our posterior sample plot, 
pointing us towards areas of our geometry that are 
problematic:

```julia:./code/ex1
divergences_naive_param = filter(row -> row.numerical_error == 1,
                                 DataFrame(simple_chain))

scatter!(divergences_naive_param[!, "x[1]"],
         divergences_naive_param[!, :y],
         markershape = :x,
         color = :aquamarine,
         opacity = 0.8,
         label = "divergence")
savefig(joinpath(@OUTPUT, "neal1_update.svg")) # hide
```

\fig{neal1_update}

## Ways Forward

Divergent transistions are usually symptoms of some deeper degeneracy, and as such can indicate 
issues with biased inference in your MCMC sampler, non-identifiability in your model, etc.

A guide to taming divergences can be found [here](https://mc-stan.org/misc/warnings.html). 

As discused in the Stan handbook, The most powerful solution is 
usually model reparametrization, which can be done in Turing as follows:

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
rawer_chain = sample(Neal2(), NUTS(), 5000)

raw_chain = Turing.MCMCChains.get_sections(rawer_chain,
                                           :parameters)

reparam_chain = reduce(hcat, generated_quantities(Neal2(), raw_chain))
```

We can check the number of divergences in our reparametrized chain:

```julia:./code/ex1
div = sum(rawer_chain[:numerical_error])
print("Our new parametrization has: ", div, " divergences") # hide
```
\show{ex1}




Plotting, we can see that this allows much better exploration of the funnel:

```julia:./code/ex1
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
```
\fig{neal2}


---

