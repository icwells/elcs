# ELCS Project scripts

### These scripts are meant for the use of the Atkipis lab, Biodesign Institute, Arizona State University
### Copyright 2019 by Shawn Rupp

## Installation  
	git clone https://github.com/icwells/elcs.git    

## Usage 
These scripts are meant to run on a Windows server with no internet access, and thus are completely self-contained.  
All input files are declared within the manifest.py file, and all output will be written to the scripts' parent directory.  

### Merge UCR and UPDB records:  

	& 'C:\Program Files (x86)\Python\Python37-32\python.exe' mergeRecords.py  

### Summarize Output files:  

	& 'C:\Program Files (x86)\Python\Python37-32\python.exe' summary.py \path\to\input  

### File Description  
Amycasedat_051916.csv: UCR data  
David_Ken_BreastCancer_CaseControl_New20171024.csv: 5 case IDs (person IDs) to 1 control  
David_Ken_BreastCancer_Main_20160617.csv: UPDB data for entries in UCR data  
David_Ken_BreastCancer_Main_Ctrl_20160617.csv: UPDB data for entries without UCR data  
