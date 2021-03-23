# General-purpose data wrangling
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


# Verbose regular expressions
# library(rebus)  


# Eases DateTime manipulation
#library(lubridate)

# string matching
#library(fuzzywuzzyR)



# Verbose regular expressions
# library(rebus)  


# Eases DateTime manipulation
#library(lubridate)

# string matching
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

scrape_courses <- function(html,css_list,xpath_list){
  lang <-  scrape_xpath_list(html,xpath_list[['course_lang']])#  %>% str_replace('<div class=\"course-block__technology course-block__technology--','') 
  course_vec <- scrape_css_list(html,css_list[['course_list']]) 
  urls <- scrape_css_attr(html,css_list[['course_urls']]) 
  desc <- scrape_css_list(html,css_list[['course_descriptions']]) %>% str_replace('\n','') %>% str_trim()
  courses <- data.frame(Technology = lang,Course_Name = course_vec, Description = desc,URL = urls)
  #courses$Technology <- str_sub(courses$Technology, end=-9) 
   }

xpath_list= list(course_lang =  '//div[contains(@class,"course-block__technology course-block__technology--")]')
css_list <- list(dc_counts =  '.dc-u-m-none',course_list = '.course-block__title',course_urls = '.course-block__link',
                 course_descriptions =  '.course-block__description', topic_names =  '.dc-u-mb-4', per_topic_data = 'p.dc-u-mt-0', 
                 track_names = '.track-block__main', topic_urls = 'section.profile-topics a.shim', track_urls = 'section.profile-tracks a.shim',
                 titles_text =  'title', project_urls = 'section.profile-courses a.shim', project_names = '.dc-project-block__title' )
css_list[['dc_counts']]

html <- read_html('my_profile.txt')

print(scrape_summary(html,css_list))
fred2 <-  scrape_courses(html,css_list,xpath_list) 
fred2$Technology <- str_sub(fred2$Technology, end=-9) 

# html_nodes_text <- compose(html_text,html_nodes)
# print(html %% html_nodes_text(css_list[['dc_counts']]))



read_pdfs <- function(){
  course_files <- list.files('Datacamp/Courses', full.names = TRUE, 
                             recursive = TRUE,pattern = "certificate.pdf$")
  skill_files <- list.files('Datacamp/Tracks/Skill', full.names = TRUE, 
                            recursive = TRUE,pattern = "certificate.pdf$")
  career_files <- list.files('Datacamp/Tracks/Career', full.names = TRUE,
                             recursive = TRUE,pattern = "certificate.pdf$")
  
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


scrape_css_attr <- function(html,css,attr_val="href"){
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

scrape_courses <- function(html,css_list,xpath_list){
  lang <-  scrape_xpath_list(html,xpath_list[['course_lang']])  %>% str_replace("<div class=\"course-block__technology course-block__technology--","") 
  course_vec <- scrape_css_list(html,css_list[['course_list']]) 
  urls <- scrape_css_attr(html,css_list[['course_urls']]) 
  desc <- scrape_css_list(html,css_list[['course_descriptions']]) %>% str_replace('\n','') %>% str_trim()
  courses <- data.frame(Technology = lang,Course_Name = course_vec, Description = desc,URL = urls)
  #courses$Technology <- str_sub(courses$Technology, end=-9) 
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
courses$Technology <- str_sub(fred2$Technology, end=-9) 
certs <- pdf_paths() 

names(certs)

# html_nodes_text <- compose(html_text,html_nodes)
# print(html %% html_nodes_text(css_list[['dc_counts']]))

#stringdist_inner_join(certs,method="jaccard", by = c(Course_Name = "course"),distance_col="distance")
# filter(distance>0.04,distance < 0.0905) %>%
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




