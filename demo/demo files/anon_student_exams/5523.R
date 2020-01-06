
#?list.files

library(tidyverse)
library(ggthemes)
library(lubridate)
library(forcats)
library(data.table)
library(tidyr)


rm(list = ls())
getwd()
setwd('C:/Users/cathe/Code/data')

file_list <- list.files(path = 'C:/Users/cathe/Code/data')

ldf <- lapply(file_list, read.csv)

df_final <- do.call("rbind", ldf)


dl_df = data.frame(
  lapply(dl, as.character),
  stringsAsFactors = F
)

dl_df$AMOUNT[is.na(dl_df$AMOUNT)] <- 0

dl_df <- dl_df %>% 
  mutate(.,AMOUNT = as.numeric(AMOUNT))

sum(dl_df$AMOUNT,na.rm = T)

str(dl_df)


dl_df <- dl_df %>% 
  mutate(., END.DATE = (as.Date.character(dl_df$END.DATE,"%m/%d/%y"))) %>% 
  mutate(., START.DATE = (as.Date.character(dl_df$START.DATE,"%m/%d/%y"))) %>% 
  mutate(., COVERGE.PERIOD = END.DATE - START.DATE)


#d = (as.duration(COVERGE.PERIOD[dl_df$COVERGE.PERIOD>0]) / ddays(1))

summarize(dl_df,COVERGE.PERIOD = sd((as.duration(COVERGE.PERIOD[dl_df$COVERGE.PERIOD>0]) / ddays(1)),na.rm = T))

str(dl_df)


summarize(dl_df,START.DATE = sum((as.duration(START.DATE[dl_df$START.DATE>0]) / ddays(1)),na.rm = T)))




##attemp 2
#dl_df %>% group_by(., AMOUNT, START.DATE =
#(dl_df$START.DATE[dl_df$START.DATE > "2010-01-01" & dl_df$START.DATE < "2010-12-31"])) %>% 
 # summarise(., std = sd(AMOUNT))

##subset from START DATE
dl_df$START.DATE[dl_df$START.DATE > "2010-01-01" & dl_df$START.DATE < "2010-12-31"]




#aggregate(dl_df$AMOUNT, by = list(dl_df$START.DATE =dl_df$START.DATE[dl_df$START.DATE > "2010-01-01" & dl_df$START.DATE < "2010-12-31"]), FUN = sd)

####finding office w. highest exp in 2016

dl_df %>% 
  group_by(., OFFICE,START.DATE>'2015-12-31' < '2016-12-31') %>% 
  summarise(., sum(AMOUNT))
