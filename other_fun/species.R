# https://www.environment.gov.au/sprat-public/


f_name <- '05062021-063319-report.csv'
library(stringr)
library(tidyverse)
library(readr)
library(ggplot2)
library(forcats)
url <- 'https://data.gov.au/data/dataset/ae652011-f39e-4c6c-91b8-1dc2d2dfee8f/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8/download/20201012spcs.csv'
# boa_file <- "Gutenberg eBook of The Birds of Australia vol 1.txt"
# more nlp fun
# birds_of_australia <- paste(readLines(boa_file), collapse=" ")

#boa_list <- unlist(strsplit(birds_of_australia, "\\.\\s\\D")) 
#boa_df <- data.frame(line_no = seq(1,length(boa_list)),text = tolower(boa_list))

# some test project data
test_df <- data.frame( description =  c("a large fin whale and koala (drop bear)","a small fin whale"
                                     ,"a southern right whale","Australian white ibis (Threskiornis molucca) or Bin Chicken"),
                    project_name = c("project 1","project 1","project 2","project 3"),
                    
                    project_id = c("p1","p1","p2","p3"))

# standardise the test data column names for analysis
ref_data <- test_df %>% mutate(search_text = description,
                               name = project_name,
                               ident= project_id) %>%
  mutate(source="test data")
# subset the EPBC species 
raw_epbc <- read_csv(f_name,skip=1) %>% dplyr::rename_all(make.names)  %>%
  filter(!is.na(EPBC.Threat.Status))
# list of generic common names
# need some code needed to generate this vector in the future
gen_names <- c("a tree","a land snail","a fern","a daisy","a grass",
               "a herb","a filmy fern","a hellicaronid land animal",
               "a leek-orchid","a mint-bush","A native bee","a palm",
               "a sedge","a short-tongued bee","a shrub","a bottlebrush",
               "a creeper, Clematis","a triggerplant","a vine",
               "a stringybark","a spike rush")


# produce the the linkage data from test and 
link_df <- raw_epbc  %>%
  mutate( 
    report_name = case_when(is.na(Common.Name) ~ Scientific.Name,
                            Common.Name %in% gen_names ~ Scientific.Name,
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
  mutate(project_id = ref_data[lookup,'ident'],
         project_name = ref_data[lookup,'name'],
         source_text = ref_data[lookup,'source']) %>% 
  distinct(Taxon.ID,Scientific.Name,report_name,EPBC.Threat.Status,Taxon.Group,
           project_id,project_name,source_text)

# make a summary table
summary_table <- link_df %>% 
  group_by(Taxon.Group,EPBC.Threat.Status,project_name) %>%
  summarise(project_count=n()) %>%
  arrange(desc(project_count))
print(summary_table)

# a bar chart 
link_df %>% 
  group_by(EPBC.Threat.Status,Taxon.Group) %>%
  summarise(project_count=n()) %>%
  ungroup() %>%
  mutate(EPBC.Threat.Status = fct_reorder(EPBC.Threat.Status, 
                                          desc(project_count))) %>%
  ggplot(aes(x=EPBC.Threat.Status, y=project_count)) +
  geom_col(aes(fill = Taxon.Group)) +
  ggtitle("EBPC Threatened Species by Taxonomy Group in test data")


# todo 
# read input from Excel file format
# save tables to Excel file Format
# a customised word document with fixed commentary, tables and charts
