# Parsing functions for histograms.R

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

getCountsTable <- function(data, col) {
	# Returns table of frequencies from column
	pos <- getERColumns(data, col, "P", "ER+")
	pos <- table(pos)
	neg <- getERColumns(data, col, "N", "ER-")
	neg <- table(neg)
	con <- getControlColumn(data, col)
	con <- table(con)
	ret <- merge(pos, neg, by = 0, all = TRUE)
	ret <- subset(ret, select = c(pos, Freq.x, Freq.y))
	ret <- merge(ret, data.frame(con), by = 1, all = TRUE)
	colnames(ret) <- c("Values", "ER+", "ER-", "Control")
	return(ret)
}

subColumn <- function(tbl, col) {
	# Converts column of frequencies to percent
	ret <- subset(tbl, select = c("Values", col))
	ret <- na.omit(ret)
	colnames(ret) <- c("Values", "Count")
	ret$Values <- sapply(ret$Values, as.character)
	ret$Values <- sapply(ret$Values, as.numeric)
	return(ret)
}