+++
title = "mixtures1.md"
hascode = true
date = Date(2023, 4, 22)
rss = "mixtures1"
+++
@def tags = ["syntax", "code"]

# Mixture Models For The Old Faithful Dataset

The Old Faithful dataset is a pretty classic mixture model example (see, e.g. Bishop PRML). There are a couple 
of different version of this --- I'll use the one from the `RDatasets.jl` package.

```julia
old_faithful = dataset("datasets", "faithful")
```

We can plot the data:


## EDA
\fig{/_assets/oldfaithful/p1.svg}

\collaps{**Click Me** For Plotting Code}{
```julia
l = @layout [a{0.7w} b{0.3w}; c{0.7h} d{0.3h}]

# Main scatter plot
p1 = scatter(old_faithful.Eruptions, 
             old_faithful.Waiting,
             color = 3,
             legend = false,
             xlabel = "Eruption time (minutes)",
             ylabel = "Waiting time (minutes)");

# Horizontal histogram for waiting time
p2 = histogram(old_faithful.Waiting, 
               color = 3, 
               orientation = :horizontal,
               legend = false,
               title = "",
               bins = 30,
               ylims = (minimum(old_faithful.Waiting), maximum(old_faithful.Waiting)),
               yaxis = false,
               xaxis = false);

# Upside-down histogram for eruption time
p3 = histogram(old_faithful.Eruptions,
               color = 3,
               title = "",
               yflip = true,
               xlims = (minimum(old_faithful.Eruptions), maximum(old_faithful.Eruptions)),
               yaxis = false,
               xaxis = false,
               bins = 30,
               legend = false);

# Placeholder for alignment 
p4 = plot(legend = false, axis = false, grid = false, foreground_color_subplot=:white);

# Combine plots with adjusted layout
plot(p1, p2, p3, p4, layout = l, size=(600, 600))
```
**Note:** As of `Plots.jl` version `1.39.0`, `orientation = :horizontal` does not swap the xlims, so you
need to do this manually.
}

## Model One: 1D Mixture Model

Let's implement a simple one-dimensional mixture of Gaussians for the eruption time data:

```julia


```




