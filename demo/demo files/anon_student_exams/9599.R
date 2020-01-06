library(stringr)
library(lubridate)

lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE, stringsAsFactors = F)[[1]]

# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}
lst_dfs <- lst_dfsread
# convert AMOUNT to numeric ####
for (idx in lst_fnames) {
  lst_dfs[[idx]]$AMOUNT <- as.numeric(lst_dfs[[idx]]$AMOUNT)
}
warnings()
#convert NA in AMOUNT to 0
class(lst_dfs[['2010-Q3.csv']]$AMOUNT)
for (idx in lst_fnames) {
  lst_dfs[[idx]]$AMOUNT <- ifelse(is.na(lst_dfs[[idx]]$AMOUNT),0,lst_dfs[[idx]]$AMOUNT)
}
# convert start date into date format ####
for (idx in lst_fnames) {
    lst_dfs[[idx]]$START.DATE <- ifelse(is.na(str_locate(lst_dfs[[idx]]$START.DATE,'/')[1]),
                                        gsub('-','/',lst_dfs[[idx]]$START.DATE),
                                        lst_dfs[[idx]]$START.DATE)
}  
for (idx in lst_fnames) {
    lst_dfs[[idx]]$START.DATE <- ifelse(str_locate(lst_dfs[[idx]]$START.DATE,'/')[1] == 2,
                                        paste0('0',str_sub(lst_dfs[[idx]]$START.DATE,1,-1)),
                                        lst_dfs[[idx]]$START.DATE)
} 
for (idx in lst_fnames) {
    lst_dfs[[idx]]$START.DATE <- ifelse(str_locate_all(lst_dfs[[idx]]$START.DATE,'/')[[1]][1,1] == 3 & 
                                        str_locate_all(lst_dfs[[idx]]$START.DATE,'/')[[1]][2,1] == 5,
                                        paste0(str_sub(lst_dfs[[idx]]$START.DATE,1,3),'0',
                                        str_sub(lst_dfs[[idx]]$START.DATE,4,-1)),
                                        lst_dfs[[idx]]$START.DATE)
}  
for (idx in lst_fnames) {
    if (nchar(lst_dfs[[idx]]$START.DATE) == 10) {
    if (str_locate(lst_dfs[[idx]]$START.DATE,'/')[1] == 3) {
      lst_dfs[[idx]]$START.DATE <- as.Date(lst_dfs[[idx]]$START.DATE, '%m/%d/%Y')
    } else if (str_locate(lst_dfs[[idx]]$START.DATE,'/')[1] == 5) {
      lst_dfs[[idx]]$START.DATE <- as.Date(lst_dfs[[idx]]$START.DATE, '%Y/%m/%d')
    }
  } else if (nchar(lst_dfs[[idx]]$START.DATE) == 8) {
        if (str_locate(lst_dfs[[idx]]$START.DATE,'/')[1] == 3) {
      lst_dfs[[idx]]$START.DATE <- as.Date(lst_dfs[[idx]]$START.DATE, '%m/%d/%y')
    }
  }
}  

# convert end date into date format ####
for (idx in lst_fnames) {
    lst_dfs[[idx]]$END.DATE <- ifelse(is.na(str_locate(lst_dfs[[idx]]$END.DATE,'/')[1]),
                                        gsub('-','/',lst_dfs[[idx]]$END.DATE),
                                        lst_dfs[[idx]]$END.DATE)
}  
for (idx in lst_fnames) {
    lst_dfs[[idx]]$END.DATE <- ifelse(str_locate(lst_dfs[[idx]]$END.DATE,'/')[1] == 2,
                                        paste0('0',str_sub(lst_dfs[[idx]]$END.DATE,1,-1)),
                                        lst_dfs[[idx]]$END.DATE)
} 
for (idx in lst_fnames) {
    lst_dfs[[idx]]$END.DATE <- ifelse(str_locate_all(lst_dfs[[idx]]$END.DATE,'/')[[1]][1,1] == 3 & 
                                        str_locate_all(lst_dfs[[idx]]$END.DATE,'/')[[1]][2,1] == 5  ,
                                        paste0(str_sub(lst_dfs[[idx]]$END.DATE,1,3),'0',
                                        str_sub(lst_dfs[[idx]]$END.DATE,4,-1)),
                                        lst_dfs[[idx]]$END.DATE)
}  
for (idx in lst_fnames) {
    if (nchar(lst_dfs[[idx]]$END.DATE) == 10) {
    if (str_locate(lst_dfs[[idx]]$END.DATE,'/')[1] == 3) {
      lst_dfs[[idx]]$END.DATE <- as.Date(lst_dfs[[idx]]$END.DATE, '%m/%d/%Y')
    } else if (str_locate(lst_dfs[[idx]]$END.DATE,'/')[1] == 5) {
      lst_dfs[[idx]]$END.DATE <- as.Date(lst_dfs[[idx]]$END.DATE, '%Y/%m/%d')
    }
  } else if (nchar(lst_dfs[[idx]]$END.DATE) == 8) {
        if (str_locate(lst_dfs[[idx]]$END.DATE,'/')[1] == 3) {
      lst_dfs[[idx]]$END.DATE <- as.Date(lst_dfs[[idx]]$END.DATE, '%m/%d/%y')
    }
  }
}

# get rid of fiscal year in office ####
for (idx in lst_fnames) {
  lst_dfs[[idx]]$OFFICE <- ifelse(str_sub(lst_dfs[[idx]]$OFFICE,1,12) == 'FISCAL YEAR ',
         str_sub(lst_dfs[[idx]]$OFFICE,13,-1),
         lst_dfs[[idx]]$OFFICE)
}
for (idx in lst_fnames) {
  lst_dfs[[idx]]$OFFICE <- ifelse(str_sub(lst_dfs[[idx]]$OFFICE,1,2) == '20',
         str_sub(lst_dfs[[idx]]$OFFICE,6,-1),
         lst_dfs[[idx]]$OFFICE)
}

cleandf <- lapply(lst_fnames,function(x){lst_dfs[[x]] %>% 
    select(., OFFICE, START.DATE, END.DATE, AMOUNT, PURPOSE)}) %>% bind_rows()
# done cleaning ####



# 1
total_payment <- cleandf %>% summarise(., sum(AMOUNT))
total_payment

# 2
sd_coverage <- cleandf %>% mutate(., coverage = END.DATE - START.DATE) %>% summarise(., sd(coverage))
sd_coverage

#3
mean_spending <- cleandf %>% filter(., START.DATE >= '2010-01-01' & START.DATE <= '2016-12-31') %>% 
  filter(., AMOUNT > 0) %>% group_by(., year(START.DATE)) %>% summarise(.,mean(AMOUNT))
mean_spending

#4
cleandf %>% filter(., year(START.DATE) == '2016' & AMOUNT > 0) %>% group_by(., OFFICE) %>% 
  summarise(., spending = sum(AMOUNT)) %>% top_n(.,1 ) -> topspender
topspender
cleandf %>% filter(., year(START.DATE) == '2016' & OFFICE == topspender[[1]][1] & AMOUNT > 0) %>% 
  group_by(., PURPOSE) %>% 
  summarise(., spending = sum(AMOUNT)) %>% top_n(., 1) -> topreason
topreason
topfraction <- topreason$spending/topspender$spending
topfraction

