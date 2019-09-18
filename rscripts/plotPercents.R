# Plots percents of adversity values

percentBarPlot <- function(tbl, title, xlabel, t, c) {
  # Returns bar plot of percents for given er status
  df <- subset(tbl, Type == t)
  main <- paste(title, t, sep = ": ")
  return(ggplot(df, aes(Values, y = (..count..)/sum(..count..))) + 
           geom_bar(position = "identity", fill = c) + xlab(xlabel) + ylab("Percent") + 
           scale_y_continuous(labels = scales::percent) + ggtitle(main))
}

percentHistorgram <- function(tbl, title, xlabel, t, c) {
  # Returns bar plot of percents for given er status
  df <- subset(tbl, Type == t)
  main <- paste(title, t, sep = ": ")
  return(ggplot(df, aes(Values, y = (..count..)/sum(..count..))) + 
           geom_histogram(bins = 100, position = "identity", fill = c) + xlab(xlabel) + ylab("Percent") + 
           scale_y_continuous(labels = scales::percent) + ggtitle(main))
}

writeXLSX <- function(data, file, names, append) {
  # Writes data frame to xlsx file
  first <- TRUE
  for (i in names) {
	  df <- getCountsTable(data, i)
  	if (first == FALSE) {
  		# Append all sucessive tables
  		append = TRUE
  	}
    write.xlsx(df, file, sheetName = i, row.names = FALSE, append = append)
  	first <- FALSE
  }
}

plotPercents <- function(data, names, titles, labels, totals, append, hst=FALSE) {
	# Plots given columns and writes counts to xlsx
  idx <- 1
	ret <- list()
	types <- c("ER+", "ER-", "Control")
	colors <- c("firebrick", "gold3", "navy")
	for (i in 1:length(names)){
		df <- getDataFrame(data, names[i], TRUE)
		for (x in 1:length(types)) {
		  if (hst == TRUE) {
			  ret[[idx]] <- percentHistorgram(df, titles[i], labels[i], types[x], colors[x])
		  } else {
		    ret[[idx]] <- percentBarPlot(df, titles[i], labels[i], types[x], colors[x])
		  }
			idx = idx + 1
		}
	}
	if (nchar(totals) > 0) {
	  writeXLSX(data, totals, names, append)
	}
	return(ret)
}

#-----------------------------------------------------------------------------

percentAges <- function(data, totals="") {
	# Saves age percent plots and tables to list
	names <- c("AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood")
	titles <- c("Age at Mother's Death", "Mother's Age at Birth", "Age at Father's Death", "Fathers's Age at Birth", "Number of Siblings Died During Childhood")
	labels <- c("Age", "Age", "Age", "Age", "Number of Siblings")
	return(plotPercents(data, names, titles, labels, totals, FALSE))
}

percentSEI <- function(data, totals="") {
	# Saves sei/nam powers percent plots and tables to list
	names <- c("MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI")
	titles <- c("Mother's Nam Powers", "Mother's SEI", "Father's Nam Powers", "Fathers's SEI")
	labels <- c("Nam Powers", "Socio-Economic Index", "Nam Powers", "Socio-Economic Index")
	return(plotPercents(data, names, titles, labels, totals, TRUE))
}

percentIncome <- function(data, totals="") {
	# Saves income percent plots and tables to list
	names <- c("EgoCenIncome", "MaCenIncome_New", "PaCenIncome_New")
	titles <- c("Ego's Income", "Mother's Income", "Father's Income")
	labels <- c("Income", "Income", "Income")
	return(plotPercents(data, names, titles, labels, totals, TRUE, TRUE))
}

percentHomeValue <- function(data, totals="") {
	# Saves income percent plots and tables to list
	names <- c("HomeValue1940_New", "MaHomeValue1940_New", "PaHomeValue1940_New")
	titles <- c("Ego's Home Value", "Mother's Home Value", "Father's Home Value")
	labels <- c("Home Value", "Home Value", "Home Value")
	return(plotPercents(data, names, titles, labels, totals, TRUE, TRUE))
}

#-----------------------------------------------------------------------------

plotNAs <- function(data) {
	# Makes bar plot of number of NAs for each field
	nas <- data.frame(matrix(ncol = 4, nrow = 0))
	colnames(nas) <- c("Field", "ER+", "ER-", "Control")
	columns <- c("AgeMaD", "MaAgeBr", "AgePaD", "PaAgeBr", "NumSibsDieChildhood", 
	             "MaCenNamPow", "MaCenSEI", "PaCenNamPow", "PaCenSEI", "EgoCenIncome", 
	             "MaCenIncome_New", "PaCenIncome_New", "HomeValue1940_New", 
	             "PaHomeValue1940_New", "MaHomeValue1940_New")
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
