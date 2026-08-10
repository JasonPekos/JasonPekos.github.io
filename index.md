@def title = "Jason Pekos"
@def showmasthead = false

~~~
<div class="hero">
    <div class="hero-text">
      <p><b>Currently:</b> I lead the modelling team at <a href="https://getrecast.com">Recast Labs Inc</a>, where I work on problems related to efficient gaussian-process approximations inside HMC, causal inference, and validation methods for computationally expensive Bayesian models.</p>
      <p>I'm broadly interested in computational statistics, probabilistic programming systems, procedural art, Julia, and cross-country skiing.</p>
      <p>I may <a href="/menu1/">blog here</a> occasionally on those or other topics!</p>
      <p><b>Formerly:</b> I completed my M.Sc. at McMaster under <a href="https://math.mcmaster.ca/~bolker/">Prof. Ben Bolker</a> in June 2023, specialising in inference for stochastic state-space models of historical plagues.</p>
    </div>

    <figure class="portrait-fig">
      <div class="portrait-wrap" id="portraitWrap" title="hover: the data · click: the program">
        {{gridfig ascii-inverse/portrait id=asciiPortrait class=overlaid inline seed=20260713 label=ASCII_portrait_of_Jason_Pekos,_animated_through_posterior_samples}}
        <div class="photo-reveal" aria-hidden="true"><img id="portraitPhoto" alt="" loading="lazy"></div>
        <div class="code-reveal" aria-label="The Turing.jl model this portrait is a posterior of">
<pre><code><span class="hljs-meta">@model</span> <span class="hljs-keyword">function</span> ascii_model(D, n_cells, n_chars)
    σ ~ Exponential(50.0)
    inv2σ2 = 1.0 / (2.0 * σ^2)
    log_norm = -0.5 * CELL_NPIX * log(2π * σ^2)
    ll = 0.0
    <span class="hljs-keyword">for</span> i <span class="hljs-keyword">in</span> 1:n_cells
        d_row = <span class="hljs-meta">@view</span> D[i, :]
        mx = -minimum(d_row) * inv2σ2
        lse = mx + log(sum(
            exp(-d * inv2σ2 - mx) <span class="hljs-keyword">for</span> d <span class="hljs-keyword">in</span> d_row
        ))
        ll += lse + log_norm - log(n_chars)
    <span class="hljs-keyword">end</span>
    Turing.<span class="hljs-meta">@addlogprob!</span> ll
<span class="hljs-keyword">end</span>

chain = sample(
    ascii_model(D, n_cells, N_CHARS),
    NUTS(), 500,
)</code></pre>
        </div>
      </div>
      <figcaption> <b>Posterior samples</b> from a Turing.jl ascii-inverse model, conditioned on the photograph underneath.</figcaption>
    </figure>
  </div>

  <p class="home-contact"><b>Contact</b>: <code>first.last@gmail.com</code> | <a href="https://github.com/JasonPekos">github</a> | <a href="https://www.linkedin.com/in/jasonpekos/">linkedin</a></p>

<script src="/assets/scripts/ascii-player.js" defer></script>
<script src="/assets/scripts/portrait-hero.js" defer></script>
~~~
