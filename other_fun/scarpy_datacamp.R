# General-purpose data wrangling
library(tidyverse)  

# Parsing of HTML/XML files  
library(rvest)    
# 
library(purrr)

# String manipulation
library(stringr)   

# Verbose regular expressions
# library(rebus)  

   

# Eases DateTime manipulation
#library(lubridate)

# string matching
#library(fuzzywuzzyR)

css_list <- list(dc_counts =  '.dc-u-m-none',course_list = '.course-block__title',course_urls =  '.course-block__link',
        course_descriptions =  '.course-block__description', topic_names =  '.dc-u-mb-4', per_topic_data = 'p.dc-u-mt-0', 
        track_names = '.track-block__main', topic_urls = 'section.profile-topics a.shim', track_urls = 'section.profile-tracks a.shim',
    	titles_text =  'title', project_urls = 'section.profile-courses a.shim', project_names = '.dc-project-block__title' )
css_list[['dc_counts']]

html <- read_html('my_profile.txt')

scrape_css <- function(html,css){
	text_out <- html %>% 
	    # The '.' indicates the class
	    html_nodes(css) %>% 
	    # Extract the raw text as a list
	    html_text()                                      
}

scrape_summary <- function(html,css_list){
    dc_counts <- scrape_css(html,css_list[['dc_counts']])
    the_title <- scrape_css(html,css_list[['titles_text']])
    summary <- paste(the_title,'\n Total XP',dc_counts[2],'Total Courses',dc_counts[3],'Total Exercises', dc_counts[4],sep=' ')
    }


scrape_courses <- function(html,css_list){
    course_vec <- scrape_css(html,css_list[['course_list']]) %>% str_replace(c("\\n"=" "))
    urls <- scrape_css(html,css_list[['course_urls']])
    desc <- scrape_css(html,css_list[['course_descriptions']])
    courses <- data.frame(Course_Name = course_vec, Description = desc,URL = urls)
}


print(scrape_summary(html,css_list))
print(scrape_courses(html,css_list))

# html_nodes_text <- compose(html_text,html_nodes)
# print(html %% html_nodes_text(css_list[['dc_counts']]))

