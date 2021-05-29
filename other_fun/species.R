# https://data.gov.au/data/dataset/threatened-species-state-lists/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8
# 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'
# '20201012spcs.csv'

library(stringr)
library(tidyverse)
url <- 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'

raw_data <- read.csv(url,na.strings="-")
processed <- raw_data %>%  
  mutate(
    report_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                                 TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    search_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                          TRUE ~ Common.Name)) %>% 
    separate_rows(search_name,sep=", ")

# remove extra text after word Koala so we can find Koalas
processed$search_name[grep("Koala",processed$search_name)[1]] = "Koala"
# delete the incorrectly created row data 
processed <- processed[-grep("Koala",processed$Common.Name)[2],] 
