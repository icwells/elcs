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
	bw <- floor(max(df$Values) * 0.01)
	return(ggplot(df, aes(Values, fill = Type)) + geom_histogram(binwidth = bw, position = "dodge") + 
           ggtitle(title))
}

getERColumns <- function(data, col, status , title) {
	# Returns data frame of target column
	ret <- subset(data, ER == status, select = col)
	ret <- na.omit(ret)
	colnames(ret) <- title
	if (title == "ER+") {
	  ret$"ER+" <- sapply(ret$"ER+", as.numeric)
	} else {
	  ret$"ER-" <- sapply(ret$"ER-", as.numeric)
	}
	return(ret)
}

getControlColumn <- function(data, col) {
	# Returns data frame of control values
	ret <- subset(data, Case == "0", select = col)
	ret <- na.omit(ret)
	colnames(ret) <- "Control"
	ret$Control <- sapply(ret$Control, as.numeric)
	return(ret)
}

getDataFrame <- function(data, col) {
	# Returns columns melted into dataframe
	pos <- getERColumns(data, col, "P", "ER+")
	neg <- getERColumns(data, col, "N", "ER-")
	con <- getControlColumn(data, col)
	ret <- melt(c(pos, neg, con))
	colnames(ret) <- c("Values", "Type")
	return(ret)
}

countNA <- function(data, col) {
	# Returns count of NA values by ER status
	pos <- subset(data, ER == "P", select = col)
	neg <- subset(data, ER == "N", select = col)
	con <- subset(data, Case == "0", select = col)
	p <- as.numeric(colSums(is.na(pos)))
	n <- as.numeric(colSums(is.na(neg)))
	co<- as.numeric(colSums(is.na(con)))
	ret <- data.frame(col, p, n, co)
	colnames(ret) <- c("Field", "ER+", "ER-", "Control")
	return(ret)
}

#-----------------------------------------------------------------------------

plotAges <- function(data) {
	# Saves age related plots to file
	ages <- list()
	amd <- getDataFrame(data, "AgeMaD")
	ages[[1]] <- erBarPlot(amd, "Age at Mother's Death")
	mab <- getDataFrame(data, "MaAgeBr")
	ages[[2]] <- erBarPlot(mab, "Mother's Age at Birth")
	apd <- getDataFrame(data, "AgePaD")
	ages[[3]] <- erBarPlot(apd, "Age at Father's Death")
	pab <- getDataFrame(data, "PaAgeBr")
	ages[[4]] <- erBarPlot(pab, "Fathers's Age at Birth")
	sibs <- getDataFrame(data, "NumSibsDieChildhood")
	ages[[5]] <- erBarPlot(sibs, "Number of Siblings Died During Childhood")
	# Save plots to file
	svg(file = "Z:/ELCS/histograms/ageHistograms.svg")
	cowplot::plot_grid(plotlist = ages, nrow = 5)
	dev.off()
}

plotSEI <- function(data) {
	# Saves economic index plots to file
	sei <- list()
	mnp <- getDataFrame(data, "MaCenNamPow")
	sei[[1]] <- erHistogram(mnp, "Mother's Nam Powers Score")
	msei <- getDataFrame(data, "MaCenSEI")
	sei[[2]] <- erBarPlot(msei, "Mother's Socio-Economic Index")
	pnp <- getDataFrame(data, "PaCenNamPow")
	sei[[3]] <- erHistogram(pnp, "Fathers's Nam Powers Score")
	psei <- getDataFrame(data, "PaCenSEI")
	sei[[4]] <- erBarPlot(psei, "Fathers's Socio-Economic Index")
	# Save plots to file
	svg(file = "Z:/ELCS/histograms/seiHistograms.svg")
	cowplot::plot_grid(plotlist = sei, nrow = 2)
	dev.off()
}

plotIncome <- function(data) {
	# Saves income plots to file
	income <- list()
	ei <- getDataFrame(data, "EgoCenIncome")
	income[[1]] <- erHistogram(ei, "Ego's Income")
	mi <- getDataFrame(data, "MaCenIncome_New")
	income[[2]] <- erHistogram(mi, "Mother's Income")
	pi <- getDataFrame(data, "PaCenIncome_New")
	income[[3]] <- erHistogram(pi, "Father's Income")
	# Save plots to file
	svg(file = "Z:/ELCS/histograms/incomeHistograms.svg")
	cowplot::plot_grid(plotlist = income, nrow = 3)
	dev.off()
}

plotHomeVal <- function(data) {
	# Saves home value plots to file
	homeval <- list()
	ehv <- getDataFrame(data, "HomeValue1940_New")
	homeval[[1]] <- erHistogram(ehv, "Ego's 1940 Home Value")
	mhv <- getDataFrame(data, "MaHomeValue1940_New")
	homeval[[2]] <- erHistogram(mhv, "Mother's 1940 Home Value")
	phv <- getDataFrame(data, "PaHomeValue1940_New")
	homeval[[3]] <- erHistogram(phv, "Father's 1940 Home Value")
	# Save plots to file
	svg(file = "Z:/ELCS/histograms/homeValHistograms.svg")
	cowplot::plot_grid(plotlist = homeval, nrow = 3)
	dev.off()
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
		ggtitle("Adversity Fields NA Counts") + xlab("NA Count") + scale_x_discrete(nas$id) +
	  theme(axis.text.x = element_text(angle = 90, hjust = 1))
	dev.off()
}

# Read csv with blanks as NAs
data <- read.csv("Z:/ELCS/mergedUCRrecords.2019-08-07.csv", na.strings = c("", "NA"))

plotAges(data)
plotSEI(data)
plotIncome(data)
plotHomeVal(data)
