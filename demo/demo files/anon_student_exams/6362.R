library(dplyr)
library(tidyverse)
lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE)[[1]]

# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F,fileEncoding="latin1")
}
##########################################
ConvertDates<-function(x){
  if (grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b",x)){
    return(as.Date(x,format='%m/%d/%y'))
  } else if (grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{4}\\b", x)){
    return(as.Date(x,format='%m/%d/%Y'))
  } else if (grepl("^\\d{4}-\\d{1,2}-\\d{1,2}", x)){
    return(as.Date(x,format='%Y-%m-%d'))
  } else {
    return(NA)
  }
}
# ###########################################
# as.num = function(x, na.strings = "NA") {
#   stopifnot(is.character(x))
#   na = x %in% na.strings
#   x[na] = 0
#   x = as.numeric(x)
#   x[na] = NA_real_
#   x
# }
# ##########################################
mylstdf=list()
##########################################
for(i in 1:length(lst_dfs)){
#for(i in 1:2){
  
  df<-lst_dfs[[i]]
  df<-df%>%transmute(PURPOSE=PURPOSE,
                     AMOUNT=suppressWarnings(as.numeric(gsub(',','',AMOUNT))),
                     #AMOUNT=as.numeric(gsub(',','',AMOUNT)),
                     OFFICE=gsub('[[:digit:]]+', '', OFFICE),
                     START.DATE=START.DATE,
                     END.DATE=END.DATE
                     )
  print(i)
  ###### Convert string to dates and unlisting properly while keeping date format####
  a1<-as.list(df$START.DATE)
  b1<-lapply(a1,ConvertDates)
  c1<-do.call("c", b1)
  df$START.DATE<-c1
  a2<-as.list(df$END.DATE)
  b2<-lapply(a2,ConvertDates)
  c2<-do.call("c", b2)
  df$END.DATE<-c2
  ############################
  df<-df[!duplicated(df[,'OFFICE']),]
  mylstdf[[i]]<-df
}
#########################################
#1 SUM AMOUNT
sumVec=vector()
for(i in 1:length(mylstdf)){
 sumVec=append(sumVec,sum(mylstdf[[i]]$AMOUNT,na.rm=TRUE))
}
sum(sumVec,na.rm=TRUE)

#2a Making only positive amounts matter
for(i in 1:length(mylstdf)){
  tempdf<-mylstdf[[i]]
  finaldf<-tempdf[tempdf$AMOUNT>0,]
  mylstdf[[i]]<-finaldf
}

#2b COVERAGE PERIOD
periodVec=vector()
for(i in 1:length(mylstdf)){
  diff_in_time<-mylstdf[[i]]$END.DATE-mylstdf[[i]]$START.DATE
  COVERAGE.PERIOD<-as.numeric(diff_in_time)
  periodVec=append(periodVec,COVERAGE.PERIOD)
}
sd(periodVec,na.rm=TRUE)

#3 Note! in the downloaded dataset the first 12 files are before december 31, 2016.
newsumVec<-sumVec[1:12]
mean(newsumVec[newsumVec>0])

#4 Note! in the downloaded dataset the last 3 files are after jan 2016.
comparevec=list()
for(i in 12:14){
  tempdf<-mylstdf[[i]]
  chosendf<-tempdf[which(tempdf$AMOUNT==max(tempdf$AMOUNT,na.rm=TRUE)),c('PURPOSE','AMOUNT')]
  print(chosendf)
  comparevec<-append(comparevec,chosendf)
}
finalcomparevec<-unlist(comparevec)
maxamount=finalcomparevec[which(finalcomparevec==max(as.numeric(finalcomparevec[c(2,4,6)])))]
maxpurpose=finalcomparevec[which(finalcomparevec==max(as.numeric(finalcomparevec[c(2,4,6)])))-1]          

#4b fraction of expenditure
fraction=as.numeric(maxamount)/sum(sumVec[12:14])
                      
                   

