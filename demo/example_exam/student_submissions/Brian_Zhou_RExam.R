getwd()
setwd("E:/Coding/NYCDSA - Sep 2019/Homework/Midterm/")
getwd()

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
  path = paste0("./CSV Data/", fname)
  
  if(length(result)!=0){
    write.csv(result, path, row.names = FALSE)
  } else {
    fname = NULL
  }
  
  return(fname)
}

lst_fnames = character()
four_quarters = paste("Q", 1:4, sep = "")
for(year in 2009:2018){
  for(quarter in four_quarters){
    i = length(lst_fnames) + 1
    fname = load_file_get_fname(year, quarter)
    if(length(fname)!=0){
      lst_fnames[i] = fname
    }
  }
}

write(lst_fnames, "CSV Data/lst_fnames.txt")




# Load data & clean data

library(ggplot2)
library(dplyr)
library(lubridate)

lst_fnames = read.csv("./CSV Data/lst_fnames.txt", header = FALSE)[[1]]
lst_fnames

# Initializing the list of df
lst_df = list()
lst_y = c('2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018')
index = 1

for (i in lst_fnames){
  df = read.csv(paste0('./CSV Data/', i), stringsAsFactors = FALSE)
  # Select cols
  df_c = df %>% select(PURPOSE, AMOUNT, OFFICE, START.DATE, END.DATE)
  # Clean data in AMOUNT, OFFICE
  df_c = df_c %>% 
    mutate(AMOUNT = as.numeric(AMOUNT)) %>%
    filter(! is.na(AMOUNT)) %>%
    mutate(OFFICE = ifelse(substr(OFFICE, 1, 4) %in% lst_y, 
                           substr(OFFICE, 6, nchar(OFFICE)), 
                                  ifelse(substr(OFFICE, 13, 16) %in% year, 
                                         substr(OFFICE, 18, nchar(OFFICE)), OFFICE)))
  
  # Clean start and end dates
  df_c$START.DATE = as.Date(df_c$START.DATE, format = '%Y-%m-%d')

  df_c$START.DATE = ifelse(year(df_c$START.DATE) <= 25, df_c$START.DATE + years(2000),
                           ifelse(year(df_c$START.DATE) <= 99, df_c$START.DATE + years(1900)), df_c$START.DATE)
  
  df_c$END.DATE = as.Date(df_c$END.DATE, format = '%Y-%m-%d')
  
  df_c$END.DATE = ifelse(year(df_c$END.DATE) <= 25, df_c$END.DATE + years(2000),
                           ifelse(year(df_c$END.DATE) <= 99, df_c$END.DATE + years(1900)), df_c$END.DATE)
  
  
  # df_c = df_c %>% 
  #   mutate(START.DATE = ifelse(year(START.DATE) <= 25, START.DATE + years(2000), ifelse(year(START.DATE) <= 99, START.DATE + years(1900), START.DATE)))
  
  lst_df[[index]] = df_c
  index = index + 1
}

lst_df[[1]]

## Q1



## Q2



## Q3




## Q4






















