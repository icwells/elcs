# Plots histograms for adversity fields by ER status

.libPaths(c("R:/Packages3.4", .libPaths()))
library(ggplot2)
library(reshape2)
library(tidyverse)
library(scales)

source("parse.R")
source("plot.R")

# Read csv with blanks as NAs
data <- read.csv("Z:/ELCS/mergedUCRrecords.2019-09-03.csv", na.strings = c("", "NA"))
totals <- "Z:/ELCS/histograms/totalsTables.xlsx"

#--------------------Plot Percents--------------------------------------------

# Plot ages by percent
ages <- percentAges(data, totals)
svg(file = "Z:/ELCS/histograms/ageHistograms_percent.svg")
cowplot::plot_grid(plotlist = ages, nrow = 5)
dev.off()

# Plot SEI data by percent
sei <- percentSEI(data, totals)
svg(file = "Z:/ELCS/histograms/seiHistograms_percent.svg")
cowplot::plot_grid(plotlist = sei, nrow = 4)
dev.off()

# Plot income data by percent
income <- percentIncome(data, totals)
svg(file = "Z:/ELCS/histograms/incomeHistograms_percent.svg")
cowplot::plot_grid(plotlist = income, nrow = 3)
dev.off()

# Plot income data by percent
homeval <- percentHomeValue(data, totals)
svg(file = "Z:/ELCS/histograms/homeValHistograms_percent.svg")
cowplot::plot_grid(plotlist = homeval, nrow = 3)
dev.off()

#--------------------Plot Counts----------------------------------------------

# Plot ages with and without controls
ages <- plotAges(data, TRUE)
svg(file = "Z:/ELCS/histograms/ageHistograms_controls.svg")
cowplot::plot_grid(plotlist = ages, nrow = 5)
dev.off()

ages <- plotAges(data, FALSE)
svg(file = "Z:/ELCS/histograms/ageHistograms_cases.svg")
cowplot::plot_grid(plotlist = ages, nrow = 5)
dev.off()

# Plot economic status data with and without controls
sei <- plotSEI(data, TRUE)
svg(file = "Z:/ELCS/histograms/seiHistograms_controls.svg")
cowplot::plot_grid(plotlist = sei, nrow = 2)
dev.off()

sei <- plotSEI(data, FALSE)
svg(file = "Z:/ELCS/histograms/seiHistograms_cases.svg")
cowplot::plot_grid(plotlist = sei, nrow = 2)
dev.off()

# Plot income data with and without controls
income <- plotIncome(data, TRUE)
svg(file = "Z:/ELCS/histograms/incomeHistograms_controls.svg")
cowplot::plot_grid(plotlist = income, nrow = 3)
dev.off()

income <- plotIncome(data, FALSE)
svg(file = "Z:/ELCS/histograms/incomeHistograms_cases.svg")
cowplot::plot_grid(plotlist = income, nrow = 3)
dev.off()

# Plot home value data with and without controls
homeval <- plotHomeVal(data, TRUE)
svg(file = "Z:/ELCS/histograms/homeValHistograms_controls.svg")
cowplot::plot_grid(plotlist = homeval, nrow = 3)
dev.off()

homeval <- plotHomeVal(data, FALSE)
svg(file = "Z:/ELCS/histograms/homeValHistograms_cases.svg")
cowplot::plot_grid(plotlist = homeval, nrow = 3)
dev.off()
