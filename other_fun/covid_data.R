library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)
file_name <- "time_series_covid19_confirmed_global.csv"
file_path <- file.path('COVID-19',
                       'csse_covid_19_data',
                       'csse_covid_19_time_series',
                       file_name)
file_df <- read.csv(file_path)


aust_df <- file_df %>% 
        gather(key="date", value = "confirmed", 
         -c("Province.State","Country.Region","Lat","Long")) %>%
        mutate(date = str_replace(date,"X","")) %>%
        mutate(date = str_replace_all(date,"[.]","-")) %>%
        mutate(date = as.POSIXct(date, format="%m-%d-%y")) %>%
        filter(Country.Region=="Australia")

plot_df <- aust_df %>% group_by(date) %>%
  summarise(total = sum(confirmed))
plot(plot_df$date,plot_df$total)
