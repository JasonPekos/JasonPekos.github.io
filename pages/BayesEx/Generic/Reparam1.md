+++
title = "Generic Non-Centred Parameterizations"
hascode = true
hasmath = true
date = Date(2026, 8, 10)
rss = "What's really going on here."
+++
@def tags = ["bayes"]

Recipes from Papaspiliopoulos, Roberts, Sköld (2007). There is a pretty large prior literature here from before the invention of performant modern PPLs like Stan or Pyro. The current userbase of heirarchical Bayesian models specified in PPLs -- I'm thinking mostly of data scientists in industry -- is pretty separate from the then-users of BUGS / JAGS / WINBUGS, so I think it might be worth highlighting some of these results in the context of HMC / industry.

## Generic Non-Centred Parameterizations

Non-centred parameterizations are a common tool for the Bayesian modeller, see [here](https://mc-stan.org/docs/2_18/stan-users-guide/reparameterization-section.html), (link to my own Neal's funnel) page, probably want a third link. It seems like these are originally specified in the context of blocked Gibbs samplers.

These are most often deployed when using location-scale families in heirarchical modelling. But the universe of possible model is large –- often we would like an equivalent parameterization for a model which is not location-scale. The common location scale reparameterization is a nice special case of a general strategy, in which one samples from some "nice" generator distribution, pushing the samples through a map to transform them into the quantity of interest, such that the generator in uncorellated apriori from the rest of parameter space. 


One way to think about this is that, for any set of sampler-visible parameters $\theta$, somewhere in the world there exists $F^{-1}(z)$ such that $F^{-1}$ transports a standard Normal to the correct posterior marginal (see my blog on Doob's h-transform, which I haven't written yet). Sampling from a standard Normal induces an optimal distribution for HMC, so we'd like to move to that world when possible.

Maybe we can't find such a function. But we can do the easier job of finding alternate coordinates (or auxillary variable augementations) that bring us closer to that world. 

## Papaspiliopoulos, Roberts, Sköld

This paper exists in the following setting:

We have data $y$, parameters of interest $\theta$, latent parameters $z$ and hierarchical model:

$$p(\theta, z \mid y) \propto p(\theta \mid z) p(z) p(y \mid \theta)$$

we're interested in the family of possible latent parameterization $z$ such that, after marginalizing out $z$, the
posterior $p(\theta \mid y)$ is unchanged:

$$p(\theta \mid y) \propto \int p(\theta) p(z) p(y \mid \theta, z) dz$$

A parameterization here is some construction where we sample $z^*$ such that, for some function $h$,
we can construct $z = h(z^*, \theta, y)$.
