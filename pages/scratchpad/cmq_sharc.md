+++
title = "Using ClusterMQ on Sharcnet via SSH"
hascode = true
date = Date(2023, 6, 17)
rss = "cmq_sharc"
+++
@def tags = ["syntax", "code"]

# What's this about?

This is a guide to using ClusterMQ on Sharcnet via SSH. It's a work in progress — let me know if something is unclear! The goal of this is to get you to the point where you can submit jobs using the `Q()` function from a local machine. 


## Installing ClusterMQ and ZeroMQ locally 

What you do here depends on your local machine. A complete guide can be found [here](https://mschubert.github.io/clustermq/articles/userguide.html#installation).

## Installing ClusterMQ and ZeroMQ on the cluster 

The ComputeCanada clusters should already have ZeroMQ installed. You should install ClusterMQ in the R module you plan on using by
starting a session and running:

```R
install.packages("clustermq")
```

# Setting up your R profiles and Slurm template

## On your local machine
You need to add the following to your local `.Rprofile` file. You can find this file by running `file.edit("~/.Rprofile")` in R. If the file doesn't exist, create it in your home directory.


```R
options(
    clustermq.scheduler = "ssh",
    clustermq.ssh.host = "user@host", # e.g. bob@graham.computecanada.ca
    clustermq.ssh.log = "~/cmq_ssh.log" # ssh log location
)
```

## On the cluster
You need to add the following to your cluster `.Rprofile` file. You can find this file in your home directory:

```R
options(
    clustermq.template = "/path_to_file/slurm.tmpl"
)
```

You also need to create a `.tmpl` file (in the example above, this is `slurm.tmpl`) in the same directory. Here's an example, taken from of I use (via mschubert):

```bash
#!/bin/sh

# Modified from https://github.com/mschubert/clustermq/blob/master/inst/SLURM.tmpl
# under the Apache 2.0 license.

#SBATCH --job-name=superconservative_halcyon_{{ job_name }}
#SBATCH --output={{ log_file | /dev/null }}
#SBATCH --error={{ log_file | /dev/null }}
#SBATCH --mem-per-cpu={{ memory | 3G }}
#SBATCH --array=1-{{ n_jobs }}
#SBATCH --cpus-per-task={{ cores | 4 }}
#SBATCH --account=ACCOUNT NAME YOU WANT GOES HERE e.g. def-abc <--- change this
#SBATCH --time=0-00:10  <--- change this

module load R # Comment out if R is not an environment module.
# ulimit -v $(( 1024 * {{ memory | 3G }} ))
CMQ_AUTH={{ auth }} R --no-save --no-restore -e 'clustermq:::worker("{{ master }}")'
```

## Also on the cluster --- Adding the R module you want to your bashrc.

You need to add the R module you want to use to the end of your bashrc. If you don't, you'll fail with

```bash
Error in initialize(...) : 
  Remote R process did not respond after 5000 seconds. Check your SSH server log.
```

For example, I use the following:

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
module load r/4.2.2 # <--- this is the line you need to add
```

# Testing if this works:

The following should work (you'll be prompted for your password or ssh key):

```R
library(clustermq)

fx = function(x) x * 2

Q(fx, x=1:3, n_jobs=1)


```