# https://data.gov.au/data/dataset/threatened-species-state-lists/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8
library(stringr)
library(dplyr)
raw_data <- read.csv('20201012spcs.csv',na.strings="-")
processed <- raw_data %>%  
  mutate(
    report_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                                 TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    names_to_split = case_when(is.na(Common.Name) ~ Scientific.Name,
                          TRUE ~ Common.Name)) %>% 
    separate_rows(names_to_split,sep=", ")
