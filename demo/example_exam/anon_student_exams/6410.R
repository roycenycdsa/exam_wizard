lst_fnames = read.csv(
    "./data/lst_fnames.txt", header = FALSE)[[1]]
library(dplyr)
library(readr)
library(tidyverse)
library(lubridate)
library(zoo)
lst_dfs = list()
for(fname in lst_fnames){
    path = paste0("./data/", fname)
    print(path)
    lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

dataframe = rbind(lst_dfs[[1]], lst_dfs[[2]], lst_dfs[[3]], lst_dfs[[4]], lst_dfs[[5]],
                  lst_dfs[[6]], lst_dfs[[7]], lst_dfs[[8]], lst_dfs[[9]], lst_dfs[[10]],
                  lst_dfs[[11]], lst_dfs[[12]])
dataframe = dataframe %>% select(BIOGUIDE_ID, OFFICE, QUARTER, CATEGORY, DATE, PAYEE,
                                 START.DATE, END.DATE, PURPOSE, AMOUNT, YEAR, 
                                 TRANSCODE, RECORDID)
dataframe2 = rbind(lst_dfs[[13]], lst_dfs[[14]])
dataframe2 = dataframe2 %>% select(BIOGUIDE_ID, OFFICE, QUARTER, CATEGORY, DATE, PAYEE,
                                   START.DATE, END.DATE, PURPOSE, AMOUNT, YEAR, 
                                   TRANSCODE, RECORDID)
dataframe= rbind(dataframe, dataframe2)
dataframeNY = dataframe %>% select(PURPOSE, AMOUNT, OFFICE, START.DATE, END.DATE)
head(dataframeNY)
dataframeNY$AMOUNT = parse_number(dataframeNY$AMOUNT)
class(dataframeNY$AMOUNT)
dataframeNY %>% keep(~all(is.na(.x))) %>% names

dataframeNY$START.DATE = parse_date_time(x = dataframeNY$START.DATE,orders = c("m d y", "d B Y", "m/d/y"))
dataframeNY$END.DATE = parse_date_time(x = dataframeNY$END.DATE,orders = c("m d y", "d B Y", "m/d/y"))
head(dataframeNY$START.DATE)
dataframeNY = dataframeNY %>% mutate(START.DATE = as.Date(START.DATE, "%m/%d/%Y")) %>% 
    mutate(END.DATE = as.Date(END.DATE, "%m/%d/%Y"))
# Question 1
Total_payments = sum(dataframeNY$AMOUNT, na.rm=TRUE)
Total_payments

# Question 2
dataframeNY = dataframeNY %>% mutate(start_day = substr(x = dataframeNY$START.DATE, 
                                                        start = 9, stop=10))  %>% 
    mutate(end_day = substr(x = dataframeNY$END.DATE, 
                              start = 9, stop=10))
head(dataframeNY) 
class(dataframeNY$start_day)
dataframeNY$start_day = as.numeric(dataframeNY$start_day)
dataframeNY$end_day = as.numeric(dataframeNY$end_day)
head(dataframeNY)
dataframeNY = dataframeNY %>% mutate (coverage_period = end_day - start_day)
head(dataframeNY)
dataframePositive = dataframeNY %>% filter(coverage_period > 0, AMOUNT > 0) 
head(dataframePositive)
sd(coverage_period, na.rm=TRUE)

# Question 3
dataframeDates = dataframePositive %>% filter(between(START.DATE , as.Date("2010-01-01"), as.Date("2016-12-21"))) %>% 
    summarise(average_annual_expenditure = mean(AMOUNT))
head(dataframeDates)

# Question 4
dataframePositive$year = as.factor(format(dataframePositive$START.DATE ,"%Y"))
dataframeOffice = dataframePositive %>% select(year, PURPOSE, OFFICE, START.DATE, 
                                               END.DATE, AMOUNT, coverage_period) %>% 
    filter(year == 2016) %>%  arrange(desc(AMOUNT))
head(dataframeOffice)    
