library(tidyverse)

lst_fnames = read.csv("lst_fnames.txt", header = FALSE)[[1]]

# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0(fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

# Take each item from list of dataframes, selecting only 5 columns in each
# and combine into one new dataframe
for (i_df in 1:36){
  lst_dfs[[i_df]] %>%
    select(., OFFICE, START.DATE, END.DATE, PURPOSE, AMOUNT) -> lst_dfs2
}

lst_dfs2$AMOUNT <- gsub(",","",lst_dfs2$AMOUNT)
lst_dfs2$AMOUNT <- as.numeric(lst_dfs2$AMOUNT)

lst_dfs2$OFFICE <- gsub("\\d{4} ","", lst_dfs2$OFFICE)
lst_dfs2$OFFICE <- gsub("FISCAL YEAR", "", lst_dfs2$OFFICE)

lst_dfs2$START.DATE <- as.Date(lst_dfs2$START.DATE,format="%Y-%m-%d", tryFormats="%Y-%m-%d", "%m-%d-%y","%m-%d-%Y")
lst_dfs2$END.DATE <- as.Date(lst_dfs2$END.DATE,format="%Y-%m-%d", tryFormats="%Y-%m-%d", "%m-%d-%y","%m-%d-%Y")


sum(lst_dfs2$AMOUNT, na.rm = TRUE)

lst_dfs2$COVERAGE.PERIOD <- lst_dfs2$END.DATE - lst_dfs2$START.DATE

sd(lst_dfs2[lst_dfs2$AMOUNT>0,6],na.rm=TRUE)
         
lst_dfs2$START.YEAR <- as.numeric(format(lst_dfs2$START.DATE, "%Y"))

mean(lst_dfs2[(lst_dfs2$AMOUNT>0 & lst_dfs2$START.YEAR >=2010 & lst_dfs2$START.YEAR <= 2017),5],na.rm=TRUE)

oo <- lst_dfs2[(lst_dfs2$START.YEAR == 2016),]

oo %>%
  group_by(.,OFFICE) %>%
  summarise(.,max(AMOUNT)) -> amount_table












