+++
title = "Using sf or geojsonio on ComputeCanada Clusters"
hascode = true
date = Date(2023, 6, 17)
rss = "cmq_sharc"
+++
@def tags = ["syntax", "code"]

# What's the problem?

When you try to use `sf` or `geojsonio` on a ComputeCanada cluster, you might get an error like this:

```
-----Error: libudunits2.a not found-----
     If the udunits2 library is installed in a non-standard location,
     use --configure-args='--with-udunits2-lib=/usr/local/lib' for   
     example,
     or --configure-args='--with-udunits2-include=/usr/include/udunits2'
     replacing paths with appropriate values for your installation.
     You can alternatively use the UDUNITS2_INCLUDE and UDUNITS2_LIB
     environment variables.
     If udunits2 is not installed, please install it.
     It is required for this package.
     ERROR: configuration failed for package ‘udunits2’
```
...
```
 installation of package ‘udunits2’ had non-zero exit status
```

When this happens, the issue is that you haven't loaded the udunits2 module. You should run the following code before you open R to
run your `install.packages()` command.

```bash
module load udunits/2.2.26
module load StdEnv/2020  gcc/9.3.0
module load gdal/3.5.1
```