library(dplyr)
library(ggplot2)
library(tidyr)

lst_fnames = read.csv("./data/lst_fnames.txt", header = FALSE)[[1]]


# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

df <- lst_dfs[[fname]]
head(df,1)

df2 <- na.omit(df)
anyNA(df2)

#Q1
df2 %>% summarise(.,sum(AMOUNT))


#Q2
df2 <- df2 %>% mutate(., d.start.date=as.Date(START.DATE))
df2 <- df2 %>% mutate(., d.end.date=as.Date(END.DATE))

df2  <- df2 %>% mutate(., coverage_period= d.end.date - d.start.date)

# without ALL amounts
df2 %>%  summarise(., sd(coverage_period,na.rm = TRUE))

p_coverage_period <- df2$coverage_period[which(df2$coverage_period > 0)]
head(p_coverage_period)

# with only POSITIVE amounts
sd(p_coverage_period)

#Q3
df2_date_filtered <- df2 %>% filter(d.start.date >= "2010-01-01" & d.start.date <= "2016-12-31")
head(df2_date_filtered,1)

range(df2_date_filtered$d.start.date)
range(df2$d.start.date,na.rm = TRUE)
range(df2_date_filtered$AMOUNT)

df2_date_filtered_positive_amounts <- df2_date_filtered$AMOUNT[which(df2_date_filtered$AMOUNT > 0)]
range(df2_date_filtered_positive_amounts)

#length(df2_date_filtered_positive_amounts)
mean(df2_date_filtered_positive_amounts)


#Q4
df2 <- df2 %>% mutate(start.date.year = as.numeric(as.character(format(as.Date(d.start.date), "%Y"))))

df2_year_filtered <- df2 %>% filter(start.date.year >= "2016")
head(df2_year_filtered,1)
range(df2_year_filtered$start.date.year)

head(df2_year_filtered %>% group_by(OFFICE) %>% summarise(.,avg_by_office=mean(AMOUNT)) %>% arrange(desc(avg_by_office)),5)

head(df2_year_filtered %>% group_by(OFFICE,PURPOSE) %>% summarise(.,avg_by_office=mean(AMOUNT)) %>% arrange(desc(avg_by_office)),5)

head(df2_year_filtered %>% group_by(PURPOSE) %>% summarise(.,avg_by_office=mean(AMOUNT)) %>% arrange(desc(avg_by_office)),5)

df2_year_filtered_ratio <- df2_year_filtered %>% mutate(., ratio=df2_year_filtered$AMOUNT/length(df2_year_filtered$AMOUNT))
head(df2_year_filtered_ratio,1)
head(df2_year_filtered_ratio$ratio)

head(df2_year_filtered_ratio %>% select(., OFFICE, PURPOSE, ratio) %>% group_by(OFFICE) %>% arrange(desc(ratio)),3)

