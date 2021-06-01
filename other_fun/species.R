# https://data.gov.au/data/dataset/threatened-species-state-lists/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8
# 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'
# '20201012spcs.csv'

# Project Gutenberg's The Birds of Australia, Vol. 1 of 7
# https://www.gutenberg.org/ebooks/65002
# https://www.gutenberg.org/files/65002/65002-0.txt
f_name <- '01062021-074408-report.csv'
library(stringr)
library(tidyverse)
url <- 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'
# boa_file <- "Gutenberg eBook of The Birds of Australia vol 1.txt"
# more nlp fun
# birds_of_australia <- paste(readLines(boa_file), collapse=" ")

#boa_list <- unlist(strsplit(birds_of_australia, "\\.\\s\\D")) 
#boa_df <- data.frame(line_no = seq(1,length(boa_list)),text = tolower(boa_list))


raw_ebpc <- read.csv(f_name,na.strings="-", skip=1)
processed_ebpc <- raw_ebpc %>%  
  mutate(
    report_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                            Common.Name == "a tree" ~ Scientific.Name,
                            Common.Name == "a grass" ~ Scientific.Name,
                                 TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    search_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                          TRUE ~ Common.Name)) %>% 
    separate_rows(search_name,sep=", ") %>%
  mutate( search_name = case_when(search_name=='a tree' ~ Scientific.Name,
                                  search_name=='a grass' ~ Scientific.Name,
                                  nchar(search_name)<4 ~ Scientific.Name,
                                  TRUE ~ tolower(str_replace_all(search_name, 
                                                                 "[^[:alnum:] ]", ""))),
          report_name = str_replace_all(report_name, "[^[:alnum:] ]", ""))
  

# remove extra text after word Koala so we can find Koalas
processed_ebpc$search_name[grep("Koala",processed_ebpc$search_name)[1]] = "koala"
# delete the incorrectly created row data 
# processed_ebpc <- processed_ebpc[-grep("koala",processed_ebpc$Common.Name)[2],] 

# fred <- lapply(paste(processed_ebpc$search_name," ",sep=""),grep,boa_df$text)
# mmm <- sapply(paste(processed_ebpc$search_name," ",sep=""),grep,boa_df$text)
# data.frame(mmm)
# names(fred) <- processed_ebpc$search_name
# fred <- fred[lapply(fred, length) > 0]
# ddd <- data.frame(id = unlist(fred))
# ddd$names <- rownames(ddd)
# ddd['project'] = test[ddd$id,'project']
# rownames(ddd) <- NULL
# ddd$names <- gsub("[0-9]", "", ddd$names)
test <- data.frame( description =  c("a large fin whale (drop bear)","a small fin whale"
                                     ,"a southern right whale"),
                    project = c("project 1","project 1","project 2"))
fred <- lapply(paste(processed_ebpc$search_name,sep=""),grep,test$description)
names(fred) <- processed_ebpc$search_name
fred <- fred[lapply(fred, length) > 0]
ddd <- data.frame(id = unlist(fred))
ddd$names <- rownames(ddd)
ddd['project'] = test[ddd$id,'project']
rownames(ddd) <- NULL
ddd$names <- gsub("[0-9]", "", ddd$names)
ddd <- ddd[!duplicated(ddd$project),]

# l[grep("Falcon",boa_list)]
