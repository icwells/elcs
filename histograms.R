# Plots histograms for adversity fields by ER status

.libPaths(c("R:/Packages3.4", .libPaths()))
library(ggplot2)
library(reshape2)
library(tidyverse)

getMode <- function(v) {
  # Returns mode of vector
  u <- unique(v)
  m <- u[which.max(tabulate(match(v, u)))]
  return(m)
}

erHistogram <- function(df, col) {
	# Returns histogram of data column by er status
  xmax <- max(df$Values)
  ymax <- as.numeric(sum(df$Values == getMode(df$Values)))
  return(ggplot(df, aes(Values, fill = Type)) + geom_bar(position = "dodge") + 
           ggtitle(col))
}

getDataFrame <- function(data, col) {
	# Returns columns melted into dataframe
	pos <- subset(data, ER == "P", select = col)
	pos <- na.omit(pos)
	colnames(pos) <- "ER+"
	pos$"ER+" <- as.numeric(pos$"ER+")
	neg <- subset(data, ER == "N", select = col)
	neg <- na.omit(neg)
	colnames(neg) <- "ER-"
	neg$"ER-" <- as.numeric(neg$"ER-")
	#none <- subset(data, ER == "NA", select = col)
	#none <- na.omit(none)
	#colnames(none) <- "NA"
	ret <- melt(c(pos, neg))
	colnames(ret) <- c("Values", "Type")
	return(ret)
}

# Read csv with blanks as NAs
plots <- list()
data <- read.csv("file:///Z:/ELCS/mergedUCRrecords.2019-08-07.csv", na.strings = c("", "NA"))
columns <- c("AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI", 
			"EgoCenIncome", "MaCenIncome_New", "PaCenIncome_New", "HomeValue1940_New", "PaHomeValue1940_New", "MaHomeValue1940_New")

# Set row,column parameter for 15 plots
for (i in 1:length(columns)) {
	# Subset data for each columns and plot
  column <- columns[i]
	df <- getDataFrame(data, column)
	plots[[i]] <- erHistogram(df, column)
}

# Plot by group and save
svg(file = "../ageHistograms.svg")
cowplot::plot_grid(plotlist = plots[1:5], nrow = 5)
dev.off()

svg(file = "../seiHistograms.svg")
cowplot::plot_grid(plotlist = plots[6:9], nrow = 4)
dev.off()

svg(file = "../incomeHistograms.svg")
cowplot::plot_grid(plotlist = plots[10:12], nrow = 3)
dev.off()

svg(file = "../homeValHistograms.svg")
cowplot::plot_grid(plotlist = plots[13:15], nrow = 3)
dev.off()
