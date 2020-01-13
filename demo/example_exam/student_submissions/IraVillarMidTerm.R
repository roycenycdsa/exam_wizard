library(dplyr)
library(lubridate)

lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE)[[1]]

# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path,stringsAsFactors = F)
}

for(i in 1:length(lst_dfs)){
  lst_dfs[[i]] = lst_dfs[[i]] %>% 
    select(PURPOSE,AMOUNT,OFFICE,START.DATE,END.DATE)
  }
colnames(lst_dfs[[1]])
#### Test Start ####

# lst_dfs[[1]] = lst_dfs[[1]] %>% 
#   select(AMOUNT) %>% 
#   mutate(AMOUNT = gsub(pattern ='"',replacement = "", lst_dfs[[1]]$AMOUNT)) %>% 
#   mutate(AMOUNT = gsub("([..])|[[:punct:]]", "", lst_dfs[[1]]$AMOUNT)) %>% 
#   mutate(AMOUNT = as.numeric(format(AMOUNT))) %>% 
#   filter(AMOUNT != is.na(AMOUNT)) %>% 
#   summarise(sum_ = sum(AMOUNT))
# lst_dfs[[1]]$sum_
lst_dfs[[22]] %>% 
  select(AMOUNT) %>% 
  mutate(AMOUNT = gsub(pattern ='"',replacement = "", lst_dfs[[22]]$AMOUNT)) %>% 
  mutate(AMOUNT = gsub(",", "", lst_dfs[[22]]$AMOUNT)) %>%
  mutate(AMOUNT = as.numeric(AMOUNT)) %>% 
  filter(AMOUNT != is.na(AMOUNT)) %>% 
  summarise(sum_ = sum(AMOUNT))
#1.
payment_sum = 0
for(i in 1:length(lst_dfs)){
  
  lst_dfs[[i]] %>% 
    select(AMOUNT) %>% 
    mutate(AMOUNT = gsub(pattern ='"',replacement = "", lst_dfs[[i]]$AMOUNT)) %>% 
    mutate(AMOUNT = gsub(",", "", lst_dfs[[i]]$AMOUNT)) %>%
    mutate(AMOUNT = as.numeric(AMOUNT)) %>% 
    filter(AMOUNT != is.na(AMOUNT)) %>% 
    select(sum_ = sum(AMOUNT))
  
    payment_sum = payment_sum + lst_dfs[[i]]$sum_
}

#2.

for(i in 1:length(lst_dfs)){
lst_dfs[[i]] %>% 
    select(START.DATE,END.DATE,AMOUNT) %>%
    filter(AMOUNT > 0) %>% 
    mutate(START.DATE = as.Date(START.DATE, "%m/%d/%Y")) %>% 
    mutate(END.DATE = as.Date(END.DATE,"%m/%d/%Y")) %>% 
    filter(END.DATE != is.na(END.DATE)) %>% 
    filter(START.DATE != is.na(START.DATE)) %>% 
    mutate(COVERAGE.PERIOD = as.numeric(difftime(END.DATE, START.DATE))) %>%
    filter(COVERAGE.PERIOD >0) 
    summarise(sd = sd(COVERAGE.PERIOD))
  
 }


#3.
# for(i in lst_dfs[[1]]:lst_dfs[[28]]){
#   
# }
