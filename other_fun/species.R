# https://data.gov.au/data/dataset/threatened-species-state-lists/resource/c478a397-e1e9-4292-950c-e0f9ed9430c8
library(stringr)
library(dplyr)
fred <- read.csv('20201012spcs.csv')
fred <- fred %>%  
  mutate(
    report_name = case_when(Common.Name == "-" ~ Scientific.Name,
                                 TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    search_name = case_when(Common.Name == "-" ~ Scientific.Name,
                            TRUE ~ sapply(strsplit(Common.Name,", "), `[`, 1)),
    term_count = str_count(Common.Name,", ")) 
joe <- data.frame(fred)
for (row_val in seq(1,nrow(fred)-1))
     {
        if (fred[row_val,"term_count"]>0) {
            for (rep_no in seq(2,fred$term_count[row_val]+1))
                    joe <- rbind(joe,fred[row_val,])
                    joe[nrow(joe),"search_name"]= str_split(fred$Common.Name[row_val],
                                                            pattern=",",
                                                            simplify=TRUE)[rep_no]
  }
}
  
