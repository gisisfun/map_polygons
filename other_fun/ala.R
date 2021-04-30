library(dplyr)
library(httr)
library(rjson)
library(stringi)
url = "https://biocache-ws.ala.org.au/ws/occurrences/search?q=genus:%22Macropus%22"
getdata <- GET(url=url)

listdata <- fromJSON(content(getdata,type="text"))


#do.call(rbind,lapply(listdata$occurrences,data.frame))


#bind_rows(listdata$occurrences)

 
res <- as.data.frame(t(stri_list2matrix(listdata$occurrences)))
colnames(res) <- unique(unlist(sapply(listdata$occurrences, names)))
names(res) <- names(listdata$occurrences[[1]]) 