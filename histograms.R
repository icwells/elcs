# Plots histograms for adversity fields by ER status

.libPaths(c("R:/Packages3.4", .libPaths()))
library(ggplot2)
library(reshape2)

erHistogram <- function(df, col) {
	# Plots histogram of data column by er status
	ggplot() + geom_bar(data = df, aes(x = "Values", y = "Frequency", fill = variable), position = "dodge", stat = "identity")
}

subsetColumns <- function(data, col, er) {
	# Extracts given columns with er status and nas omitted
	ret <- subset(data, ER == er, select = col)
	return na.omit(ret)
}

getDataFrame <- function(data, col) {
	# Returns columns merged into dataframe
	pos <- subsetColumns(data, i, "P")
	neg <- subsetColumns(data, i, "N")
	none <- subsetColumns(data, i, "NA")
	df <- data.frame(pos, neg, none)
	colnames(df) <- c("ER+", "ER-", "None")
	df <- melt(df, id = "Values")
	return df
}

main <- function() {
	# Read csv with blanks as NAs
	data <- read.csv ("../mergedUCRrecords.2019_08_07.csv", na.strings = c("", "NA"))
	columns <- c("AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", "MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI", 
				"EgoCenIncome", "MaCenIncome_New", "PaCenIncome_New", "HomeValue1940_New", "PaHomeValue1940_New", "MaHomeValue1940_New")

	#svg(file = "adversityHistograms.svg")
	# Set row,column parameter for 15 plots
	par(mfrow=c(3, 5))
	for (i in columns) {
		# Subset data for each columns and plot
		df <- getDataFrame(data, i)
		erHistorgram(df, i)
	}
	#dev.off()
}

main()
