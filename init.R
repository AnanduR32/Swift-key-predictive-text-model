# R script to run author supplied code, typically used to install additional R packages
# contains placeholders which are inserted by the compile script
# NOTE: this script is executed in the chroot context; check paths!

r <- getOption('repos')
r['CRAN'] <- 'http://cloud.r-project.org'
options(repos=r)

# ======================================================================

# packages go here
install.packages('remotes')
install.packages('stringr')


# fiery and friends
install.packages("https://cloud.r-project.org/src/contrib/routr_0.4.0.tar.gz", type="source", repos=NULL)
install.packages("https://cloud.r-project.org/src/contrib/fiery_1.1.2.tar.gz", type="source", repos=NULL)

# dash components
remotes::install_github("plotly/dash-table", ref="042ad65")
remotes::install_github("plotly/dash-html-components", ref="17da1f4")
remotes::install_github("plotly/dash-core-components", ref="cc1e654")
remotes::install_github("plotly/dashR", ref="dev", dependencies=FALSE)