#download the csvs

get_url <- function(year, quarter){
  url = paste0(
    "https://projects.propublica.org/congress/assets/staffers/", 
    year, quarter, 
    "-house-disburse-detail.csv"
  )
  
  return(url)
}

load_file_get_fname <- function(year, quarter){
  url = get_url(year, quarter)
  
  result = tryCatch(
    {
      print(paste0("Downloading for ", year, " ", quarter))
      read.csv(url)
    }, 
    error = function(e) {
      print(paste0("The url might not exist, no data for ", year, quarter, " is loaded."))
      NULL}
  )
  
  fname = paste0(year, "-", quarter, ".csv")
  path = paste0("./data/", fname)
  
  if(length(result)!=0){
    write.csv(result, path, row.names = FALSE)
  } else {
    fname = NULL
  }
  
  return(fname)
}

lst_fnames = character()
four_quarters = paste("Q", 1:4, sep = "")
for(year in 2010:2018){
  for(quarter in four_quarters){
    i = length(lst_fnames) + 1
    fname = load_file_get_fname(year, quarter)
    if(length(fname)!=0){
      lst_fnames[i] = fname
    }
  }
}

# generate list of file names

lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE)[[1]]
lst_fnames

# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

# Examine lst_dfs and data frames stored in it
str(lst_dfs[[2]])
length(lst_dfs)

#select PURPOSE, AMOUNT, OFFICE, START.DATE and END.DATE

# check whether column names are consisent across all data frames in the list - confirmed that each 
#column name occurs 36 times which is equal to the number of data frames in lst_df
cnames = lapply(lst_dfs, colnames)
cnames = unlist(cnames)

sum(cnames == "OFFICE")
sum(cnames == "PURPOSE")
sum(cnames == "AMOUNT")
sum(cnames == "START.DATE")
sum(cnames == "END.DATE")

#select PURPOSE, AMOUNT, OFFICE, START.DATE and END.DATE by applying dplyr
#select function to east element of a list, then confirm success by checking one data frame

library(dplyr)
lst_dfs2 = lapply(lst_dfs, function(x) select(x, OFFICE, PURPOSE, AMOUNT, START.DATE, END.DATE))
colnames(lst_dfs2[[8]])
rm(lst_dfs)

# the issue with amount not converting properly appears to be due to commas in the 4+ digit numbers
# the below code tests a potential solution
a = lst_dfs2[[1]]$AMOUNT
a = gsub(",","",a)
a = as.numeric(a)
sum(is.na(a))

# apply the solution to all "AMOUNT" columns in lst_dfs2 by looping through the list

for(i in 1:length(lst_dfs2)){
  temp = gsub(",","",lst_dfs2[[i]]$AMOUNT)
  temp2 = as.numeric(temp)
  lst_dfs2[[i]]$AMOUNT = temp2
}

# loop through to remove "FISCAL YEAR yyyy"
for(i in 1:length(lst_dfs2)){
  temp = trimws(gsub("FISCAL YEAR [0-9]*", '',lst_dfs2[[i]]$OFFICE),which="left")
  lst_dfs2[[i]]$OFFICE = temp
}

# loop through to remove yyyy"
for(i in 1:length(lst_dfs2)){
  temp = trimws(gsub("[0-9]+",'',lst_dfs2[[i]]$OFFICE),which="left")
  lst_dfs2[[i]]$OFFICE = temp
}

# loop through list of data frames to convert start date
for(i in 1:length(lst_dfs2)){
  if(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", lst_dfs2[[i]]$START.DATE)==TRUE){
    lst_dfs2[[i]]$START.DATE = as.Date(lst_dfs2[[i]]$START.DATE, "%m/%d/%y")
  } else if(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", x)==TRUE){
    lst_dfs2[[i]]$START.DATE = as.Date(lst_dfs2[[i]]$START.DATE, "%m/%d/%Y")
  } else {
    lst_dfs2[[i]]$START.DATE = lst_dfs2[[i]]$START.DATE
  }
}

#loop through list of data frames to convert end date

for(i in 1:length(lst_dfs2)){
  if(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", lst_dfs2[[i]]$END.DATE)==TRUE){
    lst_dfs2[[i]]$END.DATE = as.Date(lst_dfs2[[i]]$END.DATE, "%m/%d/%y")
  } else if(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", x)==TRUE){
    lst_dfs2[[i]]$END.DATE = as.Date(lst_dfs2[[i]]$END.DATE, "%m/%d/%Y")
  } else {
    lst_dfs2[[i]]$END.DATE = lst_dfs2[[i]]$END.DATE
  }
}

#bind into single file, but convert dates to characters to allow for bind_rows

for(i in 1:length(lst_dfs2)){
  lst_dfs2[[i]]$START.DATE = as.character(lst_dfs2[[i]]$START.DATE)
}

for(i in 1:length(lst_dfs2)){
  lst_dfs2[[i]]$END.DATE = as.character(lst_dfs2[[i]]$END.DATE)
}

lst_dfs3 = bind_rows(lst_dfs2)

#Q1

lst_dfs3 = lst_dfs3[-3688493,]
sum(lst_dfs3$AMOUNT)

#Q2

lst_dfs3$START.DATE = as.Date(lst_dfs3$START.DATE)
lst_dfs3$END.DATE = as.Date(lst_dfs3$END.DATE)
lst_dfs3$COVERAGE.PERIOD = lst_dfs3$END.DATE - lst_dfs3$START.DATE

cov_per = filter(lst_dfs3, AMOUNT>0) %>% 
  .[,6]
cov_per = as.numeric(cov_per)
cov_per[is.na(cov_per)]=0
sd(cov_per)

#Q3




