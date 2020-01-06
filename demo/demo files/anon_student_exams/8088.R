library(dplyr)

lst_fnames = read.csv(
    "./data/lst_fnames.txt", header = FALSE)[[1]]


# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
    path = paste0("./data/", fname)
    print(path)
    lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

lst_dfs[[1]]

n=length(lst_dfs)

df = lst_dfs[[1]] %>% select("PURPOSE", "AMOUNT", "OFFICE", "START.DATE","END.DATE")

for (j in 2:n){
    lst_dfs[[j]] %>% select("PURPOSE", "AMOUNT", "OFFICE", "START.DATE","END.DATE") -> temp
    df = rbind(df,temp)
}

unique(df$START.DATE)

colnames(df)

df$temp=as.numeric(gsub(",","",df$AMOUNT))
#df_backup=df
df$AMOUNT=df$temp
df$temp=NULL

#df$temp2=df$START.DATE

#df$temp=as.Date(df$START.DATE,"%m/%d/%y")
#df$temp2=as.Date(df$START.DATE,"%Y-%m-%d")
#df$start=ifelse(is.na(df$temp),as.Date(df$temp2),as.Date(df$temp))

#df$start=NULL
#df$temp=NULL
#df$temp2=NULL
#sum(is.na(df$temp))
#sum(is.na(df$temp2))

#df$start=df$temp
#df$start[is.na(df$temp)]==df$temp2[is.na(df$start)]
#chr=apply(df,2,nchar)

df %>% mutate(start=nchar(START.DATE)) -> df
temp$start2=as.Date(temp$start)

library(lubridate)

head(df %>% select(START.DATE,start) %>% filter(start==6),2)
head(df %>% select(START.DATE,start) %>% filter(start==7),2)
head(df %>% select(START.DATE,start) %>% filter(start==8),2)
head(df %>% select(START.DATE,start) %>% filter(start==9),2)
head(df %>% select(START.DATE,start) %>% filter(start==10),2)

df$start=NULL
df$x=NULL

temp=ifelse(df$start<10 & df$start>5,strsplit(df$START.DATE,split = "/"),"")

temp2=ifelse(df$start==10,strsplit(df$START.DATE,split = "-"),"")

df %>% mutate(x_5_9=mdy(START.DATE),x_10=ymd(START.DATE)) %>% mutate(x=ifelse(start<10,x_5_9,x_10)) -> df

mdy("2/13/2017")
library(lubridate)

unique(month(df$temp))
x=df[is.na(df$temp),]
df$AMOUNT

data=df$START.DATE
convert_date <- function(data){
    n=length(data)
    a<-vector("numeric",length=n)
    class(a)="Date"
    for (i in 1:n){
        if (nchar(data[i]) > 5 & nchar(data[i]) < 10){
            a[i] <- mdy(data[i])
        } else if (nchar(data[i]) == 10){
            a[i] <- ymd(data[i])
        } else {NA}
    }    
}

data=df$START.DATE
df$date.start=a

grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2,4}\\b", "1/1/1998")
grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2,4}\\b", "1/1/98")

#n=nrow(df)
dates<-vector("numeric",length=nrow(df))
class(dates)="Date"



df$dates_2=grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", df$START.DATE)
df$dates_4=grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", df$START.DATE)

#df$start.date=0
#class(df$start) = "Date"
df %>% mutate(end.date=ifelse(df$dates_2==T,mdy(START.DATE),ymd(START.DATE))) -> df
df$start.date.2=as.Date(df$start.date, origin = "1970-01-01")

df$dates_2=grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", df$END.DATE)
df$dates_4=grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b", df$END.DATE)

df %>% mutate(end.date=ifelse(df$dates_2==T,mdy(END.DATE),ymd(END.DATE))) -> df
df$end.date.2=as.Date(df$end.date, origin = "1970-01-01")







#QUESTION 1
#TOTAL NUMBER OF PAYMENTS
nrow(df)
#3688493


#QUESTION 2
df$COVERAGE.PERIOD=(df$end.date.2-df$start.date.2)

df$COVERAGE.PERIOD=(difftime(df$end.date.2,df$start.date.2))
df$COVERAGE.PERIOD=((df$COVERAGE.PERIOD/60)/60)
sd(df$COVERAGE.PERIOD,na.rm=T)
#answer 2: 1,512 days

