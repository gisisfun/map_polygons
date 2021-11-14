libary(dplyr)
library(rvest)

content_5 <- read_html("http://dataquestio.github.io/web-scraping-pages/2014_super_bowl.html")

# Type your answer below
table_text <- content_5 %>% 
    html_node("table") %>%
    html_table()

print(table_text)
