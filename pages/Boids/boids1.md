+++
title = "Boids In Julia - 1"
hascode = true
date = Date(2019, 3, 22)
rss = "boids1"
+++
@def tags = ["syntax", "code"]

\fig{/_assets/boids/output2_excomp.mp4}


[Boids](https://en.wikipedia.org/wiki/Boids) are, per Wikipedia,

> an [artificial life](https://en.wikipedia.org/wiki/Artificial_life "Artificial life") program, developed by [Craig Reynolds](https://en.wikipedia.org/wiki/Craig_Reynolds_(computer_graphics) "Craig Reynolds (computer graphics)") in 1986, which simulates the [flocking](https://en.wikipedia.org/wiki/Flocking_(behavior) "Flocking (behavior)") behaviour of [birds](https://en.wikipedia.org/wiki/Bird "Bird"), and related group motion.

This blog covers a naive implementation of a Boids algorithm in Julia.