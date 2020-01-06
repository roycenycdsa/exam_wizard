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

library(data.table)

#Clean Data
lst_fnames
lst_fnames = read.csv("./data/lst_fnames.txt",header = F)[[1]]
getwd()


#Brute force solution
hoExpenditureData <- read.csv(paste0("./data/","2009-Q3.csv"),stringsAsFactors = F)
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2009-Q4.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2010-Q1.csv"),stringsAsFactors = F))
#Starthere
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2010-Q2.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2010-Q3.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2010-Q4.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2011-Q1.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2011-Q2.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2011-Q3.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2011-Q4.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2012-Q1.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2012-Q2.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2012-Q3.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2012-Q4.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2013-Q1.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2013-Q2.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2013-Q3.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2013-Q4.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2014-Q1.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2014-Q2.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2014-Q3.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2014-Q4.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2015-Q1.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2015-Q2.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2015-Q3.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2015-Q4.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2016-Q1.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2016-Q2.csv"),stringsAsFactors = F))
hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/","2016-Q3.csv"),stringsAsFactors = F))

#structure changed columns mismatch
hoExpenditureData2 <- read.csv(paste0("./data/","2016-Q4.csv"),stringsAsFactors = F)
hoExpenditureData2 <- rbind(hoExpenditureData2,read.csv(paste0("./data/","2017-Q1.csv"),stringsAsFactors = F))

#structure changed columns mismatch
hoExpenditureData3 <- (read.csv(paste0("./data/","2017-Q2.csv")))
hoExpenditureData3 <- rbind(hoExpenditureData3,read.csv(paste0("./data/","2017-Q3.csv"),stringsAsFactors = F))
hoExpenditureData3 <- rbind(hoExpenditureData3,read.csv(paste0("./data/","2017-Q4.csv"),stringsAsFactors = F))
hoExpenditureData3 <- rbind(hoExpenditureData3,read.csv(paste0("./data/","2018-Q1.csv"),stringsAsFactors = F))

#structure changed columns mismatch
hoExpenditureData4 <- (read.csv(paste0("./data/","2018-Q2.csv"),stringsAsFactors = F))

#structure changed columns mismatch
hoExpenditureData5 <- (read.csv(paste0("./data/","2018-Q3.csv"),stringsAsFactors = F))
hoExpenditureData5 <- rbind(hoExpenditureData5,read.csv(paste0("./data/","2018-Q4.csv"),stringsAsFactors = F))

#given time constraints and issue with formatting of data frames only used data up to 2016 Q3

class(hoExpenditureData$OFFICE)


head(hoExpenditureData)

colnames(hoExpenditureData)
colnames(hoExpenditureData2)
colnames(hoExpenditureData3)
colnames(hoExpenditureData4)
colnames(hoExpenditureData5)


library(lubridate)

hoExpenditureData <- hoExpenditureData %>% mutate(StaDateNew = ifelse(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{4}\\b", START.DATE), 
                                                                as.Date(START.DATE, "%m/%d/%Y"),as.Date(START.DATE, "%m/%d/%y")))

hoExpenditureData <- hoExpenditureData %>% mutate(EndDateNew = ifelse(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{4}\\b", END.DATE), 
                                                                      as.Date(END.DATE, "%m/%d/%Y"),as.Date(END.DATE, "%m/%d/%y")))

pattern <- "([[:digit:]]+)([[:digit:]]+)([[:digit:]]+)([[:digit:]]+)"

hoExpenditureData <- hoExpenditureData %>% mutate(OFFICENEW = gsub(pattern,'',OFFICE))


x<-"2007 HON. JO ANN DAVIS"

ifelse(is.na(as.numeric(substr(x,1,4))),1,0)

gsub("[[:digits:]]",'',x)

gsub((x %like% "\\d"),"",x)

numbers <- grepl("^[:digit:]+$", x)
numbers

gsub("^[0:9]+",'',x)



gsub(pattern,'',x)

library(stringr)
yr <- c("2006", "2007", "2008","2009","2010","2011","2012","2013","2014","2015","2016")


#use for loop to read file names, better solution is probably to use for loop or lapply but for sake of time used method above
#for (f in lst_fnames) {
#  hoExpenditureData <- rbind(hoExpenditureData,read.csv(paste0("./data/", lst_fnames)))
#}


#Question 1

totalN <- hoExpenditureData %>% select(PAYEE) %>% summarise(n = sum(n()))
totalN

hoExpenditureData <- hoExpenditureData %>% mutate(COVERAGE.PERIOD = (EndDateNew - StaDateNew))

#Question 2
CPSD <- hoExpenditureData %>% filter(COVERAGE.PERIOD > 0) %>% summarise(CoverageSD = sd(COVERAGE.PERIOD))
CPSD
colnames(hoExpenditureData)

head(hoExpenditureData$AMOUNT)

#Question 3
dateLow <- as.numeric(as.Date("1/1/2010", "%m/%d/%Y"))
dateHigh <- as.numeric(as.Date("12/31/2016", "%m/%d/%Y"))

amountsPay <- hoExpenditureData %>% filter(StaDateNew >= dateLow & StaDateNew <= dateHigh) %>% 
  mutate(AmountNum = as.numeric(gsub(",", "", AMOUNT))) %>% filter(AmountNum > 0) %>% 
  group_by(YEAR) %>% summarise(totalAnnExp = mean(AmountNum))

amountsPay

#Question 4
dL <- as.numeric(as.Date("1/1/2016", "%m/%d/%Y"))
dH <- as.numeric(as.Date("12/31/2016", "%m/%d/%Y"))

byOffice <- hoExpenditureData %>% filter(StaDateNew >= dL & StaDateNew <= dH) %>% 
  mutate(AmountNum = as.numeric(gsub(",", "", AMOUNT))) %>% filter(AmountNum > 0) %>% 
  group_by(OFFICE) %>% summarise(totalExp = sum(AmountNum)) %>% arrange(desc(totalExp)) %>% top_n(1, totalExp)

byOffice

total <- hoExpenditureData %>% filter(StaDateNew >= dL & StaDateNew <= dH) %>% 
  mutate(AmountNum = as.numeric(gsub(",", "", AMOUNT))) %>% filter(AmountNum > 0) %>% 
  summarise(TotalAllExp = sum(AmountNum))

total

byOfficePurp <- hoExpenditureData %>% filter(StaDateNew >= dL & StaDateNew <= dH) %>% 
  mutate(AmountNum = as.numeric(gsub(",", "", AMOUNT))) %>% filter(AmountNum > 0) %>% 
  filter(OFFICE == "GOVERNMENT CONTRIBUTIONS") %>% 
  group_by(OFFICE,PURPOSE) %>% 
  summarise(totalExp = sum(AmountNum)) %>% 
  arrange(desc(totalExp)) %>% top_n(1, totalExp) %>% mutate(PctofTotal = totalExp/total$TotalAllExp * 100)

byOfficePurp
