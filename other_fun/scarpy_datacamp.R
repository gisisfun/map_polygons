# General-purpose data wrangling
library(tidyverse)  

# Parsing of HTML/XML files  
library(rvest)    
# 
library(purrr)

# String manipulation
# library(stringr)   

# Verbose regular expressions
# library(rebus)  

   

# Eases DateTime manipulation
library(lubridate)

# string matching
library(fuzzywuzzyR)

css_list <- list(dc_counts =  '.dc-u-m-none',course_list = '.course-block__title',course_urls =  '.course-block__link',
        course_descriptions =  '.course-block__description', topic_names =  '.dc-u-mb-4', per_topic_data = 'p.dc-u-mt-0', 
        track_names = '.track-block__main', topic_urls = 'section.profile-topics a.shim', track_urls = 'section.profile-tracks a.shim',
    	titles_text =  'title', project_urls = 'section.profile-courses a.shim', project_names = '.dc-project-block__title' )
css_list[['dc_counts']]

html <- read_html('my_profile.txt')

scrape_summary <- function(html,css_list){

    data1 <- html %>% 
	# The '.' indicates the class
	html_nodes(css_list[['dc_counts']]) %>% 
	# Extract the raw text as a list
	html_text()                   

    data2 <- html %>% 
	# The '.' indicates the class
	html_nodes(css_list[['dc_counts']]) %>% 
	# Extract the raw text as a list
	html_text()                   
    page_data <- list(data1,data2)

      # The second to last of the buttons is the one
#      pages_data[(length(pages_data)-1)] %>%            
        # Take the raw string
#        unname() %>%                                     
        # Convert to number
#        as.numeric()                                     
    }
print(scrape_summary(html,css_list))

# html_nodes_text <- compose(html_text,html_nodes)
# print(html %% html_nodes_text(css_list[['dc_counts']]))

