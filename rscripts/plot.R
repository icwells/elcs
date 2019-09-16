# Plotting functions for historgrams.R

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
