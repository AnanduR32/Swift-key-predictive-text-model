# R script to run author supplied code, typically used to install additional R packages
# contains placeholders which are inserted by the compile script
# NOTE: this script is executed in the chroot context; check paths!

r = getOption('repos')
r['CRAN'] = 'http://cloud.r-project.org'
options(repos=r)

# ======================================================================

# packages go here
install.packages('remotes')
install.packages('stringr')


# fiery and friends
install.packages(c("fiery", "routr", "reqres", "htmltools", "base64enc", "plotly", "mime", "crayon", "devtools"))

# dash components
# installs dashHtmlComponents, dashCoreComponents, and dashTable
# and will update the component libraries when a new package is released
devtools::install_github("plotly/dashR", ref="dev", upgrade = TRUE)