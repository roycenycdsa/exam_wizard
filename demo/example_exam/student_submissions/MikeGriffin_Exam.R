# MG ANSWERS

library(tidyverse)

# READ DATA ####

#Test and visualising
df_2010_Q1 = read.csv("./data/2010-Q2.csv",stringsAsFactors=FALSE)
head(df_10_Q1)

lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE)[[1]]

# Look at column names across dfs
for (i in 1: 14) {
  print(colnames(lst_dfs[[1]]))
}

# Initialize empty df
df_comb = df_2010_Q1[FALSE,]
df_comb = df_comb %>% mutate(YY_IMPORT= '', QQ_IMPORT = '') %>% 
  select(c(DATE,YEAR,YY_IMPORT,QQ_IMPORT,START.DATE,END.DATE,OFFICE,AMOUNT,PURPOSE))

# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
  df_next = as.data.frame(read.csv(path, stringsAsFactors = F))
  df_next = df_next %>% mutate(YY_IMPORT = as.numeric(substr(fname[1],1,4)), QQ_IMPORT = substr(fname[1],6,7)) %>% 
     select(c(DATE,YEAR,YY_IMPORT,QQ_IMPORT,START.DATE,END.DATE,OFFICE,AMOUNT,PURPOSE))
  df_comb = rbind(df_comb,df_next)
}

# Test aggregation across years, complete against dataset from Sam (which misses years)
test = df_comb %>% group_by(YY_IMPORT,QQ_IMPORT) %>% 
    summarise(count = n())


# DATA CLEANING ####

# Define new cleansed varaibles to allow easy comparison

#Cleanse numerical amounts
df_comb['AMOUNT_NUM'] = as.numeric(gsub(",","",df_comb$AMOUNT)) # Fix formatting to allow summation
df_comb$AMOUNT_NUM[is.na(df_comb$AMOUNT_NUM)] =0

#Cleanse office
df_comb['OFFICE_CLEAN'] = gsub("FISCAL YEAR","",df_comb$OFFICE)
for (i in 2010:2018) {
  df_comb['OFFICE_CLEAN'] = gsub(i,"",df_comb$OFFICE)
}

# Cleanse dates

# Loop to check date formats, shows change in format in 2018 with blanks 
for (i in 2010:2018) {
print(head(df_comb[df_comb$YY_IMPORT == as.character(i),"START.DATE"]))
      }

df_comb = df_comb %>% mutate(START_DATE_CLEAN = case_when(
      YY_IMPORT <= 2017 ~ as.Date(df_comb$START.DATE,format = "%m/%d/%y"),
#     YY_IMPORT == 2018 ~ parse_date_time(df_comb$START.DATE)  
      YY_IMPORT == 2018 ~ as.Date(df_comb$START.DATE,format = "%Y-%m-%d")                               
        ),
      END_DATE_CLEAN = case_when(
        YY_IMPORT <= 2017 ~ as.Date(df_comb$END.DATE,format = "%m/%d/%y"),
#        YY_IMPORT == 2018 ~ parse_date_time(df_comb$START.DATE)
        YY_IMPORT == 2018 ~ as.Date(df_comb$END.DATE,format = "%Y-%m-%d")
        )
  )


# QUESTIONS #### 

# Q1
total_payments = sum(df_comb$AMOUNT_NUM)
print(total_payments)


# Q2
df_comb = df_comb %>% mutate(COVERAGE_PERIOD = (END_DATE_CLEAN - START_DATE_CLEAN)) 

# Removing all NAs
sd(df_comb$COVERAGE_PERIOD[!is.na(df_comb$COVERAGE_PERIOD)])


# Q3
Pos_Exp_2010_to_2016 = df_comb %>% filter(year(START_DATE_CLEAN) >= 2010 & year(START_DATE_CLEAN) <=2016) %>% 
  filter(AMOUNT_NUM > 0)
  
print(sum(Pos_Exp_2010_to_2016$AMOUNT_NUM))


#Q4, CHIEF ADMIN OFCR OF THE HOUSE 
df_comb %>% filter(year(START_DATE_CLEAN) == '2016') %>%
  group_by(OFFICE) %>% 
  summarise(total = sum(AMOUNT_NUM)) %>% 
  top_n(1, wt =total)

df_comb[df_comb$OFFICE == 'CHIEF ADMIN OFCR OF THE HOUSE',] %>% 
  group_by(PURPOSE) %>% 
  summarise(total = sum(AMOUNT_NUM)) %>% 
  arrange(desc(total))
