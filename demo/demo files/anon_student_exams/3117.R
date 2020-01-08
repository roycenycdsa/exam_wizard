# Libraries

library(dplyr)
library(data.table)

lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE)[[1]]


# Load all files and combine

lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

View(lst_dfs)




# Convert AMOUNT to numeric type


for(fname in lst_fnames){
   lst_dfs[[fname]]$AMOUNT = as.numeric(gsub(",", "",
                                                    lst_dfs[[fname]]$AMOUNT,
                                                    fixed = TRUE))
}




# Remove "yyyy" or "FISCAL YEAR yyyy" from OFFICE



for(fname in lst_fnames){
  lst_dfs[[fname]]$OFFICE = trimws(gsub("[0-9]|FISCAL YEAR", "" ,
                                            lst_dfs[[fname]]$OFFICE,
                                            fixed = FALSE))
}




# Convert START.DATE and END.DATE to date type


View(lst_dfs[["2018-Q3.csv"]])


for(fname in lst_fnames){
  lst_dfs[[fname]]$START.DATE = if_else(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b",
                                              lst_dfs[[fname]]$START.DATE),
                                        as.Date(lst_dfs[[fname]]$START.DATE,
                                                format = "%m/%d/%y",
                                                optional = TRUE),
                                        if_else(grepl("^\\d{4}\\b/\\d{1,2}\\b/\\d{1,2}\\b",
                                                      lst_dfs[[fname]]$START.DATE),
                                                as.Date(lst_dfs[[fname]]$START.DATE,
                                                        format = "%Y/%m/%d",
                                                        optional = TRUE),
                                        if_else(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{4}\\b",
                                                      lst_dfs[[fname]]$START.DATE),
                                                as.Date(lst_dfs[[fname]]$START.DATE,
                                                        optional = TRUE),
                                                as.Date("01/01/1900"))))


    lst_dfs[[fname]]$END.DATE = if_else(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{2}\\b",
                                              lst_dfs[[fname]]$END.DATE),
                                        as.Date(lst_dfs[[fname]]$END.DATE,
                                                format = "%m/%d/%y",
                                                optional = TRUE),
                                        if_else(grepl("^\\d{1,2}\\b/\\d{1,2}\\b/\\d{4}\\b",
                                                      lst_dfs[[fname]]$END.DATE),
                                                as.Date(lst_dfs[[fname]]$END.DATE,
                                                        optional = TRUE),
                                                as.Date("01/01/1900")))
  
}
  
?as.Date


# Questions:


lst_dfs_selected = list()

for(fname in lst_fnames){
  lst_dfs_selected[[fname]] = lst_dfs[[fname]] %>% 
    select (., PURPOSE, AMOUNT, OFFICE, START.DATE, END.DATE)
  
}

View(lst_dfs_selected[[1]])

df = bind_rows(lst_dfs_selected, .id = "id")  

View(df)



# Question 01


total_payment = df %>% 
  summarise(., payment = sum(AMOUNT, na.rm = TRUE))

total_payment


# Question 02

coverage_df = df %>% 
  filter(., AMOUNT > 0) %>% 
  summarise(., coverage.sd = sd(END.DATE - START.DATE, na.rm = TRUE))

coverage_df


# Question 03












