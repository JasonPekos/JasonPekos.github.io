+++
title = "RT.md"
hascode = true
date = Date(2023, 4, 22)
rss = "RT"
+++
@def tags = ["syntax", "code"]

# Setting:
The situation here is the following: We want to estimate the prevalence of tumours in a control group of type "F344" rats. In our latest experiment, we have fourteen rats ($n = 14$), and we observe four tumours ($y = 4$).


Additionally, we have historical data from seventy previous experiments, which we can use to inform our model. In total, we have $x_i = 71$ total experiments with $n_i$ rats, and $y_i$ tumours, with
$x_{71}$ being the experiment of primary interest. 

# The Dataset:

We have the following data from Tarone (1982) via BDA3:

\collaps{Dataset: **Press here to expand**}{

| Number of tumors | Number of rats |
|------------------|----------------|
| 0                | 20             |
| 0                | 20             |
| 0                | 20             |
| 0                | 20             |
| 0                | 20             |
| 0                | 20             |
| 0                | 20             |
| 0                | 19             |
| 0                | 19             |
| 0                | 19             |
| 0                | 19             |
| 0                | 18             |
| 0                | 18             |
| 0                | 17             |
| 1                | 20             |
| 1                | 20             |
| 1                | 20             |
| 1                | 20             |
| 1                | 19             |
| 1                | 19             |
| 1                | 18             |
| 1                | 18             |
| 2                | 25             |
| 2                | 24             |
| 2                | 23             |
| 2                | 20             |
| 2                | 20             |
| 2                | 20             |
| 2                | 20             |
| 2                | 20             |
| 2                | 20             |
| 1                | 10             |
| 5                | 49             |
| 2                | 19             |
| 5                | 46             |
| 3                | 27             |
| 2                | 17             |
| 7                | 49             |
| 7                | 47             |
| 3                | 20             |
| 3                | 20             |
| 2                | 13             |
| 9                | 48             |
| 10               | 50             |
| 4                | 20             |
| 4                | 20             |
| 4                | 20             |
| 4                | 20             |
| 4                | 20             |
| 4                | 20             |
| 4                | 20             |
| 10               | 48             |
| 4                | 19             |
| 4                | 19             |
| 4                | 19             |
| 5                | 22             |
| 11               | 46             |
| 12               | 49             |
| 5                | 20             |
| 5                | 20             |
| 6                | 23             |
| 5                | 19             |
| 6                | 22             |
| 6                | 20             |
| 6                | 20             |
| 6                | 20             |
| 16               | 52             |
| 15               | 46             |
| 15               | 47             |
| 9                | 24             |
| 4                | 14             |
}

NumPyro code can be found [here](/pages/BayesEx/BDA3/RatTumor/RTNP).

Turing code can be found here: (TBD)\




