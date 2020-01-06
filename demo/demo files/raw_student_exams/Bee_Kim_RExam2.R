# load the file ####
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
for(year in 2009:2018){
  for(quarter in four_quarters){
    i = length(lst_fnames) + 1
    fname = load_file_get_fname(year, quarter)
    if(length(fname)!=0){
      lst_fnames[i] = fname
    }
  }
}

write(lst_fnames, "data/lst_fnames.txt")

lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE)[[1]]
lst_fnames

lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

head(lst_dfs,5)



#cleaning ####
library(tidyverse)
df16 <-read.csv("./data/2016-Q3.csv")

#sorry I had a problem using the list done from the loadgin the file section. 
#my Rstudio crashed 3 times so I am gonna use 2016Q3 file just to show the cleaning part. 

#structure of this dataframe
str(df16)

#any missing value?
length(df16[is.na(df16)])   #none

#select the columns
df16s = df16 %>% 
  select(PURPOSE,AMOUNT,OFFICE,START.DATE,END.DATE)

#check the class of amount
class(df16s$AMOUNT)

#change the class of column amount
df16s = df16s %>% 
  mutate(AMOUNT = as.numeric(AMOUNT))

class(df16s$AMOUNT)
head(df16s, 10)

#check NA in amount column
length(df16s$AMOUNT[is.na(df16s$AMOUNT)])
#seems like no problem. maybe because i only used one dataset. 

#office name - i don't have any duplicates because using one 
#but let say I do, then..
# mutate(OFFICE = mutate(gsub("yyyy",""))) 
#something like this?? but can't check. Sorry

#start.date to date type
head(df16s$START.DATE, 5)
class(df16s$START.DATE)
df16s <- df16s %>% 
  mutate(START.DATE=as.Date(START.DATE, "%m/%d/%y"),"%y/%m/%d")

head(df16s$START.DATE, 5)
class(df16s$START.DATE)

#end.date to date type
head(df16s$END.DATE, 5)
class(df16s$END.DATE)
df16s <- df16s %>% 
  mutate(END.DATE=as.Date(END.DATE, "%m/%d/%y"),"%y/%m/%d")

head(df16s$END.DATE, 5)
class(df16s$END.DATE)




# Q1 ####
df16s %>% 
  summarise(sum(AMOUNT))



# Q2 ####
df16sCD = df16s %>% 
  mutate(COVERAGE.PERIOD = difftime(END.DATE ,START.DATE, units = c("days")))
df16sCD



# Q3 annual average ####
df16s3 = df16s %>%
  filter(AMOUNT >0) %>%
  summarise(mean(AMOUNT))

df16s3



# Q4 highest total expensitures with a start.date in 2016. ####
#subset(START.DATE, format(START.DATE, "%Y") == 2016)

df16s %>% 
  #group_by(subset(START.DATE, format(START.DATE, "%Y") == 2016)) %>%
  top_n(1,AMOUNT)

# so HON. SUSAN W.BROOKS, HON.JUDY CHU, HON.CHARLES W.DENT, HON.RAUL M. GRIJALVA
# purpose : shared employee, computer hardw purch less than $25000 and senior policy advisor for purposes. 

Am1 = df16s %>%
  top_n(1,AMOUNT) %>% 
  select(AMOUNT) 

df16s %>% 
  summarise(Am1/sum(AMOUNT))




#comment ####
#over all, sorry for not completing the exam the way it was asked. 
#I had a hard time using list from the loaded csv files because I didn't know how to convert this list to data frame to work on. 
#R studio crushed 3 times trying to change to dataframe (up till 12pm) so I decided to just use 2016-Q3 file to at least answer the questions as much as I can. 
