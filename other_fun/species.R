# https://data.gov.au/data/dataset/threatened-species-state-lists/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8
library(stringr)
library(dplyr)
raw_data <- read.csv('20201012spcs.csv')
raw_data <- raw_data %>%  
  mutate(
    report_name = case_when(Common.Name == "-" ~ Scientific.Name,
                                 TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    search_name = case_when(Common.Name == "-" ~ Scientific.Name,
                            TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    term_count = str_count(Common.Name,", ")) 

# copy and paste a lot of times rows with alternative common names separated by commas
processed <- data.frame(raw_data)
for (row_val in seq(1,nrow(fred)-1))
     {
        if (raw_data[row_val,"term_count"]>0) {
            for (rep_no in seq(2,raw_data$term_count[row_val]+1))
                    processed <- rbind(processed,raw_data[row_val,])
                    processed[nrow(processed),"search_name"]= str_split(raw_data$Common.Name[row_val],
                                                            pattern=",",
                                                            simplify=TRUE)[rep_no]
  }
}
# remove extra text after word Koala so we find Koalas
processed$search_name[grep("Koala",processed$search_name)[1]] = "Koala"
# delete the incorrectly created row data 
processed <- processed[-grep("Koala",processed$Common.Name)[2],] 
