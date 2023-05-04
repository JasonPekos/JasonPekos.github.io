+++
title = "bio1.md"
hascode = true
date = Date(2023, 4, 22)
rss = "bio1"
+++
@def tags = ["syntax", "code"]



# The Dataset:

This is the classic bioassay example from BDA3, originally via Racine et al. (1986). The data are the number of deaths in 4 groups of 5 rats, each of which were given a different dose of a drug. The goal is to estimate the dose-response curve and the LD50, the dose at which 50% of the rats die.


| Dose (log g/ml) | Number of Rats | Number of Deaths |
|-----------------|----------------|------------------|
| -0.86           | 5              | 0                |
| -0.30           | 5              | 1                |
| -0.05           | 5              | 3                |
| 0.73            | 5              | 5                |


---

Turing code can be found here: (TBA)\


NumPyro code can be found [here](/pages/BayesEx/BDA3/BioAssay1/b1NP).

