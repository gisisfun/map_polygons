# https://data.gov.au/data/dataset/threatened-species-state-lists/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8
# 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'
# '20201012spcs.csv'

# Project Gutenberg's The Birds of Australia, Vol. 1 of 7
# https://www.gutenberg.org/ebooks/65002
# https://www.gutenberg.org/files/65002/65002-0.txt
f_name <- '20201012spcs.csv'
library(stringr)
library(tidyverse)
url <- 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'

raw_ebpc <- read.csv(f_name,na.strings="-")
processed_ebpc <- raw_ebpc %>%  
  mutate(
    report_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                                 TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    search_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                          TRUE ~ Common.Name)) %>% 
    separate_rows(search_name,sep=", ")

# remove extra text after word Koala so we can find Koalas
processed_ebpc$search_name[grep("Koala",processed_ebpc$search_name)[1]] = "Koala"
# delete the incorrectly created row data 
processed_ebpc <- processed_ebpc[-grep("Koala",processed_ebpc$Common.Name)[2],] 

# more nlp fun
birds_of_australia <- paste(readLines("Gutenberg eBook of The Birds of Australia vol 1.txt"), collapse=" ")
# split to lines
l <- unlist(strsplit(birds_of_australia, "\\.\\s\\D"))
# return lines where "Falcon" is present
l[grep("Falcon",l)]
