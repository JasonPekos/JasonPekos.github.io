+++
title = "turingpitfalls.md"
hascode = true
date = Date(2019, 3, 22)
rss = "tpf"
+++
@def tags = ["syntax", "code"]

# Random Variables vs Observations

Here’s an issue that I’d occasionally run into: sometimes, it seems like operations on an array in my model (specifically, the array of data I want to condition on) ruins the performance of my sampler. As an example, consider the following skeleton of a spline model. 

```julia
@model function spline(data)
    # unpack x and y 
    x = data[:,1]
    y = data[:,2]

    # use x to create b-spline basis

    # likelihood
    y[i] ~ normal around spline output or something similar 
    ... (cont)
```

This will produce pretty bizzare chains that don't seem to sample from the correct posterior. Changing this to:

```julia
@model function spline(x, y) #  <- CHANGE IS HERE IN THE FUNCTION SIGNATURE
    # use x to create b-spline basis

    y[i] ~ normal around spline output or something similar 
    ... (cont)
```

Will work perfectly. Asking around on the slack, Tor Fjelde points out the following:

> The reason why you're seeing an issue here is because `x` and `y` aren't treated as observations in the first model 
> A Turing model is very "dumb": something is considered an observation/something to condition on if it is either a raw value, e.g. `1`, or if the variable on the LHS of a `~` is present in the model arguments. In your first model, `x` and `y` aren't actually present in your arguments and so these will be considered random variables.
