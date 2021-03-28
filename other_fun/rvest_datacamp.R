#DataCamp Summary of Courses Tracks and Projects
# Sourced from html from profile page (my_profile.txt) and pdf certificates
# stored in subdirectories (Courses, Skills, Career)
# 
# scrapy_datacamp.py (this code)
# my_profile.txt (html source dumped to file)
# 
# Datacamp --|
#   \ -Courses-   \ 
#   |             \ -Course Name- \
#   |                             \ -certificate.pdf
#   \ -Tracks-     \
#                  \ -Skills      -\
#                                  \ -Track Name- \
#                                                \ -certificate.pdf  
#                  \ -Career-      \ 
#                                  \ -Track Name- \
#                                                 \ -certificate.pdf             
# 
# 
# 
# Uses a range of Python knowledge gained from Data Camp Courses
# - Web page scraping
# - Natural Language Processing - TODO
# - Data Cleaning
# - Data Visualisation 
# - Excel Document creation - TODO


#General-purpose data wrangling
library(tidyverse)  

# Parsing of HTML/XML files  
library(rvest)    
# 
library(purrr)
#https://www.r-bloggers.com/2018/01/how-to-extract-data-from-a-pdf-file-with-r/
# String manipulation
library(stringr)   
# General-purpose data wrangling
library(tidyverse)  

# Parsing of HTML/XML files  
library(rvest)    
# 
library(purrr)

# String manipulation
library(stringr)   

#
library(pdftools)

#
library(caret)

library(dplyr)
# arima
library(astsa)

# Verbose regular expressions
# library(rebus)  


# Eases DateTime manipulation
#library(lubridate)

# string matching
#library(fuzzywuzzyR)



# Verbose regular expressions
# library(rebus)  

library(ggplot2)

# Eases DateTime manipulation
#library(lubridate)
#or
library(xts)

# fuzzy string matching
library(fuzzyjoin)

pdf_read <- function(url) {
   pdf_text(url) %>% str_split('\n') 
}

raw_df <-  function(raw_list,type_label) {
  raw_pdf <- map(raw_list,pdf_read)
  lines <- map_chr(raw_pdf,~ as.character(.x)) %>% str_split('"') 
  line1 <- lines %>% map(~.x[2]) %>% unlist()
  line2 <- lines %>% map(~.x[4]) %>% unlist()
  line3 <- lines %>% map(~.x[6]) %>% unlist()
  line4 <- lines %>% map(~.x[8]) %>% unlist()
  line5 <- lines %>% map(~.x[10]) %>% unlist()

  processed <- data.frame(path = raw_list,cert_no = line1,course = line3, date = line4, extra = line5) %>%
      mutate(course = ifelse(extra == "",paste(course),paste(course,date,sep=" "))) %>%
      mutate(date = ifelse(extra == "",paste(date),paste(extra))) %>%
      select(-extra) %>% mutate(Type = type_label)
}

pdf_paths <- function() {
  course_files <- list.files('Datacamp/Courses', full.names = TRUE, 
                             recursive = TRUE,pattern = "certificate.pdf$")
  skill_files <- list.files('Datacamp/Tracks/Skill', full.names = TRUE, 
                            recursive = TRUE,pattern = "certificate.pdf$")
  career_files <- list.files('Datacamp/Tracks/Career', full.names = TRUE,
                             recursive = TRUE,pattern = "certificate.pdf$")
 courses <- raw_df(course_files,'Course')
 skill <- raw_df(skill_files,'Skill')
 career <- raw_df(career_files,'Career')
 rbind(courses,skill,career) %>% 
mutate(course = str_replace(course,'So ware','Software')) %>% 
mutate(course = str_replace(course,'E cient','Efficient')) %>% 
mutate(course = str_replace(course,'Air ow','Airflow')) %>% 
mutate(course = str_replace(course,'E ects','Effects')) %>% 
mutate(course = str_replace(course,'lea et','leaflet'))%>%
mutate(course = str_replace(course,'Classi cation','Classification'))%>%
mutate(course = str_replace(course,'Classi ers','Classifiers'))
}

scrape_xpath_list <- function(html,x_path){
  text_out <- html %>% 
    # The '.' indicates the class
    html_nodes(xpath = x_path) %>% 
    # Extract the raw text as a list
    as.character()                                      
}

scrape_css_list <- function(html,css){
  text_out <- html %>% 
    # The '.' indicates the class
    html_nodes(css) %>% 
    # Extract the raw text as a list
    html_text()                                      
}


scrape_css_attr <- function(html, css, attr_val = 'href'){
  text_out <- html %>% 
    # The '.' indicates the class
    html_nodes(css) %>% 
    # Extract the raw text as a list
    html_attr(attr_val)                                      
}

scrape_summary <- function(html,css_list){
  dc_counts <- scrape_css_list(html,css_list[['dc_counts']])
  the_title <- scrape_css_list(html,css_list[['titles_text']])
  summary <- paste(the_title,'\n Total XP',dc_counts[2],'Total Courses',dc_counts[3],'Total Exercises', dc_counts[4],sep=' ')
}


scrape_tracks <- function(html,css_list,certs){
  certs_tracks <-certs %>% filter(Type %in% c("Career","Skill")) 
  name <- scrape_css_list(html,css_list[['track_names']]) %>% 
    str_replace_all('\n','') %>%
    str_replace('        ',' ') %>%
    str_replace('   ',' ') %>%
    str_replace('  with',' with') %>%
    str_trim() %>%
    str_c(.," Track")
  
  tracks_raw <- data.frame(course = name) 
  tracks <- merge(tracks_raw,certs_tracks,by='course') %>% 
    mutate(date = as.Date(date,"%b %d, %Y"))  %>% 
    arrange(date)
  }


scrape_courses <- function(html,css_list,xpath_list){
  lang <-  scrape_xpath_list(html,xpath_list[['course_lang']])#  %>% str_replace('<div class=\"course-block__technology course-block__technology--','') 
  course_vec <- scrape_css_list(html,css_list[['course_list']]) 
  urls <- scrape_css_attr(html,css_list[['course_urls']]) 
  desc <- scrape_css_list(html,css_list[['course_descriptions']]) %>% str_replace('\n','') %>% str_trim()
  courses <- data.frame(Technology = lang,Course_Name = course_vec, Description = desc,URL = urls)
  #courses$Technology <- str_sub(courses$Technology, end=-9) 
   }


courses_and_certs<- function(courses,certs) {
  course_certs <- filter(certs,Type=="Course") %>% mutate(Type=Type)
  
  three_dots <- str_detect(courses$Course_Name,'\\.\\.')
  
  courses_trunc <- courses[three_dots,]
  
  courses_fuzzy_trunc <- courses_trunc %>%
    stringdist_left_join(course_certs,method="jaccard", max_dist = 0.2,by = c(Course_Name = "course"),distance_col="distance") %>% 
    select(-distance) %>% mutate(Course_Name=course) %>% 
    select(Course_Name,Technology,Description,URL,path,cert_no,date,Type,-course)
  
  courses_match <- courses[!three_dots,]
  courses_join_match <- courses_match %>%
    merge(course_certs,by.x='Course_Name', by.y='course') %>% bind_rows(courses_fuzzy_trunc)
  
  dummy <- dummyVars(" ~ Technology", data=courses_join_match)
  
  dummy_df <- courses_join_match %>% 
    bind_cols(data.frame(predict(dummy, newdata = courses_join_match)))
}

time_series <- function(courses_certs) {
  date_prep <- courses_certs %>% select(starts_with("Technology"),-Technology)
  #date_prep <- date_prep  %>% mutate_if(as.numeric())
  names(date_prep) <- gsub(x = names(date_prep), pattern = "Technology", replacement = "") 
  time_raw <- xts(date_prep,order.by = as.Date(courses_certs$date, "%b %d, %Y") )
  
}



xpath_list= list(course_lang =  '//div[contains(@class,"course-block__technology course-block__technology--")]')
css_list <- list(dc_counts =  '.dc-u-m-none',course_list = '.course-block__title',course_urls = '.course-block__link',
                 course_descriptions =  '.course-block__description', topic_names =  '.dc-u-mb-4', per_topic_data = 'p.dc-u-mt-0', 
                 track_names = '.track-block__main', topic_urls = 'section.profile-topics a.shim', track_urls = 'section.profile-tracks a.shim',
                 titles_text =  'title', project_urls = 'section.profile-courses a.shim', project_names = '.dc-project-block__title' )
css_list[['dc_counts']]

html <- read_html('my_profile.txt')
print(scrape_summary(html,css_list))

courses <-  scrape_courses(html,css_list,xpath_list) 
courses['Technology'] <- str_sub(courses$Technology, end=-9) 
courses['Technology'] <- str_replace(courses$Technology,'<div class="course-block__technology course-block__technology--','')

certs <- pdf_paths() 

names(certs)

courses_certs <- courses_and_certs(courses,certs)
tracks_certs <- scrape_tracks(html,css_list,certs)

daily_xts <- time_series(courses_certs)
daily_cumsum_xts <- cumsum(daily_xts)
twoweeks_ep <- endpoints(daily_cumsum_xts, on = "weeks")

twoweeks_xts <- daily_cumsum_xts[twoweeks_ep]

twoweeks_df <- as.data.frame(twoweeks_xts)
twoweeks_df$date <- as.Date(rownames(twoweeks_df))

chart_data <- gather(twoweeks_df, values=-date )


#c(r,python,excel,git,power_bi,theory,tableau,sql,spreadsheets,shell,scala)
chart_data %>% filter(key %in% c("r","python","sql")) %>% 
  ggplot(aes(x=date,y=value,color=key)) + geom_line() + geom_line() +
  labs(title = "R, Python and SQL Course Cumulative Progress",
       subtitle="Track certificate completion dates marked as vertical dotted lines",
       caption = "Source: https://github.com/gisisfun/map_polygons/blob/master/other_fun/rvest_datacamp.R") +
  xlab("Time (Two Week interval)") +
  ylab("Cumulative Course Count") +
  geom_smooth(method="glm",se=FALSE, method.args = list(family = "poisson")) +
  geom_vline(xintercept=as.vector(tracks_certs$date), linetype="dotted")
ggsave("R_Python.png")

chart_data %>% filter(!key %in% c("r","python","sql")) %>% 
  ggplot(aes(x=date,y=value,color=key)) + geom_line() + geom_line() +
  labs(title = "Other Courses Cumulative Progress",
       caption = "Source: https://github.com/gisisfun/map_polygons/blob/master/other_fun/scrapy_datacamp.R") +
  xlab("Time (Two Week interval)") +
  ylab("Cumulative Course Count") +
  geom_smooth(method="glm",se=FALSE, method.args = list(family = "poisson"))
ggsave("Other.png")









