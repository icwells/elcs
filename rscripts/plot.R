# Plotting functions for historgrams.R

erBarPlot <- function(df, title) {
	# Returns bar plot of data column by er status
	return(ggplot(df, aes(Values, fill = Type)) + geom_bar(position = "dodge") + 
           ggtitle(title))
}

erHistogram <- function(df, title) {
	# Returns histogram of data column by er status
	return(ggplot(df, aes(Values, fill = Type)) + geom_histogram(bins = 100, position = "dodge") + 
           ggtitle(title))
}

#--------------------Plot Percents--------------------------------------------

percentAges <- function(data) {
	# Saves age percent plots and tables to list
	ret <- list()
	amd <- getCountsTable(data, "AgeMaD")
	ret[[1]] <- erBarPlot(getPercents(amd), "Age at Mother's Death")
	ret[[2]] <- grid.table(amd)
	mab <- getCountsTable(data, "MaAgeBr")
	ret[[3]] <- erBarPlot(getPercents(mab), "Mother's Age at Birth")
	ret[[4]] <- grid.table(mab)
	apd <- getCountsTable(data, "AgePaD")
	ret[[5]] <- erBarPlot(getPercents(apd), "Age at Father's Death")
	ret[[6]] <- grid.table(apd)
	pab <- getCountsTable(data, "PaAgeBr")
	ret[[7]] <- erBarPlot(getPercents(pab), "Fathers's Age at Birth")
	ret[[8]] <- grid.table(pab)
	sibs <- getCountsTable(data, "NumSibsDieChildhood")
	ret[[9]] <- erBarPlot(getPercents(sibs), "Number of Siblings Died During Childhood")
	ret[[10]] <- grid.table(sibs)
	return(ret)
}

percentSEI <- function(data) {
	# Saves sei/nam powers percent plots and tables to list
	ret <- list()
	mnp <- getCountsTable(data, "MaCenNamPow")
	ret[[1]] <- erBarPlot(getPercents(mnp), "Mother's Nam Powers Score")
	ret[[2]] <- grid.table(mnp)
	msei <- getCountsTable(data, "MaCenSEI")
	ret[[3]] <- erBarPlot(getPercents(msei), "Mother's Socio-Economic Index")
	ret[[4]] <- grid.table(msei)
	pnp <- getCountsTable(data, "PaCenNamPow")
	ret[[5]] <- erBarPlot(getPercents(pnp), "Father's Nam Powers Score")
	ret[[6]] <- grid.table(pnp)
	psei <- getCountsTable(data, "PaCenSEI")
	ret[[7]] <- erBarPlot(getPercents(psei), "Fathers's Socio-Economic Index")
	ret[[8]] <- grid.table(psei)
	return(ret)
}

percentIncome <- function(data) {
	# Saves income percent plots and tables to list
	ret <- list()
	ei <- getCountsTable(data, "EgoCenIncome")
	ret[[1]] <- erBarPlot(getPercents(ei), "Ego's Income")
	ret[[2]] <- grid.table(ei)
	mi <- getCountsTable(data, "MaCenIncome_New")
	ret[[3]] <- erBarPlot(getPercents(mi), "Mother's Income")
	ret[[4]] <- grid.table(mi)
	pi <- getCountsTable(data, "PaCenIncome_New")
	ret[[5]] <- erBarPlot(getPercents(pi), "Father's Income")
	ret[[6]] <- grid.table(pi)
	return(ret)
}

percentHomeValue <- function(data) {
	# Saves income percent plots and tables to list
	ret <- list()
	ehv <- getCountsTable(data, "HomeValue1940_New")
	ret[[1]] <- erBarPlot(getPercents(ehv), "Ego's 1940 Home Value")
	ret[[2]] <- grid.table(ehv)
	mhv <- getCountsTable(data, "MaHomeValue1940_New")
	ret[[3]] <- erBarPlot(getPercents(mhv), "Mother's 1940 Home Value")
	ret[[4]] <- grid.table(mhv)
	phv <- getCountsTable(data, "PaHomeValue1940_New")
	ret[[5]] <- erBarPlot(getPercents(phv), "Father's 1940 Home Value")
	ret[[6]] <- grid.table(phv)
	return(ret)
}

#--------------------Plot Counts----------------------------------------------

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
