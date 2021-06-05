# https://www.environment.gov.au/sprat-public/


f_name <- '05062021-063319-report.csv'
library(stringr)
library(tidyverse)
library(readr)
url <- 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'
# boa_file <- "Gutenberg eBook of The Birds of Australia vol 1.txt"
# more nlp fun
# birds_of_australia <- paste(readLines(boa_file), collapse=" ")

#boa_list <- unlist(strsplit(birds_of_australia, "\\.\\s\\D")) 
#boa_df <- data.frame(line_no = seq(1,length(boa_list)),text = tolower(boa_list))

test_df <- data.frame( description =  c("a large fin whale and koala (drop bear)","a small fin whale"
                                     ,"a southern right whale"),
                    project = c("project 1","project 1","project 2"))

ref_data <- test_df %>% mutate(search_text = description, 
                               project = project)

raw_epbc <- read_csv(f_name,skip=1) 

link_df <- raw_epbc %>%
  dplyr::rename_all(make.names) %>%
  filter(!is.na(EPBC.Threat.Status)) %>%
  mutate( 
    report_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                            Common.Name == "a tree" ~ Scientific.Name,
                            Common.Name == "a grass" ~ Scientific.Name,
                            TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    search_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                            TRUE ~ paste(Common.Name,sep=""))) %>% 
  separate_rows(search_name,sep=", ") %>%
  mutate(search_name = case_when(search_name=='a tree' ~ Scientific.Name,
                                  search_name=='a grass' ~ Scientific.Name,
                                  str_detect(Common.Name,fixed("Koala")) ~ "koala",
                                  nchar(search_name)<3 ~ Scientific.Name,
                                  TRUE ~ tolower(search_name))) %>% 
  mutate(lookup = map(paste(" ",search_name,sep=""),grep,ref_data$search_text,
      fixed=TRUE,ignore.case=TRUE)) %>% 
  unnest(lookup) %>% 
  mutate( project = ref_data[lookup,'project']) %>% 
  distinct(report_name,project)
