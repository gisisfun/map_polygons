# MERIT Tablecloth.R
# --------------


library(stringr)
require(lubridate)
require(tidyverse)
require(dplyr)
require(readr)
require(tidyr)
require(janitor)
library(openxlsx)

#read_excel(xlsx_example, sheet = "chickwts")
# change this value set extract data and locate the named files
extract_date <- '2022-05-02'
# 3weeks after start of current quarter period
report_date <- as.Date(date(),format="%a %b %d %H:%M:%S %Y")
report_date_qtr <- quarter(report_date,fiscal_start=7)
report_date_yr_qtr <- quarter(report_date,with_year=TRUE,fiscal_start=7)
#first of quarter containing report date 31-03-2022 21-04-2022

if (report_date_qtr==2) {
  threshold_days <- 14 
} else  {
threshold_days<- 7
}
current_qtr_start_date <- quarter(report_date,type="date_first",fiscal_start=7) 
due_date <- current_qtr_start_date + days(threshold_days)
prev_qtr_date <- quarter(report_date,type="date_first",fiscal_start=7)-months(3)

# list of of management unit names, ids and states
# mu_list <- read_csv('management_units_list.csv') %>% 
#   clean_names()
load("management_units.Rdata")

whats_my_classification <- function(stage) {
  case_when(
    str_detect(stage,"Outputs Report$") ~ "Outputs",
    str_detect(stage,"^Outputs Report.*") ~"Outputs",
    str_detect(stage,"2018/2019 - 3M Outputs Report 04") ~ "Outputs",
    str_detect(stage,"^Annual.*") ~ "Annual",
    str_detect(stage,"^Outcomes Report 1") ~ "Short Term",
    str_detect(stage,"^Outcomes Report 1.*") ~ "Short Term",
    str_detect(stage,"^Outcomes Report 2") ~ "Medium Term",
    str_detect(stage,"^Outcomes Report 2.*") ~ "Medium Term",
    str_detect(stage,"^Adjustment.*") ~ "Adjustment",
    TRUE ~ "Other")
}

whats_my_duration <- function(stage, report_from_date, report_to_date) {
  case_when(
    str_detect(stage,"^Outputs Report.*") & 
      round(as.numeric(difftime(report_to_date, report_from_date, 
                                units = "days"))/(365.25/12),0) <= 3 ~ "Quarter",
    str_detect(stage,"^Outputs Report.*") & 
      round(as.numeric(difftime(report_to_date, report_from_date, 
                                units = "days"))/(365.25/12),0) == 6 ~ "Semester",
    str_detect(stage,"^Outcomes Report 1")  ~ "Short Term",
    str_detect(stage,"^Outcomes Report 2")  ~ "Medium Term",
    str_detect(stage,"^Outcomes Report 1.*")  ~ "Short Term",
    str_detect(stage,"^Outcomes Report 2.*")  ~ "Medium Term",
    str_detect(stage,"Quarter 1 Outputs Report$")  ~ "Quarter",
    str_detect(stage,"Quarter 2 Outputs Report$")  ~ "Quarter",
    str_detect(stage,"Quarter 3 Outputs Report$")  ~ "Quarter",
    str_detect(stage,"Quarter 4 Outputs Report$")  ~ "Quarter",
    str_detect(stage,"Semester 1 Outputs Report$")  ~ "Semester",
    str_detect(stage,"Semester 2 Outputs Report$")  ~ "Semester",
    str_detect(stage,"^Annual.*")  ~ "Annual",
    str_detect(stage,"^Adjustment.*")  ~ "Adjustment",
    str_detect(stage,"2018/2019 - 3M Outputs Report 04")  ~ "Quarter",
    # round(as.numeric(difftime(report_to_date, report_from_date, 
    #                           units = "days"))/(365.25/12),0) <= 3 ~ "Quarter",
    # round(as.numeric(difftime(report_to_date, report_from_date, 
    #                           units = "days"))/(365.25/12),0) == 6 ~ "Semester",
    TRUE ~ "Other")
  }

whats_my_interval <- function(stage, report_from_date, report_to_date){
  case_when(
    str_detect(stage,"Progress Report 1.*") ~ "Other",
    str_detect(stage,"Progress Report 2.*") ~ "Other",
    str_detect(stage,"^Outcomes Report 1") ~ "Other",
    str_detect(stage,"^Outcomes Report 1.*") ~ "Other",
    str_detect(stage,"^Outcomes Report 2") ~ "Other",
    str_detect(stage,"^Outcomes Report 2.*") ~ "Other",
    str_detect(stage,"^Outputs Report 1") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/ (365.25/12),0) <= 3 ~ "Quarter 1",
    str_detect(stage,"^Outputs Report 1") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/(365.25/12),0) == 6 ~ "Semester 1",
    str_detect(stage,"^Outputs Report 2") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/ (365.25/12),0) <= 3 ~ "Quarter 2",
    str_detect(stage,"^Outputs Report 2") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/ (365.25/12),0) == 6 ~ "Semester 2",
    str_detect(stage,"^Outputs Report 3") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/ (365.25/12),0) <= 3 ~ "Quarter 3",
    str_detect(stage,"^Outputs Report 3") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/ (365.25/12),0) == 6 ~ "Semester 3",
    str_detect(stage,"^Outputs Report 4") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/ (365.25/12),0) <= 3 ~ "Quarter 4",
    str_detect(stage,"^Outputs Report 4") & round(
      as.numeric(difftime(report_to_date, 
                          report_from_date, 
                          units = "days"))/  (365.25/12),0) == 6 ~ "Semester 4",
    str_detect(stage,"Quarter 1 Outputs Report") ~ "Quarter 1",
    str_detect(stage,"Quarter 2 Outputs Report") ~ "Quarter 2",
    str_detect(stage,"Quarter 3 Outputs Report") ~ "Quarter 3",
    str_detect(stage,"Quarter 4 Outputs Report") ~ "Quarter 4",
    str_detect(stage,"Semester 1 Outputs Report") ~ "Semester 1",
    str_detect(stage,"Semester 2 Outputs Report") ~ "Semester 2",
    str_detect(stage,"^Annual.*") ~ "Annual",
    str_detect(stage,"^Adjustment.*") ~ "Adjustment",
    str_detect(stage,"2018/2019 - 3M Outputs Report 04") ~ "Quarter 4",
    TRUE ~ "Other")
}

non_core_report <- function(Data) {
  Data <- Data %>% mutate(across(ends_with("date"),
                               as.Date,origin = "1899-12-30"))
 # add funding status - as a filter column used to remove these values in reporting
  Not_RLP <-'RLP-MU17-P5'
  Data <- Data %>% 
    mutate(funding_status=if_else(grant_id %in% Not_RLP,"Not Funded","Funded"),
           report_from_date= as.Date(report_from_date,origin = "1899-12-30"),
           report_to_date= as.Date(report_to_date,origin = "1899-12-30"),
           report_classification = whats_my_classification(stage),
           report_duration = whats_my_duration(
             stage,as.Date(report_from_date,origin = "1899-12-30"), 
             as.Date(report_to_date,origin = "1899-12-30")),
           report_interval = 
             whats_my_interval(
               stage,
               as.Date(report_from_date,origin = "1899-12-30"), 
               as.Date(report_to_date,origin = "1899-12-30")),
           year_qtr_start = quarter(report_from_date, with_year = TRUE, 
                                    fiscal_start=7),
           year_qtr_end = quarter(report_to_date, with_year = TRUE, 
                                  fiscal_start=7),
           extract_date=extract_date,
           qtr_start = round((year_qtr_start - floor(year_qtr_start))*10,0),
           qtr_end = round((year_qtr_end - floor(year_qtr_end))*10,0),
           report_category="Non Core",
           MERIT_Reports_link = 
             str_c("https://fieldcapture.ala.org.au/project/index/",
                   project_id)) %>%
    left_join(management_units,by="management_unit") %>%
    select(grant_id,mu_id,mu_state,management_unit,status,end_date,sub_program,
           name,funding_status, report_category, 
           activity_or_report_id=activity_id,stage,description=description_2,
           report_financial_year, qtr_start,qtr_end,report_from_date, 
           report_to_date,report_classification,report_duration, 
           report_interval, report_status, MERIT_Reports_link,extract_date,
           modified_date=last_modified_2) 
 return(Data) 
}

core_report <- function(Data,report_class,report_freq,report_int) {
  
  # look for "^Core services annual report.*" in Description column for Core Annual reports.
  # look for "^Core services report.*" in Description column for Core Month reports.
  test_core_report <- c('Test Program')
  Data_Out <- Data %>% 
    mutate(
      end_date=report_date,
      across(ends_with("_date"),as.Date,origin = "1899-12-30"),
      report_from_date= as.Date(from_date,origin = "1899-12-30"),
      report_to_date= as.Date(to_date,origin = "1899-12-30"),
      year_qtr_start = quarter(report_from_date, with_year = TRUE, fiscal_start=7),
      year_qtr_end = quarter(report_to_date, with_year = TRUE, fiscal_start=7),
      report_financial_year = financial_year,
      qtr_start = round((year_qtr_start - floor(year_qtr_start))*10,0),
      qtr_end = round((year_qtr_end - floor(year_qtr_end))*10,0),
      report_classification=report_class,
      report_frequency=report_freq,
      report_interval=report_int,
      current_report_status = case_when (
        is.na(current_report_status) ~ "Unpublished (no action - never been submitted)",
        current_report_status=='submitted' ~ 'Submitted',
        current_report_status=='returned' ~ 'Returned',
        TRUE ~ as.character(current_report_status)),
      report_category="Core",
      extract_date=extract_date,
      grant_id="n/a",
      stage="n/a",
      name="n/a",
      sub_program='Regional Land Partnerships',
      status='na',
      funding_status=if_else(management_unit_name %in% test_core_report,
                             "Not Funded","Funded"),
      MERIT_Reports_link='https://fieldcapture.ala.org.au/') %>%
    left_join(management_units,by=c("management_unit_name"="management_unit")) %>%
    mutate(current_report_status = case_when(current_report_status=="approved"
                                             ~"Approved",
                                             TRUE ~ current_report_status)) %>%
    select(grant_id,mu_id,mu_state,management_unit=management_unit_name,
           status,end_date,sub_program, name, funding_status, report_category,
           activity_or_report_id=report_id,stage,description=report_description,
           report_financial_year, qtr_start,qtr_end, report_from_date, 
           report_to_date, report_classification,report_frequency,
           report_interval, report_status=current_report_status, 
           MERIT_Reports_link,extract_date,modified_date=date_of_status_change)
}

core_reports_mu_reference_data <- function(fy) {
  mu_s <- ifelse(fy=='2018/2019',52,54)
  data.frame(grant_id='n/a',
             mu_id=management_units[1:mu_s,'mu_id'],
             mu_state=management_units[1:mu_s,'mu_state'],
             management_unit=management_units[1:mu_s,'management_unit'],
             end_date=report_date,
             status='n/a',
             sub_program='Regional Land Partnerships',
             name='n/a',
             funding_status='funded',
             report_category='Core',
             activity_or_report_id=
               paste(management_units[1:mu_s,'management_unit'],fy),
             stage='n/a',
             description=paste('Core services annual report for ',
                               management_units[1:mu_s,'management_unit']),
             report_financial_year=fy,
             qtr_start=1,
             qtr_end=1,
             report_from_date=as.Date(paste(str_sub(fy,1,4),'-07-01',sep='')),
             report_to_date=as.Date(paste(str_sub(fy,6,9),'-07-01',sep='')),
             report_classification='Core Annual',
             report_frequency='Annual',
             report_interval='Annual',
             report_status='Unpublished (no action - never been submitted)',
             MERIT_Reports_link='n/a',
             extract_date=extract_date)}

bind_all <- function(...) {
  test <- bind_rows(rbind(list(...)))
}
# activity reports
M01_Activity_Summary <- openxlsx::read.xlsx(paste('M01 ',
                       extract_date,
                       '.xlsx', sep=''),
                 sheet="Activity Summary") %>%
  clean_names() %>%
  filter(sub_program %in% c('Regional Land Partnerships',
                            'Direct source procurement',
                            'Pest Mitigation and Habitat Protection',
                            'Strategic and Multi-regional projects - NRM'))

non_core <- M01_Activity_Summary  %>%
  non_core_report() #%>%
  # mutate(report_status = if_else(
  #   due_date > report_to_date & 
  #     report_status=='Unpublished (no action - never been submitted)',
  #   'Not Submitted (over due)',report_status))
# core reports

M12_core_month_reports <- openxlsx::read.xlsx(paste('M12 ',
                                      extract_date,
                                      '.xlsx', sep=''),
                                sheet="RLP Core Services report",
                                startRow = 3) %>% 
  clean_names() %>%
  distinct()

core_month_reports <- M12_core_month_reports %>%
  core_report("Core Month","Various Month","Month")

core_annual_reports_reference <- bind_rows(
  core_reports_mu_reference_data('2018/2019'),
  core_reports_mu_reference_data('2019/2020'),
  core_reports_mu_reference_data('2020/2021')) 

M12_core_annual_reports <- openxlsx::read.xlsx(paste('M12 ',
                                       extract_date,
                                       '.xlsx', sep=''),
                                 sheet="RLP Core Services annual report",
                                 startRow = 3) %>% 
  clean_names() %>%
  distinct()

core_annual_reports <-  M12_core_annual_reports %>%
  core_report("Core Annual","Annual","Annual") %>%
  bind_rows(core_annual_reports_reference) %>%
  group_by(management_unit,report_financial_year) %>%
  filter(row_number()==1) %>%
  filter(!is.na(management_unit))

# bind all reports
report_data <- bind_all(non_core, core_month_reports, core_annual_reports)  %>%
  mutate(modified_date=as.Date(modified_date,origin='1899-12-30'),
         modified_month_name=month(modified_date,label=TRUE),
         modified_month_no_in_fy = (month(modified_date) - 7) %% 12 + 1,
         report_date=report_date,
         report_date_qtr=report_date_qtr,
         report_date_yr_qtr=report_date_yr_qtr,
         due_date=due_date,
         approved_prev_qtr=if_else(report_status=='Approved' & 
                                     prev_qtr_date<modified_date,1,0),
         returned_prev_qtr=if_else(report_status=='Returned' & 
                                     prev_qtr_date<modified_date,1,0),
         submitted_prev_qtr=if_else(report_status=='Submitted' & 
                                      prev_qtr_date<modified_date,1,0)) 
# reports are over due when beyond the due date
report_data <- report_data %>% 
  mutate(
    report_status = if_else(
      report_status==
        'Unpublished (no action – never been submitted)' &
        due_date > report_to_date , "Not Submitted (over due)",
      report_status))

# em dashes are really annoying
report_data <- report_data %>% 
  mutate(report_status=if_else(
    str_detect(report_status,'Unpublished'),
    'Unpublished (No action - Never been submitted)',
    report_status))

# find the report types
project_report_profile_frequnecy <- report_data %>%
  filter(report_category=='Non Core',status=='Active') %>%
  select(grant_id,report_frequency) %>%
  group_by(grant_id)  %>%
  mutate(report = report_frequency) %>% 
  distinct() %>%
  ungroup() %>%
  select(-report_frequency) %>%
  group_by(grant_id) %>%
  summarize(report_frequencies=str_c(report,collapse = "|")) %>%
  ungroup()
  
stage_name_profile <- report_data %>% 
  select(sub_program,stage,report_from_date,report_to_date) %>% 
  group_by(sub_program) %>% 
  mutate(new_stage=str_replace_all(stage,"[\\s/]?\\d{4}"," YYYY"),
         new_stage=str_replace(new_stage,"[\\s/]\\d{2}\\D"," yy"),
         new_stage=str_replace(new_stage,"[\\s/]\\d{1}\\D?"," n "),
         dur=interval(report_from_date,report_to_date) %/% months(1)) %>%
  ungroup() %>%
  select(sub_program,new_stage,dur) %>%
  group_by(sub_program,new_stage) %>%
  summarize(dur=max(dur))

project_months_to_go <- report_data %>%
  mutate(months_to_go = interval(current_qtr_start_date,end_date) %/% 
           months(1)) %>% 
  select(grant_id,months_to_go) %>%
  distinct()

report_data <- report_data %>%
  left_join(project_report_profile_frequnecy,on='grant_id') %>%
  left_join(project_report_profile_classification,on='grant_id') %>%
  left_join(project_months_to_go,on='granti_id')
    
# openxlsx::write.xlsx(report_data,'all reports.xslx',overwrite = TRUE)
report_data %>%
   write.csv(paste('all reports.',extract_date,'.csv'),row.names=FALSE) 

# interval_counts <- report_data %>%
#   group_by(report_financial_year,report_category, report_classification,
#         report_frequency, report_interval, report_status) %>%
#   summarize(n=n(),
#             across(ends_with("_prev_qtr"),sum))
# 
# sub_program_interval_counts <- report_data %>%
#   group_by(management_unit,sub_program,report_financial_year,report_category, report_classification,
#            report_frequency, report_interval, report_status) %>%
#   summarize(n=n())
# 
# total_counts <- report_data %>%
#   group_by(report_category, report_classification, report_frequency) %>%
#   summarize(n=n(),across(ends_with("_prev_qtr"),sum))
# 
# prev_qtr_totals_mu_sp_fy_rc_rf_ri <- report_data %>%
#   group_by(management_unit,sub_program,report_financial_year,
#            report_category,report_frequency,report_interval) %>%
#   summarize(across(ends_with("_prev_qtr"),sum))
# 
# prev_qtr_totals_sp_fy_rc_rf_ri <- report_data %>%
#   group_by(sub_program,report_financial_year,
#            report_category,report_frequency,report_interval) %>%
#   summarize(across(ends_with("_prev_qtr"),sum))
# prev_qtr_totals_sp_fy_rc_rf <- report_data %>%
#   group_by(sub_program,report_financial_year,
#            report_category,report_frequency) %>%
#   summarize(across(ends_with("_prev_qtr"),sum))
# 
# prev_qtr_totals_fy_rc_rf <- report_data %>%
#   group_by(report_financial_year,
#            report_category,report_frequency) %>%
#   summarize(across(ends_with("_prev_qtr"),sum))
# 
# frequency_pivot<- interval_counts %>%
#   pivot_wider(id_cols=c(report_financial_year,report_category,report_frequency),
#               names_from=report_status, values_from=c(n), values_fn=sum) %>%
#   mutate(num_year = as.numeric(str_sub(report_financial_year,1,4)))
# 
# sub_program_frequency_pivot<- sub_program_interval_counts %>%
#   pivot_wider(id_cols=c(sub_program,report_financial_year,report_category,report_frequency,report_frequency),
#               names_from=report_status, values_from=c(n), values_fn=sum) %>%
#   mutate(num_year = as.numeric(str_sub(report_financial_year,1,4)))
# 
# sub_program_frequency_interval_pivot<- sub_program_interval_counts  %>%
#   pivot_wider(id_cols=c(sub_program,report_financial_year,report_category,
#                         report_frequency,report_interval,report_frequency),
#               names_from=report_status, values_from=c(n), values_fn=sum) %>%
#   mutate(num_year = as.numeric(str_sub(report_financial_year,1,4)))
# 
# management_unit_frequency_interval_pivot<- sub_program_interval_counts  %>%
#   pivot_wider(id_cols=c(management_unit,sub_program,report_financial_year,report_category,
#                         report_frequency,report_interval,report_frequency),
#               names_from=report_status, values_from=c(n), values_fn=sum) %>%
#   mutate(num_year = as.numeric(str_sub(report_financial_year,1,4)))
# 
# if (sum(sub_program_interval_counts$report_status=="Not Submitted (over due)")>0) {
# 
#   frequency_pivot<-  frequency_pivot %>%
#     select(report_financial_year,num_year,report_category,report_frequency,
#            Submitted_but_not_Approved= Submitted,
#            Submitted_and_approved = Approved,
#            Returned_to_provider = Returned,
#            Not_Submitted = "Not Submitted (over due)",ends_with("_prev_qtr"))
# 
#   sub_program_frequency_pivot<-  sub_program_frequency_pivot %>%
#   select(sub_program,report_financial_year,num_year,report_category,report_frequency,
#          Submitted_but_not_Approved= Submitted,
#          Submitted_and_approved = Approved,
#          Returned_to_provider = Returned,
#          Not_Submitted = "Not Submitted (over due)")
# 
#   sub_program_frequency_interval_pivot<- sub_program_frequency_interval_pivot  %>%
#     select(sub_program,report_financial_year,num_year,
#            report_category,report_frequency,report_interval,
#            Submitted_but_not_Approved= Submitted,
#            Submitted_and_approved = Approved,
#            Returned_to_provider = Returned,
#            Not_Submitted = "Not Submitted (over due)")
# 
#   management_unit_frequency_interval_pivot<- management_unit_frequency_interval_pivot  %>%
#     select(management_unit,sub_program,report_financial_year,num_year,
#            report_category,report_frequency,report_interval,
#            Submitted_but_not_Approved= Submitted,
#            Submitted_and_approved = Approved,
#            Returned_to_provider = Returned,
#            Not_Submitted = "Not Submitted (over due)")
# } else {
#   # No reports have have Not_Submiited Report_Status
#   frequency_pivot<- frequency_pivot %>%
#     mutate(Not_Submitted=0) %>%
#     select(report_financial_year,num_year,report_category,report_frequency,
#            Submitted_but_not_Approved= Submitted,
#            Submitted_and_approved = Approved,
#            Returned_to_provider = Returned,
#            Not_Submitted,ends_with("_prev_qtr"))
# 
#   sub_program_frequency_pivot<- sub_program_frequency_pivot %>%
#     mutate(Not_Submitted=0) %>%
#     select(sub_program,report_financial_year,num_year,report_category,report_frequency,
#            Submitted_but_not_Approved= Submitted,
#            Submitted_and_approved = Approved,
#            Returned_to_provider = Returned,
#            Not_Submitted)
# 
#   sub_program_frequency_interval_pivot <- sub_program_frequency_interval_pivot  %>%
#     mutate(Not_Submitted=0) %>%
#     select(sub_program,report_financial_year,num_year,report_category,report_frequency,
#            report_interval, Submitted_but_not_Approved= Submitted,
#            Submitted_and_approved = Approved,
#            Returned_to_provider = Returned,
#            Not_Submitted)
# 
#   management_unit_frequency_interval_pivot <- management_unit_frequency_interval_pivot  %>%
#     mutate(Not_Submitted=0) %>%
#     select(management_unit,sub_program,report_financial_year,num_year,report_category,report_frequency,
#            report_interval, Submitted_but_not_Approved= Submitted,
#            Submitted_and_approved = Approved,
#            Returned_to_provider = Returned,
#            Not_Submitted)
# }
# 
# sub_program_frequency_interval_pivot <- sub_program_frequency_interval_pivot %>%
#   mutate_at(c("Submitted_but_not_Approved","Submitted_and_approved",
#               "Returned_to_provider","Not_Submitted"), ~replace(., is.na(.), 0)) %>%
#   mutate(Total = Submitted_but_not_Approved + Submitted_and_approved +
#            Returned_to_provider+Not_Submitted,
#          Approved_MERIT = str_c(Submitted_and_approved,Total,sep="/"),
#          Received_MERIT = str_c(Submitted_and_approved+Submitted_but_not_Approved,Total,sep="/")) %>%
#   arrange(sub_program,desc(num_year),report_category) %>%
#   filter(num_year %in% (2018:2021)) %>%
#   select(sub_program,report_financial_year,
#          report_category, report_frequency, report_interval,-num_year,everything()) %>%
#   left_join(prev_qtr_totals_sp_fy_rc_rf_ri,by=c('sub_program','report_financial_year',
#                                        'report_category','report_frequency','report_interval') )%>%
#   select(-num_year)
# 
# management_unit_frequency_interval_pivot <- management_unit_frequency_interval_pivot %>%
#   mutate_at(c("Submitted_but_not_Approved","Submitted_and_approved",
#               "Returned_to_provider","Not_Submitted"), ~replace(., is.na(.), 0)) %>%
#   mutate(Total = Submitted_but_not_Approved + Submitted_and_approved +
#            Returned_to_provider+Not_Submitted,
#          Approved_MERIT = str_c(Submitted_and_approved,Total,sep="/"),
#          Received_MERIT = str_c(Submitted_and_approved+Submitted_but_not_Approved,Total,sep="/")) %>%
#   arrange(management_unit,sub_program,desc(num_year),report_category) %>%
#   filter(num_year %in% (2018:2021)) %>%
#   select(management_unit,sub_program,report_financial_year,
#          report_category, report_frequency, report_interval,-num_year,everything()) %>%
#   left_join(prev_qtr_totals_mu_sp_fy_rc_rf_ri,by=c('management_unit','sub_program','report_financial_year',
#                                                 'report_category','report_frequency','report_interval') ) %>%
#   select(-num_year)
# 
# frequency_pivot<- frequency_pivot %>%
#   mutate_at(c("Submitted_but_not_Approved","Submitted_and_approved",
#               "Returned_to_provider","Not_Submitted"), ~replace(., is.na(.), 0)) %>%
#   mutate(Total = Submitted_but_not_Approved + Submitted_and_approved +
#            Returned_to_provider+Not_Submitted,
#          Approved_MERIT = str_c(Submitted_and_approved,Total,sep="/"),
#          Received_MERIT = str_c(
#            Submitted_and_approved+Submitted_but_not_Approved,Total,sep="/")) %>%
#   arrange(desc(num_year),report_category) %>%
#   filter(num_year %in% (2018:2021)) %>%
#   select(report_financial_year,
#          report_category, report_frequency,ends_with("_prev_qtr"),-
#            num_year,everything()) %>%
#   left_join(prev_qtr_totals_fy_rc_rf,by=c('report_financial_year',
#                                              'report_category','report_frequency')) %>%
#   select(-num_year)
# 
# 
# sub_program_frequency_pivot<- sub_program_frequency_pivot %>%
#   mutate_at(c("Submitted_but_not_Approved","Submitted_and_approved",
#               "Returned_to_provider","Not_Submitted"), ~replace(., is.na(.), 0)) %>%
#   mutate(Total = Submitted_but_not_Approved + Submitted_and_approved +
#            Returned_to_provider+Not_Submitted,
#          Approved_MERIT = str_c(Submitted_and_approved,Total,sep="/"),
#          Received_MERIT = str_c(Submitted_and_approved+Submitted_but_not_Approved,Total,sep="/")) %>%
#   arrange(sub_program,desc(num_year),report_category) %>%
#   filter(num_year %in% (2018:2021)) %>%
#   select(sub_program,report_financial_year,
#          report_category, report_frequency,-num_year,everything()) %>%
#   left_join(prev_qtr_totals_sp_fy_rc_rf,by=c('sub_program','report_financial_year',
#                                                 'report_category','report_frequency')) %>%
#   select(-num_year)

wb <- createWorkbook()

# format for spreadsheet output
headerStyle <- createStyle(
  fontSize = 11,
  fontName = "Arial",
  textDecoration = "bold",
  halign = "left",
  fontColour = "white",
  fgFill = "black",
  border = "TopBottomLeftRight"
)
# addWorksheet(wb=wb,sheetName="Totals")
# writeData(wb=wb,sheet="Totals",
#           total_counts,
#           withFilter=TRUE,
#           headerStyle = headerStyle)
# 
# addWorksheet(wb=wb,sheetName="Sub Program Counts")
# writeData(wb=wb,sheet="Sub Program Counts",
#           sub_program_frequency_pivot,
#           withFilter=TRUE,
#           headerStyle = headerStyle)
# 
# addWorksheet(wb=wb,sheetName="Interval Counts")
# writeData(wb=wb,sheet="Interval Counts",
#           frequency_pivot,
#           withFilter=TRUE,
#           headerStyle = headerStyle)
# 
# addWorksheet(wb=wb,sheetName="Sub Program Interval Counts")
# writeData(wb=wb,sheet="Sub Program Interval Counts",
#           sub_program_frequency_interval_pivot,
#           withFilter=TRUE,
#           headerStyle = headerStyle)
# 
# addWorksheet(wb=wb,sheetName="Management Unit Interval Counts")
# writeData(wb=wb,sheet="Management Unit Interval Counts",
#           management_unit_frequency_interval_pivot,
#           withFilter=TRUE,
#           headerStyle = headerStyle)
# 

# Workaround for old column names
# names(report_data) <- c(
#   'Grant.ID','MU.ID','MU.State','Management.Unit','Sub.program','Name',
#   'Funding.Status','report_category','Activity_or_Report.ID','Stage',
#   'Description','fin_year','qtr_start','qtr_end','date_start','date_end',
#   'report_classification','report_frequency','report_interval',
#   'Report.Status','MERIT_Reports_link','extract_date')
addWorksheet(wb=wb,sheetName="Tablecloth Dataset")
writeData(wb=wb,sheet="Tablecloth Dataset",
          report_data,
          withFilter=TRUE,
          headerStyle = headerStyle)

saveWorkbook(wb=wb,file=paste0("all_reports ",extract_date,".xlsx"),overwrite=TRUE)

report_data %>% 
  filter(report_status=='Approved') %>%
  # group_by(report_financial_year) %>%
  filter(report_financial_year=='2021/2022') %>%
  count(modified_month_name) %>% 
  drop_na() %>% 
  plot()
