# Plots histograms for adversity fields by ER status

.libPaths(c("R:/Packages3.4", .libPaths()))
library(ggplot2)
library(reshape2)
library(tidyverse)

erBarPlot <- function(df, title, nas) {
	# Returns bar plot of data column by er status
	return(ggplot(df, aes(Values, fill = Type)) + geom_bar(position = "dodge") + 
           ggtitle(title))
}

erHistogram <- function(df, title, nas) {
	# Returns histogram of data column by er status
	return(ggplot(df, aes(Values, fill = Type)) + geom_histogram(bins = 100, position = "dodge") + 
           ggtitle(title))
}

getERColumns <- function(data, col, status, title) {
	# Returns data frame of target column
	ret <- subset(data, ER == status, select = col)
	ret <- na.omit(ret)
	colnames(ret) <- title
	if (title == "ER+") {
	  ret$"ER+" <- sapply(ret$"ER+", as.character)
	  ret$"ER+" <- sapply(ret$"ER+", as.numeric)
	} else {
	  ret$"ER-" <- sapply(ret$"ER-", as.character)
	  ret$"ER-" <- sapply(ret$"ER-", as.numeric)
	}
	return(ret)
}

getControlColumn <- function(data, col) {
	# Returns data frame of control values
	ret <- subset(data, Case == "0", select = col)
	ret <- na.omit(ret)
	colnames(ret) <- "Control"
	ret$Control <- sapply(ret$Control, as.character)
	ret$Control <- sapply(ret$Control, as.numeric)
	return(ret)
}

getDataFrame <- function(data, col, controls) {
	# Returns columns melted into dataframe
	pos <- getERColumns(data, col, "P", "ER+")
	neg <- getERColumns(data, col, "N", "ER-")
	if (controls == TRUE) {
		con <- getControlColumn(data, col)
		ret <- melt(c(pos, neg, con))
	} else {
		ret <- melt(c(pos, neg))
	}
	colnames(ret) <- c("Values", "Type")
	return(ret)
}

countNA <- function(data, col) {
	# Returns count of NA values by ER status
	pos <- subset(data, ER == "P", select = col)
	neg <- subset(data, ER == "N", select = col)
	con <- subset(data, Case == "0", select = col)
	p <- as.numeric(colSums(is.na(pos))) / nrow(pos)
	n <- as.numeric(colSums(is.na(neg))) / nrow(neg)
	co<- as.numeric(colSums(is.na(con))) / nrow(con)
	ret <- data.frame(col, p, n, co)
	colnames(ret) <- c("Field", "ER+", "ER-", "Control")
	return(ret)
}

#-----------------------------------------------------------------------------

plotAges <- function(data, controls) {
	# Saves age related plots to list
	ages <- list()
	amd <- getDataFrame(data, "AgeMaD", controls)
	ages[[1]] <- erBarPlot(amd, "Age at Mother's Death")
	mab <- getDataFrame(data, "MaAgeBr", controls)
	ages[[2]] <- erBarPlot(mab, "Mother's Age at Birth")
	apd <- getDataFrame(data, "AgePaD", controls)
	ages[[3]] <- erBarPlot(apd, "Age at Father's Death")
	pab <- getDataFrame(data, "PaAgeBr", controls)
	ages[[4]] <- erBarPlot(pab, "Fathers's Age at Birth")
	sibs <- getDataFrame(data, "NumSibsDieChildhood", controls)
	ages[[5]] <- erBarPlot(sibs, "Number of Siblings Died During Childhood")
	return(ages)
}

plotSEI <- function(data, controls) {
	# Saves economic index plots to list
	sei <- list()
	mnp <- getDataFrame(data, "MaCenNamPow", controls)
	sei[[1]] <- erHistogram(mnp, "Mother's Nam Powers Score")
	msei <- getDataFrame(data, "MaCenSEI", controls)
	sei[[2]] <- erBarPlot(msei, "Mother's Socio-Economic Index")
	pnp <- getDataFrame(data, "PaCenNamPow", controls)
	sei[[3]] <- erHistogram(pnp, "Fathers's Nam Powers Score")
	psei <- getDataFrame(data, "PaCenSEI", controls)
	sei[[4]] <- erBarPlot(psei, "Fathers's Socio-Economic Index")
	return(sei)
}

plotIncome <- function(data, controls) {
	# Saves income plots to list
	income <- list()
	ei <- getDataFrame(data, "EgoCenIncome", controls)
	income[[1]] <- erHistogram(ei, "Ego's Income")
	mi <- getDataFrame(data, "MaCenIncome_New", controls)
	income[[2]] <- erHistogram(mi, "Mother's Income")
	pi <- getDataFrame(data, "PaCenIncome_New", controls)
	income[[3]] <- erHistogram(pi, "Father's Income")
	return(income)
}

plotHomeVal <- function(data, controls) {
	# Saves home value plots to list
	homeval <- list()
	ehv <- getDataFrame(data, "HomeValue1940_New", controls)
	homeval[[1]] <- erHistogram(ehv, "Ego's 1940 Home Value")
	mhv <- getDataFrame(data, "MaHomeValue1940_New", controls)
	homeval[[2]] <- erHistogram(mhv, "Mother's 1940 Home Value")
	phv <- getDataFrame(data, "PaHomeValue1940_New", controls)
	homeval[[3]] <- erHistogram(phv, "Father's 1940 Home Value")
	return(homeval)
}

plotNAs <- function(data) {
	# Makes bar plot of number of NAs for each field
	nas <- data.frame(matrix(ncol = 4, nrow = 0))
	colnames(nas) <- c("Field", "ER+", "ER-", "Control")
	columns <- c("AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI", 
				"EgoCenIncome", "MaCenIncome_New", "PaCenIncome_New", "HomeValue1940_New", "PaHomeValue1940_New", "MaHomeValue1940_New")
	for (i in columns) {
		count <- countNA(data, i)
		nas <- rbind(nas, count)
	}
	n <- melt(nas)
	svg(file = "Z:/ELCS/histograms/naBarPlot.svg")
	ggplot(n, aes(x = Field, y = value, fill = variable)) + geom_bar(stat = "identity", position = "dodge") +
		ggtitle("Adversity Fields NA Percentages") + ylab("NA Percent") + scale_x_discrete(nas$id) +
	  theme(axis.text.x = element_text(angle = 90, hjust = 1))
	dev.off()
}

# Read csv with blanks as NAs
data <- read.csv("Z:/ELCS/mergedUCRrecords.2019-08-07.csv", na.strings = c("", "NA"))

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
