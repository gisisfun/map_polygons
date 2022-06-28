

library(openxlsx)
library(tidyr)
library(dplyr)
library(lubridate)
library(stringr)
library(forcats)
require(janitor)
require(rlang)
require(purrr)
require(jsonlite)
library(DBI)
library(RSQLite)
# The R code transforms data in MERIT (NoSQL) to line item (SQL) by project and 
# project report views.

# projects - reports - species view
# A grants view of procurement activity report data with grants activities 
# presented with procurement-like columns (measured,actual and invoiced). 
# Additional report species content related to each project are recorded.
# * Will require mapping of balance of report data items to provide complete
# coverage of availalble data.
#
# projects - species view
# A projects line item view with summarised project assets, investment priorities, 
# report species and MNES categories against investment priority. 
#
# Data Source: The Big Download of MERIT (Spreadsheets)
#
# The rest of the downloads from 2 onwards are a selection of programs and the 
# reports relevant to that program.  So to reproduce these, you would select 
# the same program/sub-programs, then tick all of the boxes below "Activity 
# summary" that appear.  From memory I had to exclude a couple of discontinued 
# forms from biodiversity fund and C4oC as they were causing download issues.
# The program categories I chose are:
#
# 1.	All tabs up to and including the "Activity summary" tab.  No filters 
# applied (so all projects)
# > getSheetNames(paste('M01 ',extract_date,'.xlsx',sep=''))
# [1] "Projects"                     "Output Targets"              
# [3] "Sites"                        "Documents"                   
# [5] "Activity Summary"             "Risks and Threats"           
# [7] "MERI_Budget"                  "MERI_Outcomes"               
# [9] "MERI_Monitoring"              "MERI_Project Partnerships"   
# [11] "MERI_Project Implementation"  "MERI_Key Evaluation Question"
# [13] "MERI_Priorities"              "MERI_WHS and Case Study"     
# [15] "MERI_Baseline"                "MERI_Event"                  
# [17] "MERI_Approvals"               "RLP Outcomes"                
# [19] "RLP Project Details"          "RLP Key Threats"             
# [21] "Project services and targets" "Reports"                     
# [23] "Report Summary"               "Data_set_Summary"            
# [25] "Blog"                         "MERI_Attachments"            
# [27] "MERI_Project Assets"
#
# 2.	Agriculture Stewardship + Future Drought Fund
# > getSheetNames(paste('M02 ',extract_date,'.xlsx',sep=''))
# [1] "RLP - Output WHS ...tput Report" "RLP - Baseline da...tput Report"
# [3] "RLP - Communicati...tput Report" "RLP - Community e...tput Report"
# [5] "RLP - Controlling...tput Report" "RLP - Pest animal...tput Report"
# [7] "RLP - Management ...tput Report" "RLP - Debris remo...tput Report"
# [9] "RLP - Erosion Man...tput Report" "RLP - Maintaining...tput Report"
# [11] "RLP - Establishin...tput Report" "RLP - Establishin...tput Rep(1)"
# [13] "RLP - Establishin...tput Rep(2)" "RLP - Farm Manage...tput Report"
# [15] "RLP - Fauna surve...tput Report" "RLP - Fire manage...tput Report"
# [17] "RLP - Flora surve...tput Report" "RLP - Habitat aug...tput Report"
# [19] "RLP - Identifying...tput Report" "RLP - Improving h...tput Report"
# [21] "RLP - Improving l...tput Report" "RLP - Disease man...tput Report"
# [23] "RLP - Negotiation...tput Report" "RLP - Obtaining a...tput Report"
# [25] "RLP - Pest animal...tput Rep(1)" "RLP - Plant survi...tput Report"
# [27] "RLP - Project pla...tput Report" "RLP - Remediating...tput Report"
# [29] "RLP - Weed treatm...tput Report" "RLP - Revegetatin...tput Report"
# [31] "RLP - Site prepar...tput Report" "RLP - Skills and ...tput Report"
# [33] "RLP - Soil testin...tput Report" "RLP - Emergency I...tput Report"
# [35] "RLP - Water quali...tput Report" "RLP - Weed distri...tput Report"
# [37] "RLP - Change Mana...tput Report" "RLP - Adapting to...tput Report"
# [39] "Seed Collecting -...tput Report" "RLP Annual Report"              
# [41] "RLP Short term project outcomes"
#
# 3.	Biodiversity Fund. 
# > getSheetNames(paste('M03 ',extract_date,'.xlsx',sep=''))
# [1] "Outcomes Outcomes...inal report" "Evaluation Outcom...inal report"
# [3] "Lessons Learned O...inal report" "Administration Ac...inistration"
# [5] "Participant Infor...inistration" "Overview of Proje...tage report"
# [7] "Environmental, Ec...tage report" "Implementation Up...tage report"
# [9] "Lessons Learned a...tage report" "Survey Informatio...y - general"
# [11] "Flora Survey Deta...y - general" "Participant Infor...y - general"
# [13] "Sampling Site Inf...methodology" "Field Sheet 1 - G...methodology"
# [15] "Field Sheet 2 - E...methodology" "Field Sheet 3 - O...methodology"
# [17] "Field Sheet 4 - C...methodology" "Field Sheet 5 - S...methodology"
# [19] "Event Details Com... Engagement" "Participant Infor... Engagement"
# [21] "Materials Provide... Engagement" "Fence Details Fencing"          
# [23] "Participant Information Fencing" "Pest Management D... Management"
# [25] "Fence Details Pest Management"   "Participant Infor... Management"
# [27] "Revegetation Deta...evegetation" "Participant Infor...evegetation"
# [29] "Weed Treatment De...d Treatment" "Participant Infor...d Treatment"
# [31] "Site Planning Det...ng and Risk" "Threatening Proce...ng and Risk"
# [33] "Participant Infor...ng and Risk" "Upload of stage 1...orting data"
# [35] "Seed Collection D... Collection" "Participant Infor... Collection"
# [37] "Site Preparation ...Preparation" "Weed Treatment De...Preparation"
# [39] "Participant Infor...Preparation" "Training Details ...Development"
# [41] "Skills Developmen...Development" "Participant Infor...Development"
# [43] "Fire Management D... Management" "Participant Infor... Managem(1)"
# [45] "Water Management"                "Survey Informatio...y - gene(1)"
# [47] "Fauna Survey Deta...y - general" "Participant Infor...y - gene(1)"
# [49] "Evidence of Pest ...imal Survey" "Pest Observation ...imal Survey"
# [51] "Participant Infor...imal Survey" "Evidence of Weed ... Monitoring"
# [53] "Weed Observation ... Monitoring" "Participant Infor... Monitoring"
# [55] "Debris Removal De...ris Removal" "Participant Infor...ris Removal"
# [57] "Conservation Work...Communities" "Participant Infor...Communities"
# [59] "Vegetation Monito...ival Survey" "Participant Infor...ival Survey"
# [61] "Plant Propagation...Propagation" "Participant Infor...Propagation"
# [63] "Plan Development ...Development" "Participant Infor...Developm(1)"
# [65] "Research Information Research"   "Participant Infor...on Research"
# [67] "Access Control De...rastructure" "Infrastructure De...rastructure"
# [69] "Participant Infor...rastructure" "Indigenous Knowledge Transfer"  
# [71] "Heritage Conserva...onservation" "Expected Heritage...onservation"
# [73] "Participant Infor...onservation" "Site Monitoring Plan"           
# [75] "General informati...lity Survey" "Environmental Inf...lity Survey"
# [77] "Water Quality Mea...lity Survey" "Conservation Grazing Management"
# [79] "Management Practice Change"      "Erosion Managemen... Management"
# [81] "Participant Infor... Managem(2)" "Indigenous Employ... Businesses"
# [83] "Indigenous Busine... Businesses" "Participant Infor... assessment"
# [85] "Vegetation Assess... assessment" "Site Condition Co... assessment"
# [87] "Landscape Context... assessment" "Threatening Proce... assessment"
# [89] "Biodiversity Fund... Monitoring" "Asset Protection ... Management"
# [91] "Ecological Burn D... Management" "Participant Infor... Managem(3)"
# [93] "Disease Managemen... Management" "Participant Infor... Managem(4)"
#
# 4.	Caring for our country 2
# > getSheetNames(paste('M04 ',extract_date,'.xlsx',sep=''))
# [1] "Outcomes Outcomes...inal report" "Evaluation Outcom...inal report"
# [3] "Lessons Learned O...inal report" "Administration Ac...inistration"
# [5] "Participant Infor...inistration" "Overview of Proje...tage report"
# [7] "Environmental, Ec...tage report" "Implementation Up...tage report"
# [9] "Lessons Learned a...tage report" "Event Details Com... Engagement"
# [11] "Participant Infor... Engagement" "Materials Provide... Engagement"
# [13] "Management Practice Change"      "Site Planning Det...ng and Risk"
# [15] "Threatening Proce...ng and Risk" "Participant Infor...ng and Risk"
# [17] "Training Details ...Development" "Skills Developmen...Development"
# [19] "Participant Infor...Development" "Plan Development ...Development"
# [21] "Participant Infor...Developm(1)" "Survey Informatio...y - general"
# [23] "Flora Survey Deta...y - general" "Participant Infor...y - general"
# [25] "Conservation Work...Communities" "Participant Infor...Communities"
# [27] "Pest Management D... Management" "Fence Details Pest Management"  
# [29] "Participant Infor... Management" "Research Information Research"  
# [31] "Participant Infor...on Research" "Weed Treatment De...d Treatment"
# [33] "Participant Infor...d Treatment" "Indigenous Knowledge Transfer"  
# [35] "Site Monitoring Plan"            "Survey Informatio...y - gene(1)"
# [37] "Fauna Survey Deta...y - general" "Participant Infor...y - gene(1)"
# [39] "Evidence of Weed ... Monitoring" "Weed Observation ... Monitoring"
# [41] "Participant Infor... Monitoring" "Fence Details Fencing"          
# [43] "Participant Information Fencing" "Conservation Grazing Management"
# [45] "Fire Management D... Management" "Participant Infor... Managem(1)"
# [47] "Access Control De...rastructure" "Infrastructure De...rastructure"
# [49] "Participant Infor...rastructure" "Evidence of Pest ...imal Survey"
# [51] "Pest Observation ...imal Survey" "Participant Infor...imal Survey"
# [53] "Vegetation Monito...ival Survey" "Participant Infor...ival Survey"
# [55] "Erosion Managemen... Management" "Participant Infor... Managem(2)"
# [57] "Revegetation Deta...evegetation" "Participant Infor...evegetation"
# [59] "Seed Collection D... Collection" "Participant Infor... Collection"
# [61] "Indigenous Employ... Businesses" "Indigenous Busine... Businesses"
# [63] "Water Management"                "Site Preparation ...Preparation"
# [65] "Weed Treatment De...Preparation" "Participant Infor...Preparation"
# [67] "Sampling Site Inf...methodology" "Field Sheet 1 - G...methodology"
# [69] "Field Sheet 2 - E...methodology" "Field Sheet 3 - O...methodology"
# [71] "Field Sheet 4 - C...methodology" "Field Sheet 5 - S...methodology"
# [73] "General informati...lity Survey" "Environmental Inf...lity Survey"
# [75] "Water Quality Mea...lity Survey" "Debris Removal De...ris Removal"
# [77] "Participant Infor...ris Removal" "Plant Propagation...Propagation"
# [79] "Participant Infor...Propagation" "Feral Animal Abun... assessment"
# [81] "Feral Animal Freq... assessment" "Heritage Conserva...onservation"
# [83] "Expected Heritage...onservation" "Participant Infor...onservation"
# [85] "Participant Infor... assessment" "Vegetation Assess... assessment"
# [87] "Site Condition Co... assessment" "Landscape Context... assessment"
# [89] "Threatening Proce... assessment" "Annual Stage Report"            
# [91] "Post revegetation... management" "Post revegetation... managem(1)"
# [93] "Post revegetation... managem(2)" "Post revegetation... managem(3)"
# [95] "Disease Managemen... Management" "Participant Infor... Managem(3)"
# [97] "1. Community Gran...nity Grants" "2. Community Gran...nity Grants"
# [99] "Attachments Community Grants" 
#
# 5.	Bushfire+Recovery+for+Species+and+Landscapes+Program, 
#     Bushfire+Wildlife+and+Habitat+Recovery
# > getSheetNames(paste('M05 ',extract_date,'.xlsx',sep=''))
# [1] "State Government ...ress Report" "Baseline data Sta...ress Report"
# [3] "Communication mat...ress Report" "Community engagem...ress Report"
# [5] "Controlling acces...ress Report" "Pest animal manag...ress Report"
# [7] "Management plan d...ress Report" "Debris removal St...ress Report"
# [9] "Erosion Managemen...ress Report" "Maintaining feral...ress Report"
# [11] "Establishing ex-s...ress Report" "Establishing Agre...ress Report"
# [13] "Establishing moni...ress Report" "Farm Management S...ress Report"
# [15] "Fauna survey Stat...ress Report" "Fire management S...ress Report"
# [17] "Flora survey Stat...ress Report" "Habitat augmentat...ress Report"
# [19] "Identifying sites...ress Report" "Improving hydrolo...ress Report"
# [21] "Improving land ma...ress Report" "Disease managemen...ress Report"
# [23] "Negotiations Stat...ress Report" "Obtaining approva...ress Report"
# [25] "Pest animal surve...ress Report" "Plant survival su...ress Report"
# [27] "Project planning ...ress Report" "Remediating ripar...ress Report"
# [29] "Revegetating habi...ress Report" "Weed treatment St...ress Report"
# [31] "Seed Collecting -...ress Report" "Site preparation ...ress Report"
# [33] "Skills and knowle...ress Report" "Soil testing Stat...ress Report"
# [35] "Supplementary foo...ress Report" "Emergency Interve...ress Report"
# [37] "Water quality sur...ress Report" "Weed distribution...ress Report"
# [39] "State Government ...inal Report" "Baseline data Sta...inal Report"
# [41] "Communication mat...inal Report" "Community engagem...inal Report"
# [43] "Controlling acces...inal Report" "Pest animal manag...inal Report"
# [45] "Management plan d...inal Report" "Debris removal St...inal Report"
# [47] "Erosion Managemen...inal Report" "Maintaining feral...inal Report"
# [49] "Establishing ex-s...inal Report" "Establishing Agre...inal Report"
# [51] "Establishing moni...inal Report" "Farm Management S...inal Report"
# [53] "Fauna survey Stat...inal Report" "Fire management S...inal Report"
# [55] "Flora survey Stat...inal Report" "Habitat augmentat...inal Report"
# [57] "Identifying sites...inal Report" "Improving hydrolo...inal Report"
# [59] "Improving land ma...inal Report" "Disease managemen...inal Report"
# [61] "Negotiations Stat...inal Report" "Obtaining approva...inal Report"
# [63] "Pest animal surve...inal Report" "Plant survival su...inal Report"
# [65] "Project planning ...inal Report" "Remediating ripar...inal Report"
# [67] "Revegetating habi...inal Report" "Weed treatment St...inal Report"
# [69] "Seed Collecting -...inal Report" "Site preparation ...inal Report"
# [71] "Skills and knowle...inal Report" "Soil testing Stat...inal Report"
# [73] "Supplementary foo...inal Report" "Emergency Interve...inal Report"
# [75] "Water quality sur...inal Report" "Weed distribution...inal Report"
# [77] "State Interventio...inal Report" "Wildlife Recovery...eport - WRR"
# [79] "Native wildlife r...eport - WRR" "Supplementary foo...eport - WRR"
# [81] "Emergency interve...eport - WRR" "Wildlife rescue c...eport - WRR"
# [83] "Wildlife rescue e...eport - WRR" "Wildlife rescue f...eport - WRR"
# [85] "Training and deve...eport - WRR" "Administration Wi...eport - WRR"
# [87] "Wildlife Recovery...eport - (1)" "Native wildlife r...eport - (1)"
# [89] "Supplementary foo...eport - (1)" "Emergency interve...eport - (1)"
# [91] "Wildlife rescue c...eport - (1)" "Wildlife rescue e...eport - (1)"
# [93] "Wildlife rescue f...eport - (1)" "Training and deve...eport - (1)"
# [95] "Administration Wi...eport - (1)" "WRR Final Report ...eport - WRR"
# [97] "RLP Short term project outcomes" "Bushfires States ...ress Report"
# [99] "Baseline data Bus...ress Report" "Communication mat...ress Rep(1)"
# [101] "Community engagem...ress Rep(1)" "Controlling acces...ress Rep(1)"
# [103] "Pest animal manag...ress Rep(1)" "Management plan d...ress Rep(1)"
# [105] "Debris removal Bu...ress Report" "Erosion Managemen...ress Rep(1)"
# [107] "Maintaining feral...ress Rep(1)" "Establishing ex-s...ress Rep(1)"
# [109] "Establishing Agre...ress Rep(1)" "Establishing moni...ress Rep(1)"
# [111] "Farm Management S...ress Rep(1)" "Fauna survey Bush...ress Report"
# [113] "Fire management B...ress Report" "Flora survey Bush...ress Report"
# [115] "Habitat augmentat...ress Rep(1)" "Identifying sites...ress Rep(1)"
# [117] "Improving hydrolo...ress Rep(1)" "Improving land ma...ress Rep(1)"
# [119] "Disease managemen...ress Rep(1)" "Negotiations Bush...ress Report"
# [121] "Obtaining approva...ress Rep(1)" "Pest animal surve...ress Rep(1)"
# [123] "Plant survival su...ress Rep(1)" "Project planning ...ress Rep(1)"
# [125] "Remediating ripar...ress Rep(1)" "Revegetating habi...ress Rep(1)"
# [127] "Weed treatment Bu...ress Report" "Seed Collecting -...ress Rep(1)"
# [129] "Site preparation ...ress Rep(1)" "Skills and knowle...ress Rep(1)"
# [131] "Soil testing Bush...ress Report" "Supplementary foo...ress Rep(1)"
# [133] "Emergency Interve...ress Rep(1)" "Water quality sur...ress Rep(1)"
# [135] "Weed distribution...ress Rep(1)" "Cultural value su...ress Report"
# [137] "Cultural Site Man...ress Report" "On Country Visits...ress Report"
# [139] "Cultural Practice...ress Report" "Developing-updati...ress Report"
# [141] "RLP - Output WHS ...tput Report" "RLP - Baseline da...tput Report"
# [143] "RLP - Communicati...tput Report" "RLP - Community e...tput Report"
# [145] "RLP - Controlling...tput Report" "RLP - Pest animal...tput Report"
# [147] "RLP - Management ...tput Report" "RLP - Debris remo...tput Report"
# [149] "RLP - Erosion Man...tput Report" "RLP - Maintaining...tput Report"
# [151] "RLP - Establishin...tput Report" "RLP - Establishin...tput Rep(1)"
# [153] "RLP - Establishin...tput Rep(2)" "RLP - Farm Manage...tput Report"
# [155] "RLP - Fauna surve...tput Report" "RLP - Fire manage...tput Report"
# [157] "RLP - Flora surve...tput Report" "RLP - Habitat aug...tput Report"
# [159] "RLP - Identifying...tput Report" "RLP - Improving h...tput Report"
# [161] "RLP - Improving l...tput Report" "RLP - Disease man...tput Report"
# [163] "RLP - Negotiation...tput Report" "RLP - Obtaining a...tput Report"
# [165] "RLP - Pest animal...tput Rep(1)" "RLP - Plant survi...tput Report"
# [167] "RLP - Project pla...tput Report" "RLP - Remediating...tput Report"
# [169] "RLP - Weed treatm...tput Report" "RLP - Revegetatin...tput Report"
# [171] "RLP - Site prepar...tput Report" "RLP - Skills and ...tput Report"
# [173] "RLP - Soil testin...tput Report" "RLP - Emergency I...tput Report"
# [175] "RLP - Water quali...tput Report" "RLP - Weed distri...tput Report"
# [177] "RLP - Change Mana...tput Report" "RLP - Adapting to...tput Report"
# [179] "Seed Collecting -...tput Report" "RLP Annual Report"              
# [181] "Wildlife Recovery...Report - GA" "Native seed suppl...Report - GA"
# [183] "Native Seed Capac...Report - GA" "Ten Year Native S...Report - GA"
# [185] "Investigating Flo...Report - GA" "Supporting seed b...Report - GA"
# [187] "Developing traini...Report - GA" "Fire-ground safet...Report - GA"
# [189] "Governance arrang...Report - GA" "Final Period Prog...l Reporting"
# [191] "Flora Survey GA Final Reporting" "Seed Collecting G...l Reporting"
# [193] "Final Project Rep...l Reporting" "Wildlife Recovery...eport - CVA"
# [195] "Developing a cent...eport - CVA" "Developing a cent...eport - (1)"
# [197] "Volunteer Work He...eport - CVA"
#
# 6.	Green Army
# > getSheetNames(paste('M06 ',extract_date,'.xlsx',sep=''))
# [1] "Evidence of Weed ... Monitoring" "Weed Observation ... Monitoring"
# [3] "Participant Infor... Monitoring" "Event Details Com... Engagement"
# [5] "Participant Infor... Engagement" "Materials Provide... Engagement"
# [7] "Debris Removal De...ris Removal" "Participant Infor...ris Removal"
# [9] "Plant Propagation...Propagation" "Participant Infor...Propagation"
# [11] "Revegetation Deta...evegetation" "Participant Infor...evegetation"
# [13] "Weed Treatment De...d Treatment" "Participant Infor...d Treatment"
# [15] "Erosion Managemen... Management" "Participant Infor... Management"
# [17] "Survey Informatio...y - general" "Fauna Survey Deta...y - general"
# [19] "Participant Infor...y - general" "Survey Informatio...y - gene(1)"
# [21] "Flora Survey Deta...y - general" "Participant Infor...y - gene(1)"
# [23] "Evidence of Pest ...imal Survey" "Pest Observation ...imal Survey"
# [25] "Participant Infor...imal Survey" "General informati...lity Survey"
# [27] "Environmental Inf...lity Survey" "Water Quality Mea...lity Survey"
# [29] "Sampling Site Inf...methodology" "Field Sheet 1 - G...methodology"
# [31] "Field Sheet 2 - E...methodology" "Field Sheet 3 - O...methodology"
# [33] "Field Sheet 4 - C...methodology" "Field Sheet 5 - S...methodology"
# [35] "Access Control De...rastructure" "Infrastructure De...rastructure"
# [37] "Participant Infor...rastructure" "Seed Collection D... Collection"
# [39] "Participant Infor... Collection" "Site Preparation ...Preparation"
# [41] "Weed Treatment De...Preparation" "Participant Infor...Preparation"
# [43] "Fence Details Fencing"           "Participant Information Fencing"
# [45] "Fire Management D... Management" "Participant Infor... Managem(1)"
# [47] "Pest Management D... Management" "Fence Details Pest Management"  
# [49] "Participant Infor... Managem(2)" "Site Planning Det...ng and Risk"
# [51] "Threatening Proce...ng and Risk" "Participant Infor...ng and Risk"
# [53] "Disease Managemen... Management" "Participant Infor... Managem(3)"
# [55] "Heritage Conserva...onservation" "Expected Heritage...onservation"
# [57] "Participant Infor...onservation" "Indigenous Knowledge Transfer"  
# [59] "Conservation Work...Communities" "Participant Infor...Communities"
# [61] "Site Monitoring Plan"            "Research Information Research"  
# [63] "Participant Infor...on Research" "Training Details ...Development"
# [65] "Skills Developmen...Development" "Participant Infor...Development"
# [67] "Regional Funding Final Report"   "Administration Ac...inistration"
# [69] "Participant Infor...inistration" "Annual Stage Report"            
# [71] "Vegetation Monito...ival Survey" "Participant Infor...ival Survey"
# [73] "Final Report Deta...inal Report" "Output Details 25...inal Report"
# [75] "Project Acquittal...inal Report" "Attachments 25th ...inal Report"
#
# 7.	Cumberland+Plain, Improving+Your+Local+Parks+and+Environment, 
# Reef+2050+Plan,Reef+Trust
# > getSheetNames(paste('M07 ',extract_date,'.xlsx',sep=''))
# [1] "Outcomes Outcomes...inal report" "Evaluation Outcom...inal report"
# [3] "Lessons Learned O...inal report" "Administration Ac...inistration"
# [5] "Participant Infor...inistration" "Overview of Proje...tage report"
# [7] "Environmental, Ec...tage report" "Implementation Up...tage report"
# [9] "Lessons Learned a...tage report" "Survey Informatio...y - general"
# [11] "Fauna Survey Deta...y - general" "Participant Infor...y - general"
# [13] "Evidence of Pest ...imal Survey" "Pest Observation ...imal Survey"
# [15] "Participant Infor...imal Survey" "Event Details Com... Engagement"
# [17] "Participant Infor... Engagement" "Materials Provide... Engagement"
# [19] "Pest Management D... Management" "Fence Details Pest Management"  
# [21] "Participant Infor... Management" "Research Information Research"  
# [23] "Participant Infor...on Research" "Site Planning Det...ng and Risk"
# [25] "Threatening Proce...ng and Risk" "Participant Infor...ng and Risk"
# [27] "Training Details ...Development" "Skills Developmen...Development"
# [29] "Participant Infor...Development" "Management Practice Change"     
# [31] "RLP - Output WHS ...tput Report" "RLP - Baseline da...tput Report"
# [33] "RLP - Communicati...tput Report" "RLP - Community e...tput Report"
# [35] "RLP - Controlling...tput Report" "RLP - Pest animal...tput Report"
# [37] "RLP - Management ...tput Report" "RLP - Debris remo...tput Report"
# [39] "RLP - Erosion Man...tput Report" "RLP - Maintaining...tput Report"
# [41] "RLP - Establishin...tput Report" "RLP - Establishin...tput Rep(1)"
# [43] "RLP - Establishin...tput Rep(2)" "RLP - Farm Manage...tput Report"
# [45] "RLP - Fauna surve...tput Report" "RLP - Fire manage...tput Report"
# [47] "RLP - Flora surve...tput Report" "RLP - Habitat aug...tput Report"
# [49] "RLP - Identifying...tput Report" "RLP - Improving h...tput Report"
# [51] "RLP - Improving l...tput Report" "RLP - Disease man...tput Report"
# [53] "RLP - Negotiation...tput Report" "RLP - Obtaining a...tput Report"
# [55] "RLP - Pest animal...tput Rep(1)" "RLP - Plant survi...tput Report"
# [57] "RLP - Project pla...tput Report" "RLP - Remediating...tput Report"
# [59] "RLP - Weed treatm...tput Report" "RLP - Revegetatin...tput Report"
# [61] "RLP - Site prepar...tput Report" "RLP - Skills and ...tput Report"
# [63] "RLP - Soil testin...tput Report" "RLP - Emergency I...tput Report"
# [65] "RLP - Water quali...tput Report" "RLP - Weed distri...tput Report"
# [67] "RLP - Change Mana...tput Report" "RLP - Adapting to...tput Report"
# [69] "Seed Collecting -...tput Report" "RLP Annual Report"              
# [71] "RLP Short term project outcomes" "Site Monitoring Plan"           
# [73] "General informati...lity Survey" "Environmental Inf...lity Survey"
# [75] "Water Quality Mea...lity Survey" "Sampling Site Inf...methodology"
# [77] "Field Sheet 1 - G...methodology" "Field Sheet 2 - E...methodology"
# [79] "Field Sheet 3 - O...methodology" "Field Sheet 4 - C...methodology"
# [81] "Field Sheet 5 - S...methodology" "Fence Details Fencing"          
# [83] "Participant Information Fencing" "Plan Development ...Development"
# [85] "Participant Infor...Developm(1)" "Conservation Work...Communities"
# [87] "Participant Infor...Communities" "Revegetation Deta...evegetation"
# [89] "Participant Infor...evegetation" "Water Management"               
# [91] "Weed Treatment De...d Treatment" "Participant Infor...d Treatment"
# [93] "Erosion Managemen... Management" "Participant Infor... Managem(1)"
# [95] "Reef 2050 Plan Ac...orting 2018" "Reef 2050 Plan Action Reporting"
# [97] "Debris Removal De...ris Removal" "Participant Infor...ris Removal"
# [99] "Reef Trust Final Report"         "Sediment Savings"               
# [101] "Vegetation Monito...ival Survey" "Participant Infor...ival Survey"
# [103] "Evidence of Weed ... Monitoring" "Weed Observation ... Monitoring"
# [105] "Participant Infor... Monitoring" "Site Preparation ...Preparation"
# [107] "Weed Treatment De...Preparation" "Participant Infor...Preparation"
# [109] "Annual Stage Report"             "Access Control De...rastructure"
# [111] "Infrastructure De...rastructure" "Participant Infor...rastructure"
# [113] "Seed Collection D... Collection" "Participant Infor... Collection"
# [115] "Indigenous Employ... Businesses" "Indigenous Busine... Businesses"
# [117] "Conservation Grazing Management" "Survey Informatio...y - gene(1)"
# [119] "Flora Survey Deta...y - general" "Participant Infor...y - gene(1)"
# [121] "Heritage Conserva...onservation" "Expected Heritage...onservation"
# [123] "Participant Infor...onservation" "Indigenous Knowledge Transfer"  
# [125] "Plant Propagation...Propagation" "Participant Infor...Propagation"
# [127] "Public Access and... - with map"
#
# 8.	Complementary+Investment, Environmental+Restoration+Fund, 
# MER+Network+Pilot
# > getSheetNames(paste('M08 ',extract_date,'.xlsx',sep=''))
# [1] "Sheet 1"                         "RLP - Output WHS ...tput Report"
# [3] "RLP - Baseline da...tput Report" "RLP - Communicati...tput Report"
# [5] "RLP - Community e...tput Report" "RLP - Controlling...tput Report"
# [7] "RLP - Pest animal...tput Report" "RLP - Management ...tput Report"
# [9] "RLP - Debris remo...tput Report" "RLP - Erosion Man...tput Report"
# [11] "RLP - Maintaining...tput Report" "RLP - Establishin...tput Report"
# [13] "RLP - Establishin...tput Rep(1)" "RLP - Establishin...tput Rep(2)"
# [15] "RLP - Farm Manage...tput Report" "RLP - Fauna surve...tput Report"
# [17] "RLP - Fire manage...tput Report" "RLP - Flora surve...tput Report"
# [19] "RLP - Habitat aug...tput Report" "RLP - Identifying...tput Report"
# [21] "RLP - Improving h...tput Report" "RLP - Improving l...tput Report"
# [23] "RLP - Disease man...tput Report" "RLP - Negotiation...tput Report"
# [25] "RLP - Obtaining a...tput Report" "RLP - Pest animal...tput Rep(1)"
# [27] "RLP - Plant survi...tput Report" "RLP - Project pla...tput Report"
# [29] "RLP - Remediating...tput Report" "RLP - Weed treatm...tput Report"
# [31] "RLP - Revegetatin...tput Report" "RLP - Site prepar...tput Report"
# [33] "RLP - Skills and ...tput Report" "RLP - Soil testin...tput Report"
# [35] "RLP - Emergency I...tput Report" "RLP - Water quali...tput Report"
# [37] "RLP - Weed distri...tput Report" "RLP - Change Mana...tput Report"
# [39] "RLP - Adapting to...tput Report" "Seed Collecting -...tput Report"
# [41] "RLP Annual Report"               "RLP Short term project outcomes"
# [43] "RLP Medium term p...ct outcomes"
#
# 9.	National Landcare Programme->Regional Land Partnerships and 
# WA NLP Projects
# > getSheetNames(paste('M09 ',extract_date,'.xlsx',sep=''))
# [1] "RLP - Output WHS ...tput Report" "RLP - Baseline da...tput Report"
# [3] "RLP - Communicati...tput Report" "RLP - Community e...tput Report"
# [5] "RLP - Controlling...tput Report" "RLP - Pest animal...tput Report"
# [7] "RLP - Management ...tput Report" "RLP - Debris remo...tput Report"
# [9] "RLP - Erosion Man...tput Report" "RLP - Maintaining...tput Report"
# [11] "RLP - Establishin...tput Report" "RLP - Establishin...tput Rep(1)"
# [13] "RLP - Establishin...tput Rep(2)" "RLP - Farm Manage...tput Report"
# [15] "RLP - Fauna surve...tput Report" "RLP - Fire manage...tput Report"
# [17] "RLP - Flora surve...tput Report" "RLP - Habitat aug...tput Report"
# [19] "RLP - Identifying...tput Report" "RLP - Improving h...tput Report"
# [21] "RLP - Improving l...tput Report" "RLP - Disease man...tput Report"
# [23] "RLP - Negotiation...tput Report" "RLP - Obtaining a...tput Report"
# [25] "RLP - Pest animal...tput Rep(1)" "RLP - Plant survi...tput Report"
# [27] "RLP - Project pla...tput Report" "RLP - Remediating...tput Report"
# [29] "RLP - Weed treatm...tput Report" "RLP - Revegetatin...tput Report"
# [31] "RLP - Site prepar...tput Report" "RLP - Skills and ...tput Report"
# [33] "RLP - Soil testin...tput Report" "RLP - Emergency I...tput Report"
# [35] "RLP - Water quali...tput Report" "RLP - Weed distri...tput Report"
# [37] "RLP - Change Mana...tput Report" "RLP - Adapting to...tput Report"
# [39] "Seed Collecting -...tput Report" "RLP Annual Report"              
# [41] "RLP Short term project outcomes" "RLP Medium term p...ct outcomes"
# [43] "RLP Output Report Adjustment"
#
# 10.	3ANational+Landcare+Programme&fq=associatedSubProgramFacet%3A20+Million+Trees+Cumberland+Conservation+Corridor+Grants&fq=associatedSubProgramFacet%3A20+Million+Trees+Cumberland+Conservation+Corridor+Land+Management&fq=associatedSubProgramFacet%3A20+Million+Trees+Discretionary+Grants&fq=associatedSubProgramFacet%3A20+Million+Trees+Grants+Round+1&fq=associatedSubProgramFacet%3A20+Million+Trees+Grants+Round+2&fq=associatedSubProgramFacet%3A20+Million+Trees+Grants+Round+3&fq=associatedSubProgramFacet%3A20+Million+Trees+Service+Providers&fq=associatedSubProgramFacet%3A20+Million+Trees+Service+Providers+Tranche+2&fq=associatedSubProgramFacet%3A20+Million+Trees+Service+Providers+Tranche+3&fq=associatedSubProgramFacet%3A20+Million+Trees+West+Melbourne
# > getSheetNames(paste('M10 ',extract_date,'.xlsx',sep=''))
# [1] "Outcomes Outcomes...inal report" "Evaluation Outcom...inal report"
# [3] "Lessons Learned O...inal report" "Administration Ac...inistration"
# [5] "Participant Infor...inistration" "Overview of Proje...tage report"
# [7] "Environmental, Ec...tage report" "Implementation Up...tage report"
# [9] "Lessons Learned a...tage report" "Vegetation Monito...ival Survey"
# [11] "Participant Infor...ival Survey" "Fence Details Fencing"          
# [13] "Participant Information Fencing" "Plan Development ...Development"
# [15] "Participant Infor...Development" "Conservation Work...Communities"
# [17] "Participant Infor...Communities" "Revegetation Deta...evegetation"
# [19] "Participant Infor...evegetation" "Site Preparation ...Preparation"
# [21] "Weed Treatment De...Preparation" "Participant Infor...Preparation"
# [23] "Weed Treatment De...d Treatment" "Participant Infor...d Treatment"
# [25] "Survey Informatio...y - general" "Flora Survey Deta...y - general"
# [27] "Participant Infor...y - general" "Event Details Com... Engagement"
# [29] "Participant Infor... Engagement" "Materials Provide... Engagement"
# [31] "Indigenous Knowledge Transfer"   "Survey Informatio...y - gene(1)"
# [33] "Fauna Survey Deta...y - general" "Participant Infor...y - gene(1)"
# [35] "Debris Removal De...ris Removal" "Participant Infor...ris Removal"
# [37] "Plant Propagation...Propagation" "Participant Infor...Propagation"
# [39] "Seed Collection D... Collection" "Participant Infor... Collection"
# [41] "Post revegetation... management" "Post revegetation... managem(1)"
# [43] "Post revegetation... managem(2)" "Post revegetation... managem(3)"
# [45] "Pest Management D... Management" "Fence Details Pest Management"  
# [47] "Participant Infor... Management" "Site Monitoring Plan"           
# [49] "Training Details ...Development" "Skills Developmen...Development"
# [51] "Participant Infor...Developm(1)" "Indigenous Employ... Businesses"
# [53] "Indigenous Busine... Businesses" "Site Planning Det...ng and Risk"
# [55] "Threatening Proce...ng and Risk" "Participant Infor...ng and Risk"
# [57] "Evidence of Weed ... Monitoring" "Weed Observation ... Monitoring"
# [59] "Participant Infor... Monitoring" "Sampling Site Inf...methodology"
# [61] "Field Sheet 1 - G...methodology" "Field Sheet 2 - E...methodology"
# [63] "Field Sheet 3 - O...methodology" "Field Sheet 4 - C...methodology"
# [65] "Field Sheet 5 - S...methodology" "General informati...lity Survey"
# [67] "Environmental Inf...lity Survey" "Water Quality Mea...lity Survey"
# [69] "Management Practice Change"      "Evidence of Pest ...imal Survey"
# [71] "Pest Observation ...imal Survey" "Participant Infor...imal Survey"
# [73] "Erosion Managemen... Management" "Participant Infor... Managem(1)"
# [75] "Research Information Research"   "Participant Infor...on Research"
# [77] "Access Control De...rastructure" "Infrastructure De...rastructure"
# [79] "Participant Infor...rastructure" "Fire Management D... Management"
# [81] "Participant Infor... Managem(2)" "Heritage Conserva...onservation"
# [83] "Expected Heritage...onservation" "Participant Infor...onservation"
#
# 11.	fq=associatedProgramFacet%3ANational+Landcare+Programme&fq=associatedSubProgramFacet%3A25th+Anniversary+Landcare+Grants+2014-15&fq=associatedSubProgramFacet%3ALandcare+Network+Grants+2014-16&fq=associatedSubProgramFacet%3ALocal+Programmes&fq=associatedSubProgramFacet%3ARegional+Funding"
# > getSheetNames(paste('M11 ',extract_date,'.xlsx',sep=''))
# [1] "Regional Funding Final Report"   "Indigenous Employ... Businesses"
# [3] "Indigenous Busine... Businesses" "Administration Ac...inistration"
# [5] "Participant Infor...inistration" "Overview of Proje...tage report"
# [7] "Environmental, Ec...tage report" "Implementation Up...tage report"
# [9] "Lessons Learned a...tage report" "Stage Report"                   
# [11] "1. Community Gran...nity Grants" "2. Community Gran...nity Grants"
# [13] "Attachments Community Grants"    "Event Details Com... Engagement"
# [15] "Participant Infor... Engagement" "Materials Provide... Engagement"
# [17] "Fire Management D... Management" "Participant Infor... Management"
# [19] "Plan Development ...Development" "Participant Infor...Development"
# [21] "Management Practice Change"      "Pest Management D... Management"
# [23] "Fence Details Pest Management"   "Participant Infor... Managem(1)"
# [25] "Water Management"                "Weed Treatment De...d Treatment"
# [27] "Participant Infor...d Treatment" "Site Planning Det...ng and Risk"
# [29] "Threatening Proce...ng and Risk" "Participant Infor...ng and Risk"
# [31] "Training Details ...Development" "Skills Developmen...Development"
# [33] "Participant Infor...Developm(1)" "Progress Report D...ress Report"
# [35] "Attachments 25th ...ress Report" "Final Report Deta...inal Report"
# [37] "Output Details 25...inal Report" "Project Acquittal...inal Report"
# [39] "Attachments 25th ...inal Report" "Outcomes Outcomes...inal report"
# [41] "Evaluation Outcom...inal report" "Lessons Learned O...inal report"
# [43] "Annual Stage Report"             "Access Control De...rastructure"
# [45] "Infrastructure De...rastructure" "Participant Infor...rastructure"
# [47] "Site Preparation ...Preparation" "Weed Treatment De...Preparation"
# [49] "Participant Infor...Preparation" "Research Information Research"  
# [51] "Participant Infor...on Research" "Conservation Work...Communities"
# [53] "Participant Infor...Communities" "Survey Informatio...y - general"
# [55] "Fauna Survey Deta...y - general" "Participant Infor...y - general"
# [57] "Survey Informatio...y - gene(1)" "Flora Survey Deta...y - general"
# [59] "Participant Infor...y - gene(1)" "Evidence of Pest ...imal Survey"
# [61] "Pest Observation ...imal Survey" "Participant Infor...imal Survey"
# [63] "Erosion Managemen... Management" "Participant Infor... Managem(2)"
# [65] "Revegetation Deta...evegetation" "Participant Infor...evegetation"
# [67] "Seed Collection D... Collection" "Participant Infor... Collection"
# [69] "Fence Details Fencing"           "Participant Information Fencing"
# [71] "Site Monitoring Plan"            "Evidence of Weed ... Monitoring"
# [73] "Weed Observation ... Monitoring" "Participant Infor... Monitoring"
# [75] "Debris Removal De...ris Removal" "Participant Infor...ris Removal"
# [77] "Indigenous Knowledge Transfer"   "Vegetation Monito...ival Survey"
# [79] "Participant Infor...ival Survey" "Plant Propagation...Propagation"
# [81] "Participant Infor...Propagation" "Heritage Conserva...onservation"
# [83] "Expected Heritage...onservation" "Participant Infor...onservation"
# [85] "Conservation Grazing Management" "General informati...lity Survey"
# [87] "Environmental Inf...lity Survey" "Water Quality Mea...lity Survey"
# [89] "Sampling Site Inf...methodology" "Field Sheet 1 - G...methodology"
# [91] "Field Sheet 2 - E...methodology" "Field Sheet 3 - O...methodology"
# [93] "Field Sheet 4 - C...methodology" "Field Sheet 5 - S...methodology"
# [95] "Asset Protection ... Management" "Ecological Burn D... Management"
# [97] "Participant Infor... Managem(3)" "Disease Managemen... Management"
# [99] "Participant Infor... Managem(4)" "Post revegetation... management"
# [101] "Post revegetation... managem(1)" "Post revegetation... managem(2)"
# [103] "Post revegetation... managem(3)"
#
# 12. without report data
# > getSheetNames(paste('M12 ',extract_date,'.xlsx',sep=''))
# [1] "RLP Core Services report"        "RLP Core Services annual report"
#
# 13. with report data
# > getSheetNames(paste('M13 ',extract_date,'.xlsx',sep=''))
# [1] "RLP Core Services report"        "RLP Core Services annual report"

extract_date <- '2022-06-20'

project_cols_in <- c(
  'project_id','grant_id','external_id','internal_order_number','work_order_id',
  'program','sub_program','name','description','management_unit','organisation',
  'status','report_financial_year','start_date','end_date',
  'contracted_start_date','contracted_end_date','last_modified_2')
project_cols_out <- c(
  'project_id','grant_id','external_id','internal_order_number','work_order_id',
  'organisation','management_unit','mu_id','mu_state','project_name',
  'program','sub_program','project_start_date', 'project_end_date',
  'project_contracted_start_date','project_contracted_end_date','project_status')

project_meta_cols_out <- c(
  'meta_source_sheetname','meta_col_project_start_date',
  'meta_col_project_end_date','meta_col_project_contracted_start_date',
  'meta_col_project_contracted_end_date','meta_col_project_name')

# Reports
report_cols_in <- c(
  'site_id','report_status','status_2','report_financial_year','stage',
  'activity_id', 'activity_type','report_from_date','report_to_date')
report_cols_out <- c(
  'MERIT_Reports_link','report_financial_year','report_status','service',
  'target_measure','context','site_id','report_last_modified','category',
  'subcategory','report_species','total_to_be_delivered','fy_target',
  'measured','invoiced','actual','report_stage','report_activity_type',
  'report_from_date','report_to_date')
report_meta_cols_out <- c(
  'meta_col_measured','meta_col_actual','meta_col_invoiced','meta_col_category',
  'meta_text_subcategory','meta_col_context','meta_col_report_species',
  'meta_line_item_object_class','meta_line_item_property','meta_line_item_value',
  'meta_col_project_status','meta_col_report_last_modified','meta_col_report_stage',
  'meta_col_report_activity_type')

#Species Etc
species_etc_cols_out <- c(
  'primary_secondary_outcomes','primary_outcomes','secondary_outcomes',
  'primary_secondary_investment_priorities','primary_investment_priority',
  'secondary_investment_priority','documents_priority','assets',
  'natural_cultural_assets_managed','threatened_species', 
  'threatened_ecological_communities','migratory_species',
  'ramsar_wetland,world_heritage_area','community_awareness_participation_in_nrm',
  'indigenous_cultural_values','indigenous_ecological_knowledge',
  'remnant_vegetation','aquatic_and_coastal_systems_including_wetlands',
  'report_species','epbc','tec','ramsar')

numeric_cols <- c(
  'measured','invoiced','actual','report_from_date',
  'report_to_date','start_date','end_date',
  'contracted_start_date','contracted_end_date',
  'last_modified_2')

character_cols <- c(
  'management_unit','external_id','site_id','organisation','report_species',
  'category','context')

extract_date_cols <- c('grant_or_procurement','report_to_date','extract_date')

meri_outcomes_indicator_ref <- c(
  "natural_cultural_assets_managed","threatened_species",
  "threatened_ecological_communities", "migratory_species","ramsar_wetland",
  "world_heritage_area","community_awareness_participation_in_nrm",     
  "indigenous_cultural_values","indigenous_ecological_knowledge",            
  "remnant_vegetation","aquatic_and_coastal_systems_including_wetlands",
  "world_heritage_area","community_awareness_participation_in_nrm",    
  "indigenous_cultural_values","indigenous_ecological_knowledge",
  "remnant_vegetation","aquatic_and_coastal_systems_including_wetlands")

load("management_units.Rdata")
load("sprat_lookup.Rdata")

str_to_colname <- function(a_col) {
  a_col_name <- rlang::parse_expr(a_col)
}

read_sheet <- function(sheet_name,fname,start_row=3) {
  fred <- read.xlsx(fname, 
                    sheet=sheet_name,
                    startRow = start_row) %>%
    clean_names() %>%
    mutate(across(contains("management_unit"),as.character),
           across(c(grant_id,external_id,internal_order_number, 
                    work_order_id),as.character))
}

read_sheet_for_bulk <- function(sheet_name,fname,start_row=3) {
  fred <- read.xlsx(fname,
                    sheet=sheet_name,
                    startRow = start_row) %>%
    clean_names() %>%
    mutate(across(everything(),as.character))
}

load_mult_wbooks <- function(files_vec,sheetname) {
  #files_vec <- c('M02','M05','M07','M08','M09')
  files_vec <- str_c(files_vec," ",extract_date,".xlsx",sep="")
  sheets_vec <- rep(sheetname,length(files_vec))
  
  the_file <- map2_dfr(sheets_vec,files_vec,read_sheet_for_bulk) 
}

conc_species_col <- function(Data) {
  Data_out <- Data %>% 
    group_by(across(c(-measured,-actual,-invoiced,-report_species,
                      -context))) %>%
    summarise(report_species = str_c(report_species,collapse="|"),
              context = str_c(context,collapse="|"),
              measured = first(measured),
              actual = first(actual),
              invoiced = first(invoiced)) %>% 
    ungroup() %>%
    mutate(report_species = str_replace_all(report_species,'\n','|'))
}

filter_na <- function(Data) {
  Data <- Data %>%
    conc_species_col() %>%
    filter(!is.na(measured) | !is.na(actual) | !is.na(invoiced) | 
             !is.na(report_species)) 
}

# load the investment priority data for R data file
load('investment_priority_themes.Rdata')
investment_priority_themes <- investment_priority_themes %>%
  rename(investment_priority_derived=investment_priority,
         investment_priority=merit_lookup,
         short_term_indicator=short_term_outcome_indicator_outcome) 

RLP_Outcomes <- read.xlsx(paste('M01 ',extract_date,'.xlsx',sep=''), 
                          sheet='RLP Outcomes',
                          startRow = 1) %>%
  clean_names() %>% 
  select(grant_id,type_of_outcomes,investment_priority) 

RLP_Outcomes_short_term_indicator <- RLP_Outcomes %>%
  filter(type_of_outcomes=='Primary outcome') %>%
  separate_rows(investment_priority,sep=",") %>%
  mutate(investment_priority=str_trim(investment_priority)) %>%
  left_join(investment_priority_themes,by='investment_priority') %>%
  select(grant_id, type_of_outcomes,
         investment_priority, short_term_indicator)

EPBC <- RLP_Outcomes_short_term_indicator %>%
  mutate(epbc=ifelse(short_term_indicator=='Threatened Species',"Y","N")) %>%
  filter(epbc=='Y') %>%
  select(grant_id,epbc) %>%
  drop_na(epbc) %>%
  distinct()

TEC <- RLP_Outcomes_short_term_indicator %>%
  mutate(tec=ifelse(short_term_indicator=='Threatened Ecological Community',
                    'Y','N')) %>%
  filter(tec=='Y') %>%
  select(grant_id,tec) %>%
  drop_na(tec) %>%
  distinct()

RAMSAR <- RLP_Outcomes_short_term_indicator %>%
  mutate(ramsar=ifelse(short_term_indicator=='Ramsar','Y','N')) %>%
  filter(ramsar=='Y') %>%
  select(grant_id,ramsar) %>%
  drop_na(ramsar) %>%
  distinct()

output_targets <- read_sheet(sheet='Project services and targets',
                             fname=paste('M01 ',extract_date,'.xlsx',sep=''),
                             start_row = 1) %>%
  mutate(total_to_be_delivered=as.numeric(total_to_be_delivered)) %>%
  select(grant_id,service,
         target_measure,total_to_be_delivered,
         `2018/2019`=x2018_2019,`2019/2020`=x2019_2020,
         `2020/2021`=x2020_2021,`2021/2022`=x2021_2022,
         `2021/2022`=x2021_2022,`2022/2023`=x2022_2023) %>%
  pivot_longer(cols= starts_with("20"),names_to='report_financial_year',
               values_to='fy_target') %>%
  mutate(fy_target=as.numeric(fy_target)) 

filter_by_service_target_measures_and_distinct <- function(Data,service,
                                                           target_measure) {
  fred <- Data %>%
    mutate(across(all_of(numeric_cols),as.numeric),
           across(all_of(character_cols),as.character),
           grant_or_procurement='procurement',
           service=service, target_measure=target_measure) %>%
    inner_join(output_targets,by=c("grant_id","service","target_measure",
                                   "report_financial_year")) %>%
    filter(!is.na(total_to_be_delivered)) %>%
    distinct() 
}

no_category_extract_no_context_no_species <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced,
    object_class=NA, property=NA, value=NA, category=NA, context=NA, 
    sub_category=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           measured={{ measured }},invoiced={{ invoiced }},
           actual={{ actual }}) %>%
    mutate(category=NA, context=NA, report_species=NA) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    fred <- fred %>%
      mutate(meta_source_sheetname=worksheet, 
             meta_col_measured = measured_text,
             meta_col_actual = actual_text,
             meta_col_invoiced = invoiced_text,
             meta_col_category=NA,
             meta_col_context=NA,
             meta_text_subcategory=NA,
             meta_col_report_species=NA,
             meta_line_item_object_class=object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>%
      mutate(across(starts_with("meta"),as.character))}
  return(fred)
}

all_sub_category_extract_no_context_no_species <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced,
    category, object_class=NA, property=NA, value=NA, context=NA, species=NA,
    sub_category=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           category={{ category }},measured= {{ measured }},
           invoiced={{ invoiced }},actual={{ actual }}) %>%
    filter(!is.na(category)) %>%
    mutate(context=NA, report_species=NA) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure)
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    category_text <- as_label(enquo(category))
    fred <- fred %>%
      mutate(meta_source_sheetname=worksheet,
             meta_col_measured=measured_text,
             meta_col_actual=actual_text,
             meta_col_invoiced=invoiced_text,
             meta_col_category=category_text,
             meta_col_context=NA,
             meta_text_subcategory=NA,
             meta_col_report_species=NA,
             meta_line_item_object_class=object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>%
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

all_sub_category_extract_context_species <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced,
    category, context, species, object_class=NA, property=NA, value=NA,
    sub_category=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           category={{ category }},measured= {{ measured }},
           invoiced={{ invoiced }},actual={{ actual }},
           context= {{ context }},report_species= {{ species }}) %>%
    filter(!is.na(category)) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    category_text <- as_label(enquo(category))
    context_text <- as_label(enquo(context))
    species_text <- as_label(enquo(species))
    fred <- fred %>%
      mutate(meta_source_sheetname=worksheet, 
             meta_col_measured = measured_text,
             meta_col_actual = actual_text,
             meta_col_invoiced = invoiced_text,
             meta_col_category=category_text,
             meta_col_context=context_text,
             meta_col_report_species=species_text,
             meta_text_subcategory=NA,
             meta_line_item_object_class=object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>% 
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

all_sub_category_extract_context_no_species <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced,
    category, context, object_class=NA, property=NA, value=NA, species=NA,
    sub_category=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           category={{ category }},measured= {{ measured }},
           invoiced={{ invoiced }}, actual={{ actual }},
           context= {{ context }}) %>%
    filter(!is.na(category)) %>%
    mutate(report_species=NA) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    category_text <- as_label(enquo(category))
    context_text <- as_label(enquo(context))
    fred <- fred %>%
      mutate(meta_source_sheetname=worksheet, 
             meta_col_measured=measured_text,
             meta_col_actual=actual_text,
             meta_col_invoiced=invoiced_text,
             meta_col_category=category_text,
             meta_col_context=context_text,
             meta_text_subcategory=NA,
             meta_col_report_species=NA,
             meta_line_item_object_class=object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>% 
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

no_category_extract_context_no_species <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced,
    context, object_class=NA, property=NA, value=NA, category=NA, species=NA,
    sub_category=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           measured= {{ measured }},invoiced={{ invoiced }},
           actual={{ actual }}, context= {{ context }}) %>%
    mutate(category=NA, report_species=NA) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    context_text <- as_label(enquo(context))
    fred <- fred %>% 
      mutate(meta_source_sheetname=worksheet,
             meta_col_measured = measured_text,
             meta_col_actual = actual_text,
             meta_col_invoiced = invoiced_text,
             meta_col_context=context_text,
             meta_col_category=NA,
             meta_text_subcategory=NA,
             meta_col_report_species=NA,
             meta_line_item_object_class=object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>% 
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

sub_category_extract_context_species  <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced, 
    category, sub_category, context, species, object_class=NA,property=NA,
    value=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           category={{ category }},measured= {{ measured }},
           invoiced={{ invoiced }},actual={{ actual }},
           context = {{ context }},report_species = {{ species }}) %>%
    filter(category==sub_category) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    category_text <- as_label(enquo(category))
    context_text <- as_label(enquo(context))
    species_text <- as_label(enquo(species))
    fred <- fred %>%
      mutate(meta_source_sheetname=worksheet,
             meta_col_measured=measured_text,
             meta_col_actual=actual_text,
             meta_col_invoiced=invoiced_text,
             meta_col_category=category_text,
             meta_col_context=context_text,
             meta_col_report_species=species_text,
             meta_text_subcategory=sub_category,
             meta_line_item_object_class=object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>% 
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

sub_category_extract_context_no_species  <- function(
    Data, worksheet, service, target_measure, measured, actual,invoiced, 
    category,sub_category, context,object_class=NA, property=NA, value=NA,
    species=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           category={{ category }},measured= {{ measured }},
           invoiced={{ invoiced }},actual={{ actual }},
           context = {{ context }}) %>%
    filter(category==sub_category) %>%
    mutate(report_species = NA) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    category_text <- as_label(enquo(category))
    context_text <- as_label(enquo(context))
    fred <- fred %>% 
      mutate(meta_source_sheetname=worksheet, 
             meta_col_measured=measured_text,
             meta_col_actual=actual_text,
             meta_col_invoiced=invoiced_text,
             meta_col_category=category_text,
             meta_col_context=context_text,
             meta_text_subcategory=sub_category,
             meta_col_report_species=NA,
             meta_line_item_object_class=object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>% 
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

sub_category_extract_no_context_species <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced, 
    category, sub_category, species, object_class=NA, property=NA, value=NA,
    context=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           category={{ category }},measured= {{ measured }},
           invoiced={{ invoiced }},actual={{ actual }},
           report_species={{ species }}) %>%
    filter(category==sub_category) %>%
    mutate(context=NA) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    category_text <- as_label(enquo(category))
    species_text <- as_label(enquo(species))
    fred <- fred %>%
      mutate(meta_source_sheetname=worksheet,
             meta_col_measured=measured_text,
             meta_col_actual=actual_text,
             meta_col_invoiced=invoiced_text,
             meta_col_category=category_text,
             meta_col_report_species=species_text,
             meta_col_context = NA,
             meta_text_subcategory = sub_category,
             meta_line_item_object_class = object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>% 
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

sub_category_extract_no_context_no_species <- function(
    Data, worksheet, service, target_measure, measured, actual, invoiced,
    category, sub_category, object_class=NA, property=NA, value=NA, context=NA,
    species=NA) {
  fred <-
    Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           category={{ category }},measured={{ measured }},
           invoiced={{ invoiced }}, actual={{ actual }}) %>%
    filter(category==sub_category) %>%
    mutate(context=NA, report_species=NA) %>%
    filter_by_service_target_measures_and_distinct(service,target_measure) %>%
    filter_na()
  
  if (nrow(fred) >0) {
    measured_text <- as_label(enquo(measured))
    actual_text <- as_label(enquo(actual))
    invoiced_text <- as_label(enquo(invoiced))
    category_text <- as_label(enquo(category))
    fred <- fred %>% 
      mutate(meta_source_sheetname=worksheet,
             meta_col_measured=measured_text,
             meta_col_actual=actual_text,
             meta_col_invoiced=invoiced_text,
             meta_col_category=category_text,
             meta_col_context = NA,
             meta_text_subcategory = sub_category,
             meta_col_report_species = NA,
             meta_line_item_object_class = object_class,
             meta_line_item_property=property,
             meta_line_item_value=value) %>% 
      mutate(across(starts_with("meta"),as.character))
  }
  return(fred)
}

grant_report_no_species <- function(
    Data,sheet_name,start_row=3,measured_col,actual_col,invoiced_col,
    context_col, object_class=NA,property=NA,value=NA) {
  fred <- Data %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           contracted_end_date,last_modified_2,measured={{ measured_col }},
           actual={{ actual_col }},invoiced={{ invoiced_col }},
           context= {{ context_col }}) %>%
    mutate(total_to_be_delivered=NA,fy_target=NA,    
           category=NA,subcategory=NA,
           report_species=NA,
           meta_col_report_species=NA,meta_text_subcategory=NA,
           meta_col_category=NA,service=str_c(activity_type,' > ',sheet_name),
           target_measure= as_label(enquo(measured_col)),
           meta_source_sheetname=sheet_name,
           across(all_of(numeric_cols),as.numeric),
           across(all_of(character_cols),as.character),
           meta_col_measured=as_label(enquo(measured_col)),
           meta_col_actual=as_label(enquo(actual_col)),
           meta_col_invoiced=as_label(enquo(invoiced_col)),
           target_measure=as_label(enquo(measured_col)),
           meta_col_context=as_label(enquo(context_col)),
           grant_or_procurement='grant',
           meta_line_item_object_class = object_class,
           meta_line_item_property=property,
           meta_line_item_value=value) %>%
    filter_na()
}

grant_report_species <- function(
    Data,sheet_name,start_row=3,measured_col,actual_col,invoiced_col,
    context_col,species_col, object_class=NA,property=NA,value=NA) {
  fred <- Data %>%
    filter(!is.na({{ species_col}}) | {{ species_col}}=='NA') %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           measured={{ measured_col }},
           actual={{ actual_col }},invoiced={{ invoiced_col }},
           context= {{ context_col }},report_species= {{ species_col }}) %>%
    mutate(total_to_be_delivered=NA,fy_target=NA,       
           category=NA,subcategory=NA,
           meta_text_subcategory=NA,meta_col_category=NA,
           across(all_of(numeric_cols),as.numeric),
           across(all_of(character_cols),as.character),
           service=str_c(activity_type,' > ',sheet_name),
           target_measure= as_label(enquo(measured_col)),
           meta_source_sheetname=sheet_name,
           meta_col_measured=as_label(enquo(measured_col)),
           meta_col_actual=as_label(enquo(actual_col)),
           meta_col_invoiced=as_label(enquo(invoiced_col)),
           target_measure=as_label(enquo(measured_col)),
           meta_col_context=as_label(enquo(context_col)),
           meta_col_report_species=as_label(enquo(species_col)),
           grant_or_procurement='grant',
           meta_line_item_object_class = object_class,
           meta_line_item_property=property,
           meta_line_item_value=value)
}

grant_report_species_category <- function(
    Data,sheet_name,start_row=3,category_col,measured_col,
    actual_col,invoiced_col,context_col,species_col,
    object_class=NA,property=NA,value=NA,sub_category=NA) {
  fred <- Data %>%
    filter(!is.na({{ species_col}}) | {{ species_col}}=='NA') %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           measured={{ measured_col }},category={{ category_col }}, 
           actual={{ actual_col }},invoiced={{ invoiced_col }}, 
           context= {{ context_col }}, report_species= {{ species_col }}) %>%
    mutate(total_to_be_delivered=NA,fy_target=NA,       
           subcategory=NA,
           meta_text_subcategory=NA,meta_col_category=NA,
           across(all_of(numeric_cols),as.numeric),
           across(all_of(character_cols),as.character),
           service=str_c(activity_type,' > ',sheet_name),
           target_measure= as_label(enquo(measured_col)),
           meta_source_sheetname=sheet_name,
           meta_col_measured=as_label(enquo(measured_col)),
           meta_col_actual=as_label(enquo(actual_col)),
           meta_col_invoiced=as_label(enquo(invoiced_col)),
           target_measure=as_label(enquo(measured_col)),
           meta_col_context=as_label(enquo(context_col)),
           meta_col_report_species=as_label(enquo(species_col)),
           grant_or_procurement='grant',
           meta_line_item_object_class = object_class,
           meta_line_item_property=property,
           meta_line_item_value=value)
}

grant_report_species_no_metrics <- function(
    Data,sheet_name,start_row=3,context_col,species_col,object_class=NA,
    property=NA,value=NA) {
  fred <- Data %>%
    filter(!is.na({{ species_col}}) | {{ species_col}}=='NA') %>%
    select(one_of(project_cols_in),one_of(report_cols_in),
           context= {{ context_col }},report_species= {{ species_col }}) %>%
    mutate(measured=NA,actual=NA,invoiced=NA,fy_target=NA,
           total_to_be_delivered=NA,category=NA,subcategory=NA,
           meta_col_category=NA,meta_col_measured=NA,meta_col_actual=NA,
           meta_col_invoiced=NA,meta_text_subcategory=NA,  
           across(all_of(numeric_cols),as.numeric),
           across(all_of(character_cols),as.character),
           meta_source_sheetname=sheet_name,
           service=str_c(activity_type,' > ',sheet_name),
           target_measure= as_label(enquo(species_col)),
           target_measure=as_label(enquo(species_col)),
           meta_col_context=as_label(enquo(context_col)),
           meta_col_report_species=as_label(enquo(species_col)),          
           grant_or_procurement='grant',
           meta_line_item_object_class = object_class,
           meta_line_item_property=property,
           meta_line_item_value=value)
}

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Baseline da...tput Report')
BR_Data <- load_mult_wbooks(c('M05'), 'Baseline data Sta...inal Report')

Report_Raw <- 
  bind_rows(
    no_category_extract_no_context_no_species(
      Data = RLP_Data,
      worksheet = 'RLP - Baseline da...tput Report',
      service= "Collecting, or synthesising baseline data",
      target_measure = "Number of baseline data sets collected and/or synthesised",
      measured = number_of_baseline_data_sets_collected_and_or_synthesised,
      invoiced = number_of_baseline_data_sets_collected_and_or_synthesised,
      actual = number_of_baseline_data_sets_collected_and_or_synthesised,
      object_class='Baseline Data',property='collected and/or synthesised',
      value='Total Data Sets'),
    no_category_extract_no_context_no_species(
      Data=BR_Data,
      worksheet = 'Baseline data Sta...inal Report',
      service= "Collecting, or synthesising baseline data",
      target_measure = "Number of baseline data sets collected and/or synthesised",
      measured = number_of_baseline_data_sets_collected_and_or_synthesised,
      invoiced = number_of_baseline_data_sets_collected_and_or_synthesised,
      actual = number_of_baseline_data_sets_collected_and_or_synthesised,
      object_class='Baseline data sets',property='collected and/or synthesised',
      value='Total Data Sets'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Communicati...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_no_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Communicati...tput Report',
    service= "Communication materials",
    target_measure = "Number of communication materials published",
    measured = number_of_communication_materials_published,
    invoiced = number_of_communication_materials_published,
    actual = number_of_communication_materials_published,
    object_class='Communication materials',property='Publication',
    value='Total Data Sets'))

BR_Data <- load_mult_wbooks(c('M05'), 'Communication mat...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_no_context_no_species(
    Data=BR_Data,
    worksheet = 'Communication mat...inal Report',
    service= "Communication materials",
    target_measure = "Number of communication materials published",
    measured = number_of_communication_materials_published,
    invoiced = number_of_communication_materials_published,
    actual = number_of_communication_materials_published,
    object_class='Communication materials',property='Publication',
    value='Total Published Communication Materials'))  

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Community e...tput Report')
BR_Data <- load_mult_wbooks(c('M05'), 'Community engagem...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  sub_category_extract_no_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Community e...tput Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of conferences / seminars",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    context=purpose_of_engagement,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category = 'Conferences / seminars',
    object_class='Community Engagement',property='conferences / seminars',
    value='Total Events'),
  sub_category_extract_no_context_no_species(
    Data=BR_Data,
    worksheet = 'Community engagem...inal Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of conferences / seminars",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category = 'Conferences / seminars',
    context=purpose_of_engagement,
    object_class='Community Engagement',property='conferences / seminars',
    value='Total Events'),
  sub_category_extract_no_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Community e...tput Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of field days",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category='Field days',
    object_class='Community Engagement',property='field days',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Community engagem...inal Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of field days",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category='Field days',
    context=purpose_of_engagement,
    object_class='Community Engagement',property='field days',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Community e...tput Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of on-ground trials / demonstrations",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category='On-ground trials / demonstrations',
    context=purpose_of_engagement,
    object_class='Community Engagement',property='On-ground trials / demonstrations',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Community engagem...inal Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of on-ground trials / demonstrations",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category='On-ground trials / demonstrations',
    context=purpose_of_engagement,
    object_class='Community Engagement',property='On-ground trials / demonstrations',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Community e...tput Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of on-ground works",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    context=purpose_of_engagement,
    sub_category='On-ground works',
    object_class='Community Engagement',property='on-ground works',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Community engagem...inal Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of on-ground works",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    context=purpose_of_engagement,
    sub_category='On-ground works',
    object_class='Community Engagement',property='on-ground works',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Community e...tput Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of one-on-one technical advice interactions",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    context=purpose_of_engagement,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category='One-on-one technical advice interactions',
    object_class='Community Engagement',property='one-on-one technical advice interactions',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Community engagem...inal Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of one-on-one technical advice interactions",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category='One-on-one technical advice interactions',
    context=purpose_of_engagement,
    object_class='Community Engagement',
    property='one-on-one technical advice interactions',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Community e...tput Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of training / workshop events",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    context=purpose_of_engagement,
    sub_category='Training / workshop events',
    object_class='Community Engagement',property='training / workshop events',
    value='Total Events'),
  sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Community engagem...inal Report',
    service = "Community/stakeholder engagement",
    target_measure = "Number of training / workshop events",
    measured = number_of_community_stakeholder_engagement_type_events,
    invoiced = number_of_community_stakeholder_engagement_type_events,
    actual = number_of_community_stakeholder_engagement_type_events,
    category=type_of_community_stakeholder_engagement_activity,
    sub_category='Training / workshop events',
    context=purpose_of_engagement,
    object_class='Community Engagement',property='training / workshop events',
    value='Total Events'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Controlling...tput Report')
BR_Data <- load_mult_wbooks(c('M05'), 'Controlling acces...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Controlling...tput Report',
    service = "Controlling access",
    target_measure = "Area (ha) where access has been controlled",
    measured = sites_installed_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = area_ha_where_access_has_been_controlled,
    context=control_objective,
    object_class='Sites',property='Access control measures',
    value='Total Area (Ha)'),
  no_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Controlling acces...inal Report',
    service = "Controlling access",
    target_measure = "Area (ha) where access has been controlled",
    measured = sites_installed_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = sites_installed_calculated_area_ha,
    context=control_objective,
    object_class='Sites',property='Access control measures',
    value='Total Area (Ha)'),
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Controlling...tput Report',
    service = "Controlling access",
    target_measure = "Length (km) installed",
    measured = sites_installed_calculated_length_km,
    invoiced = length_invoiced_km,
    context=control_objective,
    actual = length_km_installed,
    object_class='Sites',property='Access control measures',
    value='Total Length (km)'),
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Controlling...tput Report',
    service = "Controlling access",
    target_measure = "Number of structures installed",
    measured = number_of_structures_installed,
    invoiced = number_of_structures_installed,
    context=control_objective,
    actual = number_of_structures_installed,
    object_class='Sites',property='Access control measures',
    value='Total Structures'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Pest animal...tput Report')
BR_Data <- load_mult_wbooks(c('M05'), 'Pest animal manag...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Pest animal...tput Report',
    service = "Controlling pest animals",
    target_measure = "Area (ha) treated for pest animals - initial",
    measured = site_calculated_area_ha,
    invoiced = area_ha_treated_for_pest_animals,
    actual = area_ha_treated_for_pest_animals,
    category = initial_or_follow_up_control,
    context = treatment_objective,
    sub_category = 'Initial',
    object_class='Pest Animals',property='Control measures - initial',
    value='Total Area (Ha)'),
  sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Pest animal manag...inal Report',
    service = "Controlling pest animals",
    target_measure = "Area (ha) treated for pest animals - initial",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = site_calculated_area_ha,
    category = initial_or_follow_up_control,
    context = treatment_objective,
    sub_category = 'Initial',
    object_class='Pest Animals',property='Control measures - initial',
    value='Total Area (Ha)'),
  sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Pest animal manag...inal Report',
    service = "Controlling pest animals",
    target_measure = "Area (ha) treated for pest animals - initial",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = site_calculated_area_ha,
    category = initial_or_follow_up_control,
    context = treatment_objective,
    sub_category = 'Initial',
    object_class='Pest Animals',property='Control measures - initial',
    value='Total Area (Ha)'),
  sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Pest animal...tput Report',
    service = "Controlling pest animals",
    target_measure = "Area (ha) treated for pest animals - follow-up",
    measured = site_calculated_area_ha,
    invoiced = area_ha_treated_for_pest_animals,
    actual = area_ha_treated_for_pest_animals,
    category = initial_or_follow_up_control,
    context = treatment_objective,
    sub_category = 'Follow-up',
    species=target_pest_species,
    object_class='Pest Animals',property='Control measures - follow-up',
    value='Total Area (Ha)'),
  sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Pest animal manag...inal Report',
    service = "Controlling pest animals",
    target_measure = "Area (ha) treated for pest animals - follow-up",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = site_calculated_area_ha,
    category = initial_or_follow_up_control,
    context = treatment_objective,
    sub_category = 'Follow-up',
    species=target_pest_species,
    object_class='Pest Animals',property='Control measures - follow-up',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Debris remo...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Debris remo...tput Report',
    service = "Debris removal",
    target_measure = "Area (ha) of debris removal",
    measured = calculated_debris_removed_ha,
    invoiced = area_of_removed_debris_invoiced_ha,
    actual = area_ha_covered_by_debris_removal,
    context = type_of_debris_removed,
    category = initial_or_follow_up_activity,
    object_class='Debris',property='Removal',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Management ...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Management ...tput Report',
    service = "Developing farm/project/site management plan",
    target_measure = "Area (ha) covered by plan",
    measured = calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = area_ha_covered_by_plan_s,
    context= type_of_plan,
    category = are_these_plans_new_or_revised,
    species = species_and_or_threatened_ecological_communities_covered_in_plan,
    object_class='Debris',property='Removal',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Management ...tput Report',
    service = "Developing farm/project/site management plan",
    target_measure = "Number of farm/project/site plans developed",
    measured = number_of_plans_developed,
    invoiced = number_of_plans_developed,
    actual = number_of_plans_developed,
    context = type_of_plan,
    category = are_these_plans_new_or_revised,
    object_class='Debris',property='Removal',
    value='Total Plans'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Erosion Man...tput Report')
BR_Data <- load_mult_wbooks(c('M05'), 'Erosion Managemen...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Erosion Man...tput Report',
    service = "Erosion management",
    target_measure = "Area (ha) of erosion control",
    measured = calculated_area_of_erosion_control_ha,
    invoiced = area_of_erosion_control_invoiced_ha,
    actual = area_ha_benefiting_from_erosion_management,
    context = type_of_treatment_method,
    category = initial_or_follow_up_activity,
    object_class='Debris',property='Removal',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Erosion Managemen...inal Report',
    service = "Erosion management",
    target_measure = "Area (ha) of erosion control",
    measured = calculated_area_of_erosion_control_ha,
    invoiced = area_of_erosion_control_invoiced_ha,
    actual = area_of_erosion_control_ha,
    category = initial_or_follow_up_activity,
    context = erosion_management_method,
    object_class='Erosion',property='Treatment',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Erosion Man...tput Report',
    service = "Erosion management",
    target_measure = "Length (km) of stream/coastline treated for erosion",
    measured = calculated_length_of_erosion_control_km,
    invoiced = length_of_erosion_control_invoiced_km,
    actual = length_km_of_stream_coastline_treated_for_erosion,
    context = type_of_treatment_method,
    category = initial_or_follow_up_activity,
    object_class='Erosion',property='Treatment',
    value='Total Length (km)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Establishin...tput Rep(1)')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Establishin...tput Rep(1)',
    service = "Establishing and maintaining agreements",
    target_measure = "Area (ha) covered by agreements",
    measured = calculated_area_covered_by_agreements_ha,
    invoiced = area_of_covered_by_agreements_invoiced_ha,
    actual = area_ha_covered_by_agreements,
    context = type_of_agreement_s,
    category = established_or_maintained,
    object_class='Agreements',property='Establishing and maintaining',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Establishin...tput Rep(1)',
    service = "Establishing and maintaining agreements",
    target_measure = "Number of agreements",
    measured = number_of_agreements,
    invoiced = number_of_agreements,
    context = type_of_agreement_s,
    actual = number_of_agreements,
    category = established_or_maintained,
    object_class='Agreements',property='Establishing and maintaining',
    value='Total Agreements'),
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Establishin...tput Rep(1)',
    service = "Establishing and maintaining agreements",
    target_measure = "Number of days maintaining agreements",
    measured = number_of_days_maintaining_agreements_if_applicable,
    invoiced = number_of_days_maintaining_agreements_if_applicable,
    actual = number_of_days_maintaining_agreements_if_applicable,
    context = type_of_agreement_s,
    category = established_or_maintained,
    object_class='Agreements',property='Establishing and maintaining',
    value='Total Days'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Establishin...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Establishin...tput Report',
    service = "Establishing and maintaining breeding programs",
    target_measure = "Number of breeding sites and/or populations",
    measured = number_of_breeding_sites_created,
    invoiced = number_of_breeding_sites_created,
    actual = number_of_breeding_sites_created,
    context = technique_of_breeding_program,
    category = ex_situ_in_situ,
    species = targeted_threatened_species,
    object_class='Sites',property='Breeding Programs',
    value='Total Sites'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Establishin...tput Report',
    service = "Establishing and maintaining breeding programs",
    target_measure = "Number of days maintaining breeding programs",
    measured = number_of_days_maintaining_breeding_program,
    invoiced = number_of_days_maintaining_breeding_program,
    actual = number_of_days_maintaining_breeding_program,
    context = technique_of_breeding_program,
    category = ex_situ_in_situ,
    species = targeted_threatened_species,
    object_class='Sites',property='Breeding Programs',
    value='Total Days'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Maintaining...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Maintaining...tput Report',
    service = "Establishing and maintaining feral-free enclosures",
    target_measure = "Area (ha) of feral-free enclosure",
    measured = calculated_area_of_enclosures_ha,
    invoiced = invoiced_area_ha_of_feral_free_enclosures,
    actual = area_ha_of_feral_free_enclosures,
    context = targeted_feral_species_being_controlled,
    category = newly_established_or_maintained_feral_free_enclosure,
    species = targeted_species_being_protected,
    object_class='Feral-free Enclosures',property='Establishing and maintaining',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Maintaining...tput Report',
    service = "Establishing and maintaining feral-free enclosures",
    target_measure = "Number of days maintaining feral-free enclosures",
    measured = number_of_days_maintaining_feral_free_enclosures,
    invoiced = number_of_days_maintaining_feral_free_enclosures,
    actual = number_of_days_maintaining_feral_free_enclosures,                
    context = targeted_feral_species_being_controlled,
    category = newly_established_or_maintained_feral_free_enclosure,
    species = targeted_species_being_protected,
    object_class='Feral-free Enclosures',property='Establishing and maintaining',
    value='Total Days'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Maintaining...tput Report',
    service = "Establishing and maintaining feral-free enclosures",
    target_measure = "Number of feral free enclosures",
    measured = number_of_feral_free_enclosures,
    invoiced = number_of_feral_free_enclosures,
    actual = number_of_feral_free_enclosures,                
    context = targeted_feral_species_being_controlled,
    category = newly_established_or_maintained_feral_free_enclosure,
    species = targeted_species_being_protected,
    object_class='Feral-Free Enclosures',property='Establishing and maintaining',
    value='Total Enclosures'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Establishin...tput Rep(2)')

Report_Raw <- bind_rows(
  Report_Raw,
  sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Establishin...tput Rep(2)',
    service = "Establishing and maintaining monitoring regimes",
    target_measure = "Number of days maintaining monitoring regimes",
    measured = number_of_days_maintaining_monitoring_regimes,
    invoiced = number_of_days_maintaining_monitoring_regimes,
    actual = number_of_days_maintaining_monitoring_regimes,
    context = monitoring_regimes_objective, 
    category = established_or_maintained,
    sub_category = 'Maintained',
    object_class='Monitoring Regimes',property='Establishing and maintaining',
    value='Total Days'),
  sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Establishin...tput Rep(2)',
    service = "Establishing and maintaining monitoring regimes",
    target_measure = "Number of monitoring regimes established",
    measured = number_of_monitoring_regimes,
    invoiced = number_of_monitoring_regimes,
    actual = number_of_monitoring_regimes,
    category = established_or_maintained,
    context = monitoring_regimes_objective,
    sub_category='Established',
    object_class='Monitoring Regimes',property='Establishing and maintaining',
    value='Total Monitoring Regimes'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Farm Manage...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Farm Manage...tput Report',
    service = "Farm management survey",
    target_measure = "Number of farm management surveys conducted",
    measured = number_of_farm_management_surveys_conducted,
    invoiced = number_of_farm_management_surveys_conducted,
    context = survey_purpose,
    actual = number_of_farm_management_surveys_conducted,
    category = baseline_survey_or_indicator_follow_up_survey,
    object_class='Farm Management',property='Surveys',
    value='Total Surveys'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Fauna surve...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Fauna survey Stat...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Fauna surve...tput Report',
    service = "Fauna survey",
    target_measure = "Area surveyed (ha) (fauna)",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_covered_by_fauna_surveys,
    actual = area_ha_covered_by_fauna_surveys,
    category = baseline_survey_or_indicator_follow_up_survey,
    context = survey_technique,
    object_class='Fauna',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Fauna survey Stat...inal Report',
    service= "Fauna survey",
    target_measure = "Area surveyed (ha) (fauna)",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = actual_area_ha_covered_by_fauna_surveys,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    object_class='Fauna',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Fauna surve...tput Report',
    service = "Fauna survey",
    target_measure = "Number of fauna surveys conducted",
    measured = number_of_fauna_surveys_conducted,
    invoiced = number_of_fauna_surveys_conducted,
    actual = number_of_fauna_surveys_conducted,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_species_recorded,
    object_class='Fauna',property='Surveys',
    value='Total Surveys'),
  all_sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Fauna survey Stat...inal Report',
    service= "Fauna survey",
    target_measure = "Number of fauna surveys conducted",
    measured = number_of_fauna_surveys_conducted,
    invoiced = number_of_fauna_surveys_conducted,
    actual = number_of_fauna_surveys_conducted,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_species_recorded,
    object_class='Fauna',property='Surveys',
    value='Total Surveys'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Fire manage...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Fire management S...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,  
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Fire manage...tput Report',
    service = "Fire management actions",
    target_measure = "Area (ha) treated by fire management action",
    measured = calculated_area_treated_ha,
    invoiced = area_invoiced_treated_ha,
    context = type_of_fire_management_action,
    actual = area_ha_treated_by_fire_management_action,
    category = initial_or_follow_up_control,
    object_class='Fire Management',property='Control Measures',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Fire management S...inal Report',
    service = "Fire management actions",
    target_measure = "Area (ha) treated by fire management action",
    measured = calculated_area_treated_ha,
    invoiced = area_invoiced_treated_ha,
    actual = area_ha_protected_by_fire_management_action,
    context = fire_management_type,
    category = initial_or_follow_up_control,
    object_class='Fire Management',property='Control Measures',
    value='Total Area (Ha)')) 

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Flora surve...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Flora survey Stat...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Flora surve...tput Report',
    service = "Flora survey",
    target_measure = "Area surveyed (ha) (flora)",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_covered_by_flora_surveys,
    actual = area_ha_covered_by_flora_surveys,
    category = baseline_survey_or_indicator_follow_up_survey,
    context = survey_technique,
    species = target_species_recorded,
    object_class='Flora',property='Survey',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Flora survey Stat...inal Report',
    service = "Flora survey",
    target_measure = "Area surveyed (ha) (flora)",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = actual_area_ha_covered_by_flora_surveys,
    category = baseline_survey_or_indicator_follow_up_survey,
    context = survey_technique,
    species = target_species_recorded,
    object_class='Flora',property='Survey',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Flora surve...tput Report',
    service = "Flora survey",
    target_measure = "Number of flora surveys conducted",
    measured = number_of_flora_surveys_conducted,
    invoiced = number_of_flora_surveys_conducted,
    actual = number_of_flora_surveys_conducted, 
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_species_recorded,
    object_class='Flora',property='Survey',
    value='Total Surveys'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'Flora survey Stat...inal Report',
    service = "Flora survey",
    target_measure = "Number of flora surveys conducted",
    measured = number_of_flora_surveys_conducted,
    invoiced = number_of_flora_surveys_conducted,
    actual = number_of_flora_surveys_conducted,
    category = baseline_survey_or_indicator_follow_up_survey,
    context = survey_technique,
    species = target_species_recorded,
    object_class='Flora',property='Survey',
    value='Total Surveys')) 

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Habitat aug...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Habitat augmentat...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Habitat aug...tput Report',
    service = "Habitat augmentation",
    target_measure = "Area (ha) of augmentation",
    measured = calculated_area_augmented_ha,
    invoiced = area_invoiced_aumentation_ha,
    actual = area_ha_of_augmentation,
    context = type_of_habitat_augmentation_installed,
    category = initial_or_follow_up_control,
    object_class='Habitat',property='Augmentation',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Habitat augmentat...inal Report',
    service = "Habitat augmentation",
    target_measure = "Area (ha) of augmentation",
    measured = calculated_area_augmented_ha,
    invoiced = area_invoiced_aumentation_ha,
    actual = area_augmented_ha,
    context = habitat_augmentation_type,
    category = initial_or_follow_up_control,
    object_class='Habitat',property='Augmentation',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Habitat aug...tput Report',
    service = "Habitat augmentation",
    target_measure = "Number of structures or installations",
    measured = number_of_structures_installed,
    invoiced = number_of_structures_installed,
    actual = number_of_structures_installed,
    context = type_of_habitat_augmentation_installed,
    category = initial_or_follow_up_control,
    object_class='Habitat',property='Augmentation',
    value='Total Structures'),
  all_sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Habitat augmentat...inal Report',
    service = "Habitat augmentation",
    target_measure = "Number of structures or installations",
    measured = number_of_structures_installed,
    invoiced = number_of_structures_installed,
    actual = number_of_structures_installed,
    context = habitat_augmentation_type,
    category = initial_or_follow_up_control,
    object_class='Habitat',property='Augmentation',
    value='Total Structures'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Identifying...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Identifying sites...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Identifying...tput Report',
    service = "Identifying the location of potential sites",
    target_measure = "Number of potential sites identified",
    measured = number_of_potential_sites_identified,
    invoiced = number_of_potential_sites_identified,
    context = what_have_these_sites_been_identified_for,
    actual = number_of_potential_sites_identified,
    object_class='Sites',property='Identification',
    value='Total Sites'),
  no_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Identifying sites...inal Report',
    service = "Identifying the location of potential sites",
    target_measure = "Number of potential sites identified",
    measured = number_of_potential_sites_identified,
    invoiced = number_of_potential_sites_identified,
    actual = number_of_potential_sites_identified, 
    context = what_have_these_sites_been_identified_for,
    object_class='Sites',property='Identification',
    value='Total Sites'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Improving h...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Improving h...tput Report',
    service = "Improving hydrological regimes",
    target_measure = "Number of treatments implemented to improve water management",
    measured = number_of_treatments_implemented_to_improve_water_management,
    invoiced = number_of_treatments_implemented_to_improve_water_management,
    context = type_of_treatment_implemented_to_improve_water_management,
    actual = number_of_treatments_implemented_to_improve_water_management,
    category = installed_or_maintained,
    object_class='Hydrological Regimes',property='Treatments',
    value='Total Treatments'),
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Improving h...tput Report',
    service = "Improving hydrological regimes",
    target_measure = "Area (ha) of catchment being managed as a result of this management action",
    measured = calculated_area_covering_regime_change_ha,
    invoiced = area_invoiced_ha,
    context = type_of_treatment_implemented_to_improve_water_management,
    actual = area_ha_covering_the_hydrological_regime_change,
    category = installed_or_maintained,
    object_class='Hydrological Regimes',property='Treatments',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Improving l...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Improving l...tput Report',
    service = "Improving land management practices",
    target_measure = "Area (ha) covered by practice change",
    measured = calculated_area_implemented_ha,
    invoiced = area_implemented_invoiced_ha,
    context = type_of_action,
    actual = area_ha_benefitting_from_practice_change,
    category = initial_or_follow_up_control,
    object_class='Land',property='Practice Change',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Disease man...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Disease managemen...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Disease man...tput Report',
    service = "Managing disease",
    target_measure = "Area (ha) treated for disease",
    measured = calculated_area_treated_ha,
    invoiced = area_treated_invoiced_ha,
    context = management_method_treatment_objective,
    actual = area_ha_treated_for_disease,
    category = initial_or_follow_up_treatment,
    object_class='Disease',property='Treatment',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Disease managemen...inal Report',
    service = "Managing disease",
    target_measure = "Area (ha) treated for disease",
    measured = calculated_area_treated_ha,
    invoiced = area_treated_invoiced_ha,
    actual = area_treated_ha,
    context = management_method,
    category = initial_or_follow_up_treatment,
    object_class='Disease',property='Treatment',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Negotiation...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Negotiations Stat...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Negotiation...tput Report',
    service = "Negotiating with the Community, Landholders, Farmers, Traditional Owner groups, Agriculture industry groups etc.",
    target_measure = "Number of groups negotiated with",
    measured = groups_negotiated_with,
    invoiced = groups_negotiated_with, 
    context = which_sector_does_the_group_belong_to,
    actual = groups_negotiated_with,
    object_class='Groups',property='Negotiations',
    value='Total Groups'),
  no_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Negotiations Stat...inal Report',
    service = "Negotiating with the Community, Landholders, Farmers, Traditional Owner groups, Agriculture industry groups etc.",
    target_measure = "Number of groups negotiated with",
    measured = groups_negotiated_with,
    invoiced = groups_negotiated_with,
    actual = groups_negotiated_with,
    context = which_sector_does_the_group_belong_to,
    object_class='Groups',property='Negotiations',
    value='Total Groups'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Obtaining a...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Obtaining approva...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Obtaining a...tput Report',
    service = "Obtaining relevant approvals",
    target_measure = "Number of relevant approvals obtained",
    measured = number_of_relevant_approvals_obtained,
    invoiced = number_of_relevant_approvals_obtained,
    actual = number_of_relevant_approvals_obtained,
    context = what_were_these_approvals_obtained_for,
    object_class='Approvals',property='Processed',
    value='Total Approvals'),
  no_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Obtaining approva...inal Report',
    service = "Obtaining relevant approvals",
    target_measure = "Number of relevant approvals obtained",
    measured = number_of_relevant_approvals_obtained,
    invoiced = number_of_relevant_approvals_obtained,
    actual = number_of_relevant_approvals_obtained,
    context = what_were_these_approvals_obtained_for,
    object_class='Approvals',property='Processed',
    value='Total Approvals'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Pest animal...tput Rep(1)')
BR_Data <- load_mult_wbooks(c('M05'),'Pest animal surve...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Pest animal...tput Rep(1)',
    service = "Pest animal survey",
    target_measure = "Area (ha) surveyed for pest animals",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_surveyed_for_pest_animals,
    actual = area_ha_surveyed_for_pest_animals,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_species_recorded,
    object_class='Pests',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Pest animal surve...inal Report',
    service = "Pest animal survey",
    target_measure = "Area (ha) surveyed for pest animals",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = actual_area_ha_surveyed_for_pest_animals,
    context=survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_species_recorded,
    object_class='Pests',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Pest animal...tput Rep(1)',
    service = "Pest animal survey",
    target_measure = "Number of pest animal surveys conducted",
    measured = number_of_surveys_conducted,
    invoiced = number_of_surveys_conducted,
    actual = number_of_surveys_conducted,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_species_recorded,
    object_class='Pests',property='Surveys',
    value='Total Surveys'),
  all_sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Pest animal surve...inal Report',
    service = "Pest animal survey",
    target_measure = "Number of pest animal surveys conducted",
    measured = number_of_surveys_conducted,
    invoiced = number_of_surveys_conducted,
    actual = number_of_surveys_conducted,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_species_recorded,
    object_class='Pests',property='Surveys',
    value='Total Surveys'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Plant survi...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Plant survi...tput Report',
    service = "Plant survival survey",
    target_measure = "Area surveyed (ha) for plant survival",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_surveyed_for_plant_survival,
    actual = area_ha_surveyed_for_plant_survival,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = species_recorded,
    object_class='Plants',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Plant survi...tput Report',
    service = "Plant survival survey",
    target_measure = "Number of plant survival surveys conducted",
    measured = number_of_plant_survival_surveys_conducted,
    invoiced = number_of_plant_survival_surveys_conducted,
    actual = number_of_plant_survival_surveys_conducted,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = species_recorded,
    object_class='Plants',property='Surveys',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Project pla...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Project planning ...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Project pla...tput Report',
    service = "Project planning and delivery of documents as required for the delivery of the Project Services and monitoring",
    target_measure = "Number of planning and delivery documents for delivery of the project services and monitoring",
    measured = number_of_planning_and_delivery_documents_for_delivery_of_the_project_services_and_monitoring,
    invoiced = number_of_planning_and_delivery_documents_for_delivery_of_the_project_services_and_monitoring,
    actual = number_of_planning_and_delivery_documents_for_delivery_of_the_project_services_and_monitoring,
    context = purpose_of_these_documents,
    object_class='Documents',property='Project Planning',
    value='Total Documents'),
  no_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Project pla...tput Report',
    service = "Project planning and delivery of documents as required for the delivery of the Project Services and monitoring",
    target_measure = "Number of days project planning / preparation",
    measured = number_of_days_administering_project_plans_delivery_documents,
    invoiced = number_of_days_administering_project_plans_delivery_documents,
    actual = number_of_days_administering_project_plans_delivery_documents,
    context = purpose_of_these_documents,
    object_class='Documents',property='Project Planning',
    value='Total Days'),
  no_category_extract_context_no_species(
    Data=BR_Data,
    worksheet = 'Project planning ...inal Report',
    service = "Project planning and delivery of documents as required for the delivery of the Project Services and monitoring",
    target_measure = "Number of planning and delivery documents for delivery of the project services and monitoring",
    measured = number_of_planning_and_delivery_documents_for_delivery_of_the_project_and_monitoring,
    invoiced = number_of_planning_and_delivery_documents_for_delivery_of_the_project_and_monitoring,
    actual = number_of_planning_and_delivery_documents_for_delivery_of_the_project_and_monitoring,
    context = purpose_of_these_documents,
    object_class='Documents',property='Project Planning',
    value='Total Documents'),
  no_category_extract_no_context_no_species(
    Data=BR_Data,
    worksheet = 'Project planning ...inal Report',
    service = "Project planning and delivery of documents as required for the delivery of the Project Services and monitoring",
    target_measure = "Number of days project planning / preparation",
    measured = number_of_days_administering_project_plans_delivery_documents,
    invoiced = number_of_days_administering_project_plans_delivery_documents,
    actual = number_of_days_administering_project_plans_delivery_documents,
    object_class='Documents',property='Project Planning',
    value='Total Days'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Remediating...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Remediating...tput Report',
    service = "Remediating riparian and aquatic areas",
    target_measure = "Area (ha) remediated",
    measured = calculated_area_remediated_ha,
    invoiced = area_remediated_invoiced_ha,
    actual = area_ha_being_remediated,
    context = type_of_remediation,
    category = initial_followup_control,
    object_class='Riparian and Aquatic Areas',property='Remediation',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Remediating...tput Report',
    service = "Remediating riparian and aquatic areas",
    target_measure = "Length (km) remediated",
    measured = calculated_length_remediated_km,
    invoiced = length_remediated_invoiced_km,
    context = type_of_remediation,
    actual = length_remediated_invoiced_km,
    category = initial_followup_control,
    object_class='Riparian and Aquatic Areas',property='Remediation',
    value='Total Length (km)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Weed treatm...tput Report')
BR_Data <- load_mult_wbooks(c('M05'), 'Weed treatment St...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Weed treatm...tput Report',
    service = "Removing weeds",
    target_measure = "Area (ha) treated for weeds - initial",
    measured = site_calculated_area_ha,
    invoiced = area_ha_treated_for_weed_removal,
    actual = area_ha_treated_for_weed_removal,
    category = initial_or_follow_up_treatment,
    sub_category = 'Initial',
    context=treatment_objective,
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Initial',
    value='Total Area (Ha)'),
  sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Weed treatm...tput Report',
    service = "Removing weeds",
    target_measure = "Area (ha) treated for weeds - follow-up",
    measured = site_calculated_area_ha,
    invoiced = area_ha_treated_for_weed_removal,
    actual = area_ha_treated_for_weed_removal,
    category = initial_or_follow_up_treatment,
    sub_category = 'Follow-up',
    context=treatment_objective,
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Follow-up',
    value='Total Area (Ha)'),
  sub_category_extract_no_context_species(
    Data = BR_Data,
    worksheet = 'Weed treatment St...inal Report',
    service = "Removing weeds",
    target_measure = "Area (ha) treated for weeds - initial",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = area_invoiced_ha,
    category = initial_or_follow_up_treatment,
    sub_category = 'Initial',
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Initial',
    value='Total Area (Ha)'),
  sub_category_extract_no_context_species(
    Data=BR_Data,
    worksheet = 'Weed treatment St...inal Report',
    service = "Removing weeds",
    target_measure = "Area (ha) treated for weeds - follow-up",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = area_invoiced_ha,
    category = initial_or_follow_up_treatment,
    sub_category = 'Follow-up',
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Follow-up',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Weed treatm...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Weed treatm...tput Report',
    service = "Removing weeds",
    target_measure = "Length (km) treated for weeds - follow-up",
    measured = site_calculated_length_km,
    invoiced = length_invoiced_km,
    actual = length_km_treated_for_weed_removal,
    category = initial_or_follow_up_treatment,
    context = type_of_treatment,
    sub_category = 'Follow-up',
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Follow-up',
    value='Total Length (km)'),
  sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Weed treatm...tput Report',
    service = "Removing weeds",
    target_measure = "Length (km) treated for weeds - initial",
    measured = site_calculated_length_km,
    invoiced = length_invoiced_km,
    actual = length_km_treated_for_weed_removal,
    category = initial_or_follow_up_treatment,
    context = type_of_treatment,
    sub_category = 'Initial',
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Initial',
    value='Total Length (km)'),
  sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Weed treatment St...inal Report',
    service = "Removing weeds",
    target_measure = "Length (km) treated for weeds - follow-up",
    measured = site_calculated_length_km,
    invoiced = length_invoiced_km,
    actual = length_treated_km,
    category = initial_or_follow_up_treatment,
    context = type_of_treatment,
    sub_category = 'Follow-up',
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Follow-up',
    value='Total Length (km)'),
  sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Weed treatment St...inal Report',
    service = "Removing weeds",
    target_measure = "Length (km) treated for weeds - initial",
    measured = site_calculated_length_km,
    invoiced = length_invoiced_km,
    actual = length_treated_km,
    category = initial_or_follow_up_treatment,
    context = type_of_treatment,
    sub_category = 'Initial',
    species = target_weed_species,
    object_class='Weeds',property='Treatment - Initial',
    value='Total Length (km)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Revegetatin...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Revegetating habi...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Revegetatin...tput Report',
    service = "Revegetating habitat",
    target_measure = "Area (ha) of revegetated habitat maintained",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_of_habitat_revegetated,
    actual = area_ha_of_habitat_revegetated,
    context = planting_method,
    category = initial_or_maintenance_activity,
    sub_category = 'Maintenance',
    species = species,
    object_class='Habitat',property='Revegetation - Maintenance',
    value='Total Area (Ha)'),
  sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Revegetatin...tput Report',
    service = "Revegetating habitat",
    target_measure = "Area of habitat revegetated (ha)",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_of_habitat_revegetated,
    actual = area_ha_of_habitat_revegetated,
    context = planting_method,
    category = initial_or_maintenance_activity,
    sub_category = 'Initial',
    species = species,
    object_class='Habitat',property='Revegetation - Initial',
    value='Total Area (Ha)'),
  sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Revegetating habi...inal Report',
    service = "Revegetating habitat",
    target_measure = "Area (ha) of revegetated habitat maintained",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    context = planting_method,
    actual = area_invoiced_ha,
    category = initial_or_maintenance_activity,
    sub_category = 'Maintenance',
    species = species,
    object_class='Habitat',property='Revegetation - Maintenance',
    value='Total Area (Ha)'),
  sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Revegetating habi...inal Report',
    service = "Revegetating habitat",
    target_measure = "Area of habitat revegetated (ha)",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = area_invoiced_ha,
    context = planting_method,
    category = initial_or_maintenance_activity,
    sub_category = 'Initial',
    species = species,
    object_class='Habitat',property='Revegetation - Initial',
    value='Total Area (Ha)'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Revegetatin...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Revegetatin...tput Report',
    service = "Revegetating habitat",
    target_measure = "Number of days collecting seed",
    measured = number_of_days_collecting_seed,
    invoiced = number_of_days_collecting_seed,
    context = planting_method,
    actual = number_of_days_collecting_seed,
    category = initial_or_maintenance_activity,
    species = species,
    object_class='Habitat',property='Seed Collection',
    value='Total Days'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Revegetatin...tput Report',
    service = "Revegetating habitat",
    target_measure = "Number of days propagating plants",
    measured = number_of_days_propagating_plants,
    invoiced = number_of_days_propagating_plants,
    actual = number_of_days_propagating_plants,
    context = planting_method,
    category = initial_or_maintenance_activity,
    species = species,
    object_class='Habitat',property='Propagation',
    value='Total Days'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Site prepar...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  no_category_extract_context_no_species(
    Data = RLP_Data,
    worksheet = 'RLP - Site prepar...tput Report',
    service = "Developing farm/project/site management plan",
    target_measure = "Area (ha) covered by plan",
    measured = calculated_area_prepared_ha,
    invoiced = area_prepared_invoiced_ha,
    actual = area_ha_of_the_site_preparation,
    context=type_of_action,
    object_class='Plans',property='Development',
    value='Total Area (Ha)'),
  no_category_extract_context_no_species(
    Data = RLP_Data,
    worksheet = 'RLP - Site prepar...tput Report',
    service = "Developing farm/project/site management plan",
    target_measure = "Number of days preparing site/s",
    measured = number_of_days_in_preparing_site,
    invoiced = number_of_days_in_preparing_site,
    actual = number_of_days_in_preparing_site,
    context=type_of_action,
    object_class='Plans',property='Development',
    value='Total Days'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Skills and ...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data = RLP_Data,
    worksheet = 'RLP - Skills and ...tput Report',
    service = "Skills and knowledge survey",
    target_measure = "Number of skills and knowledge surveys conducted",
    measured = number_of_skills_and_knowledge_surveys_conducted,
    invoiced = number_of_skills_and_knowledge_surveys_conducted,
    actual = number_of_skills_and_knowledge_surveys_conducted,
    category = baseline_survey_or_indicator_follow_up_survey,
    context=survey_technique,
    object_class='Skills and knowledge',property='Surveys',
    value='Total Surveys'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Soil testin...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_no_species(
    Data = RLP_Data,
    worksheet = 'RLP - Soil testin...tput Report',
    service = "Soil testing",
    target_measure = "Number of soil tests conducted in targeted areas",
    measured = number_of_soil_tests_conducted_in_targeted_areas,
    invoiced = number_of_soil_tests_conducted_in_targeted_areas,
    actual = number_of_soil_tests_conducted_in_targeted_areas,
    category = initial_or_follow_up_activity,
    context=testing_technique,
    object_class='Soil',property='Testing',
    value='Total Tests'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Emergency I...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Emergency Interve...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data = RLP_Data,
    worksheet = 'RLP - Emergency I...tput Report',
    service = "Undertaking emergency interventions to prevent extinctions",
    target_measure = "Number of interventions",
    measured = number_of_interventions,
    invoiced = number_of_interventions,
    actual = number_of_interventions,
    category = initial_or_follow_up_activity,
    context = type_and_goal_or_intervention,
    species = targeted_species,
    object_class='Species and Habitat',property='Emergency Interventions',
    value='Total Interventions'),
  all_sub_category_extract_context_species(
    Data = BR_Data,
    worksheet = 'Emergency Interve...inal Report',
    service = "Undertaking emergency interventions to prevent extinctions",
    target_measure = "Number of interventions",
    measured = number_of_interventions,
    invoiced = number_of_interventions,
    actual = number_of_interventions,
    category = initial_or_follow_up_activity,
    context = type_and_goal_or_intervention,
    species = targeted_species,
    object_class='Species and Habitat',property='Emergency Interventions',
    value='Total Interventions'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Water quali...tput Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_no_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Water quali...tput Report',
    service = "Water quality survey",
    target_measure = "Area (ha) surveyed for water quality",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_covered_by_water_quality_surveys,
    actual = area_ha_covered_by_water_quality_surveys,
    category = baseline_survey_or_indicator_follow_up_survey,
    object_class='Water Quality',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_no_context_no_species(
    Data=RLP_Data,
    worksheet = 'RLP - Water quali...tput Report',
    service = "Water quality survey",
    target_measure = "Number of water quality surveys",
    measured = number_of_water_quality_surveys_conducted,
    invoiced = number_of_water_quality_surveys_conducted,
    actual = number_of_water_quality_surveys_conducted,
    category = baseline_survey_or_indicator_follow_up_survey,
    object_class='Water Quality',property='Surveys',
    value='Total Surveys'))

RLP_Data <- load_mult_wbooks(c('M02','M05','M07','M08','M09'),
                             'RLP - Weed distri...tput Report')
BR_Data <- load_mult_wbooks(c('M05'),'Weed distribution...inal Report')

Report_Raw <- bind_rows(
  Report_Raw,
  all_sub_category_extract_context_species(
    Data = RLP_Data,
    worksheet = 'RLP - Weed distri...tput Report',
    service = "Weed distribution survey",
    target_measure = "Area (ha) surveyed for weeds",
    measured = site_calculated_area_ha,
    invoiced = invoiced_area_ha_surveyed_for_weed_distribution,
    actual = area_ha_surveyed_for_weed_distribution,
    category = baseline_survey_or_indicator_follow_up_survey,
    context = survey_technique,
    species = target_weed_species_recorded,
    object_class='Weeds',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Weed distribution...inal Report',
    service = "Weed distribution survey",
    target_measure = "Area (ha) surveyed for weeds",
    measured = site_calculated_area_ha,
    invoiced = area_invoiced_ha,
    actual = actual_area_ha_surveyed_for_weed_distribution,
    category = baseline_survey_or_indicator_follow_up_survey,
    context = survey_technique,
    species = target_weed_species_recorded,
    object_class='Weeds',property='Surveys',
    value='Total Area (Ha)'),
  all_sub_category_extract_context_species(
    Data=BR_Data,
    worksheet = 'Weed distribution...inal Report',
    service = "Weed distribution survey",
    target_measure = "Number of weed distribution surveys conducted",
    measured = number_of_weed_distribution_surveys_conducted,
    invoiced = number_of_weed_distribution_surveys_conducted,
    actual = number_of_weed_distribution_surveys_conducted,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_weed_species_recorded,
    object_class='Weeds',property='Surveys',
    value='Total Surveys'),
  all_sub_category_extract_context_species(
    Data=RLP_Data,
    worksheet = 'RLP - Weed distri...tput Report',
    service = "Weed distribution survey",
    target_measure = "Number of weed distribution surveys conducted",
    measured = number_of_weed_distribution_surveys_conducted,
    invoiced = number_of_weed_distribution_surveys_conducted,
    actual = number_of_weed_distribution_surveys_conducted,
    context = survey_technique,
    category = baseline_survey_or_indicator_follow_up_survey,
    species = target_weed_species_recorded,
    object_class='Weeds',property='Surveys',
    value='Total Surveys'))

# Grant Activities
Data <- load_mult_wbooks(c('M03','M04','M06','M07','M10','M11'),
                         'Debris Removal De...ris Removal')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data=Data,
    sheet_name='Debris Removal De...ris Removal',
    measured_col=area_covered_by_this_activity_ha,
    actual_col=area_covered_by_this_activity_ha,
    invoiced_col=area_covered_by_this_activity_ha,
    context_col= type_of_material_removed,
    object_class='Debris',property='Removal',
    value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M06','M07','M10','M11'),
                         'Revegetation Deta...evegetation')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species(
    Data = Data,
    sheet_name='Revegetation Deta...evegetation',
    measured_col=area_of_revegetation_works_ha,
    actual_col=area_of_revegetation_works_ha,
    invoiced_col=area_of_revegetation_works_ha,
    context_col= revegetation_method,
    species = species,
    object_class='Habitat',property='Revegetation',
    value='Total Area (Ha)'),
  grant_report_species(
    Data = Data,
    sheet_name='Revegetation Deta...evegetation',
    measured_col=no_planted,
    actual_col=no_planted,
    invoiced_col=no_planted,
    context_col= mature_height,
    species = species,
    object_class='Habitat',property='Revegetation',
    value='Total Trees'))

Data <- load_mult_wbooks(c('M03','M04','M06','M11'),
                         'Disease Managemen... Management')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data=Data,
    sheet_name='Disease Managemen... Management',
    measured_col=area_quarantined_treated_ha,
    actual_col=area_quarantined_treated_ha,
    invoiced_col=area_quarantined_treated_ha,
    context_col= disease_management_purpose,
    object_class='Disease',property='Treatment',
    value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M06','M07','M10','M11'),
                         'Erosion Managemen... Management')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data=Data,
    sheet_name='Erosion Managemen... Management',
    measured_col=area_of_erosion_being_treated,
    actual_col=area_of_erosion_being_treated,
    invoiced_col=area_of_erosion_being_treated,
    context_col= area_of_erosion_on_this_site_ha,
    object_class='Erosion',property='Treatment',
    value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M07','M11'),
                         'Conservation Grazing Management')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data=Data,
    sheet_name='Conservation Grazing Management',
    measured_col=area_managed_ha,
    actual_col=area_managed_ha,
    invoiced_col=area_managed_ha,
    context_col= comments_notes,
    object_class='Conservation Grazing',property='Management',
    value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M07','M10','M11'),
                         'Plan Development ...Development')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data ,
    sheet_name='Plan Development ...Development',
    measured_col=area_of_plan_coverage_km2,
    actual_col=area_of_plan_coverage_km2,
    invoiced_col=area_of_plan_coverage_km2,
    context_col= type_of_planning_being_undertaken,
    object_class='Plans',property='Development',
    value='Total Area (km2)'))

Data <- load_mult_wbooks(c('M03','M04','M06','M10','M11'),
                         'Fire Management D... Management')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data,sheet_name='Fire Management D... Management',
    measured_col=actual_burnt_area_ha,actual_col=actual_burnt_area_ha,
    invoiced_col=actual_burnt_area_ha,context_col= type_of_event,
    object_class='Fire Management',property='Control Measures',
    value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M07','M10','M11'),
                         'Management Practice Change')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data,
    sheet_name='Management Practice Change',
    measured_col=area_covered_by_practice_change_ha,
    actual_col=area_covered_by_practice_change_ha,
    invoiced_col=area_covered_by_practice_change_ha,
    context_col= industry,object_class='Land',
    property='Practice Change',value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M06','M07','M10','M11'),
                         'Pest Management D... Management')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species(
    Data = Data,
    sheet_name='Pest Management D... Management',
    measured_col=total_treatment_area_ha,
    actual_col=total_treatment_area_ha,
    invoiced_col=total_treatment_area_ha,
    context_col= pest_management_method,
    species = target_species, object_class='Pest Animals',
    property='Control measures',value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M06','M07','M10','M11'),
                         'Fence Details Pest Management')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data,
    sheet_name='Fence Details Pest Management',
    measured_col=area_protected_by_erected_fence_ha,
    actual_col=area_protected_by_erected_fence_ha,
    invoiced_col=area_protected_by_erected_fence_ha,
    context_col= fence_type,
    object_class='Fences',property='Access control measures',
    value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M03','M04','M06','M07','M10','M11'),
                         'Access Control De...rastructure')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data,
    sheet_name='Access Control De...rastructure',
    measured_col=area_ha_protected_by_access_management_structure_s,
    actual_col=area_ha_protected_by_access_management_structure_s,
    invoiced_col=area_ha_protected_by_access_management_structure_s,
    context_col= description_of_issue_s_requiring_access_management,
    object_class='Infrastructure',property='Access control measures',
    value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M04','M10','M11'),'Post revegetation... management')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data,sheet_name='Post revegetation... management',
    measured_col=total_area_managed_ha,actual_col=total_area_managed_ha,
    invoiced_col=total_area_managed_ha,context_col= total_area_managed_ha,
    object_class='Sites',property='Revegetation',value='Total Area (Ha)'))

Data <- load_mult_wbooks(c('M04','M10','M11'),'Post revegetation... managem(1)')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data,sheet_name='Post revegetation... managem(1)',
    measured_col=area_managed_ha,actual_col=area_managed_ha,
    invoiced_col=area_managed_ha,context_col= comments_notes,
    object_class='Sites',property='Post Revegetation',
    value='Area (Ha)'))

Data <- load_mult_wbooks(c('M04','M10','M11'),'Post revegetation... managem(3)')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_no_species(
    Data = Data,sheet_name='Post revegetation... managem(3)',
    measured_col=total_pest_treatment_area_ha,
    actual_col=total_pest_treatment_area_ha,
    invoiced_col=total_pest_treatment_area_ha,
    context_col= type_of_pest_treatment_event,
    object_class='Sites',property='Post Revegetation',
    value='Total Area (Ha)'))

BR_Data <- load_mult_wbooks(c('M05'),'Wildlife rescue f...eport - (1)')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,sheet_name='Wildlife rescue f...eport - (1)',
    species_col= species_benefiting_by_facility_or_equipment,
    context_col= name_of_facility_equipment_type_if_applicable,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

BR_Data <- load_mult_wbooks(c('M05'),'Emergency interve...eport - (1)')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,
    sheet_name='Emergency interve...eport - (1)',
    species_col= target_species,
    context_col= intervention_activity,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

BR_Data <- load_mult_wbooks(c('M05'),'Native wildlife r...eport - (1)')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,
    sheet_name='Native wildlife r...eport - (1)',
    species_col= target_species,
    context_col= rescue_location_s,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

BR_Data <- load_mult_wbooks(c('M05'),'Supplementary foo...eport - (1)')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,
    sheet_name='Supplementary foo...eport - (1)',
    species_col= target_species,
    context_col= location_s_of_food_and_water_provisions,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

BR_Data <- load_mult_wbooks(c('M05'),'Wildlife rescue f...eport - WRR')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,
    sheet_name='Wildlife rescue f...eport - WRR',
    species_col= species_benefiting_by_facility_or_equipment,
    context_col= name_of_facility_equipment_type_if_applicable,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

BR_Data <- load_mult_wbooks(c('M05'),'Emergency interve...eport - WRR')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,
    sheet_name='Emergency interve...eport - WRR',
    species_col= target_species,
    context_col= location_s_of_intervention_activity,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

BR_Data <- load_mult_wbooks(c('M05'),'Supplementary foo...eport - WRR')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,
    sheet_name='Supplementary foo...eport - WRR',
    species_col= target_species,
    context_col= location_s_of_food_and_water_provisions,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

BR_Data <- load_mult_wbooks(c('M05'),'Native wildlife r...eport - WRR')

Report_Raw <- bind_rows(
  Report_Raw,
  grant_report_species_no_metrics(
    Data=BR_Data,
    sheet_name='Native wildlife r...eport - WRR',
    species_col= target_species,
    context_col= rescue_location_s,
    object_class='Sites',property='Wildlife rescue',
    value='Species'))

projects_reports <- 
  Report_Raw %>%
  mutate(total_to_be_delivered = ifelse(!is.na(total_to_be_delivered),
                                        total_to_be_delivered,0),
         actual = ifelse(is.na(actual),measured,actual),
         across(c('total_to_be_delivered','measured','invoiced','actual'),
                as.numeric),
         external_id=as.character(external_id),
         extract_date=extract_date,
         MERIT_Reports_link = 
           str_c("https://fieldcapture.ala.org.au/project/index/",
                 project_id)) %>%
  #mutate(proportion = measured/total_to_be_delivered) %>%
  rename(project_status=status, status=status_2, 
         report_last_modified=last_modified_2,
         report_stage = stage,report_activity_type = activity_type,
         project_start_date=start_date,project_end_date=end_date,
         project_contracted_start_date=contracted_start_date,
         project_contracted_end_date=contracted_end_date,
         project_name=name) %>%
  filter(report_status=='Approved', status=='finished') %>%
  mutate(meta_col_project_status='status',
         meta_col_status='status_2',
         meta_col_report_last_modified='last_modified_2',
         meta_col_report_stage='stage',
         meta_col_report_activity_type='activity_type',
         meta_col_project_start_date='start_date',
         meta_col_project_end_date='end_date',
         meta_col_project_contracted_start_date='contracted_start_date',
         meta_col_project_contracted_end_date='contracted_end_date',
         meta_col_project_name='name') %>%
  select(-project_id,-activity_id,-meta_col_status,-description)  %>%
  select(any_of(project_cols_out),any_of(report_cols_out),
         any_of(project_meta_cols_out),any_of(report_meta_cols_out),
         any_of(extract_date_cols)) %>% distinct()
# 193915 > 183066 distinct rows must some dups in there so distinct it
RLP_Outcomes <- read.xlsx(paste('M01 ',extract_date,'.xlsx',sep=''), 
                          sheet='RLP Outcomes',
                          startRow = 1) %>%
  clean_names() %>% 
  select(grant_id,type_of_outcomes,outcome,investment_priority) 

primary_secondary_outcomes <- RLP_Outcomes %>% 
  filter(type_of_outcomes %in% c('Primary outcome','Secondary Outcome/s'),
         !is.na(outcome),outcome!='null') %>%
  select(grant_id,outcome) %>%
  group_by(grant_id) %>%
  distinct() %>%
  summarise(primary_secondary_outcomes = str_c(outcome,collapse="|")) %>% 
  ungroup() 

primary_outcomes <- RLP_Outcomes %>% 
  filter(type_of_outcomes == 'Primary outcome',!is.na(outcome),
         outcome!='null') %>%
  select(grant_id,outcome) %>%
  group_by(grant_id) %>%
  distinct() %>%
  summarise(primary_outcomes = str_c(outcome,collapse="|")) %>% 
  ungroup() 

secondary_outcomes <- RLP_Outcomes %>% 
  filter(type_of_outcomes == 'Secondary Outcome/s',!is.na(outcome),
         outcome!='null') %>%
  select(grant_id,outcome) %>%
  group_by(grant_id) %>%
  distinct() %>%
  summarise(secondary_outcomes = str_c(outcome,collapse="|")) %>% 
  ungroup() 

primary_secondary_investment_priorities <- RLP_Outcomes %>% 
  filter(type_of_outcomes %in% c('Primary outcome','Secondary Outcome/s'),
         investment_priority !='NA') %>% 
  select(grant_id,investment_priority) %>%
  group_by(grant_id) %>%
  distinct() %>%
  summarise(primary_secondary_investment_priorities = str_c(investment_priority,
                                                            collapse="|")) %>% 
  ungroup() 

primary_investment_priority <- RLP_Outcomes %>% 
  filter(type_of_outcomes == 'Primary outcome',investment_priority !='NA') %>% 
  select(grant_id,primary_investment_priority=investment_priority) 

secondary_investment_priority <- RLP_Outcomes %>% 
  filter(type_of_outcomes == 'Secondary Outcome/s',
         investment_priority !='NA') %>% 
  select(grant_id,investment_priority) %>%
  group_by(grant_id) %>%
  distinct() %>%
  summarise(secondary_investment_priority = str_c(investment_priority,
                                                  collapse="|")) %>% 
  ungroup() 

project_assets <- read.xlsx(paste('M01 ',extract_date,'.xlsx',sep=''),
                            sheet='MERI_Project Assets',
                            startRow = 1) %>%
  clean_names() %>%
  select(grant_id,asset) %>%
  filter(asset!='NA') %>%
  group_by(grant_id) %>%
  summarise(assets = str_c(asset,collapse = "|")) %>%
  ungroup()

meri_outcomes_indicators <- read.xlsx(paste('M01 ',extract_date,'.xlsx',sep=''),
                                      sheet='MERI_Outcomes') %>% 
  clean_names() %>% 
  select(grant_id,all_of(meri_outcomes_indicator_ref)) %>%
  group_by(grant_id) %>%
  summarize(across(all_of(meri_outcomes_indicator_ref),last))

meri_priorities <- read.xlsx(paste('M01 ',extract_date,'.xlsx',sep=''),
                             sheet='MERI_Priorities') %>% 
  clean_names() %>%
  mutate(across(ends_with('_date'),as.Date,origin='1899-12-30')) %>%
  select(grant_id,document_name,relevant_section,explanation_of_strategic_alignment) %>%
  mutate(documents_priority=str_c("name: ",document_name,' section: ',relevant_section,
                                  ' alignment: ',explanation_of_strategic_alignment)) %>%
  select(grant_id,documents_priority) %>%
  drop_na(documents_priority) %>%
  distinct() %>%
  group_by(grant_id) %>%
  summarize(documents_priority=str_c(documents_priority,collapse="|")) %>%
  ungroup()

report_species <- projects_reports_species %>%
  filter(!is.na(report_species)) %>%
  separate_rows(report_species,sep='[,|]') %>%
  select(grant_id,report_species) %>%
  group_by(grant_id) %>%
  summarize(report_species=str_c(str_trim(report_species),collapse="|")) %>%
  ungroup()

# load("sprat_lookup.Rdata")
# col_by_grant_id <- function(Data,col) {
#   fred <- Data %>% 
#     filter(!is.na({{ col }})) %>%
#     separate_rows({{ col }},sep='[,;|//\n]') %>% 
#     select(grant_id,{{ col}}) %>% 
#     drop_na() %>% 
#     mutate(merit_raw=str_trim( {{ col }})) %>% 
#     distinct() %>%
#     select(grant_id,merit_raw)
# }
# 
# merit_sprat_clean <- bind_rows(
#   col_by_grant_id(projects_species,assets),
#   col_by_grant_id(projects_species,primary_investment_priority),
#   col_by_grant_id(projects_species,secondary_investment_priority),
#   col_by_grant_id(projects_reports_species,report_species)) %>%
#   distinct() %>%
#   left_join(sprat_lookup,on='merit_raw') %>%
#   filter(!is.na(sprat_category)) %>%
#   distinct()

projects_reports_species <- projects_reports %>% 
  left_join(primary_secondary_investment_priorities,by='grant_id') %>%
  left_join(primary_investment_priority,by='grant_id') %>%
  left_join(secondary_investment_priority,by='grant_id') %>%
  left_join(project_assets,by='grant_id') %>%
  left_join(meri_outcomes_indicators,by='grant_id') %>%
  left_join(EPBC,by='grant_id') %>%
  left_join(TEC,by='grant_id') %>%
  left_join(RAMSAR,by='grant_id') %>%
  left_join(primary_secondary_outcomes,by='grant_id') %>%
  left_join(primary_outcomes,by='grant_id') %>%
  left_join(secondary_outcomes,by='grant_id') %>%
  left_join(management_units,by='management_unit') %>%
  left_join(meri_priorities,by='grant_id') %>%
  mutate(across(any_of(species_etc_cols_out),function(x) {ifelse(x=='NA',
                                                                 NA,x)}),
         meta_col_project_status='status',
         meta_col_project_start_date='start_date',
         meta_col_project_end_date='end_date',
         meta_col_project_contracted_start_date='contracted_start_date',
         meta_col_project_contracted_end_date='contracted_end_date',
         meta_col_project_name='name') %>%
  select(any_of(project_cols_out),any_of(report_cols_out),
         any_of(project_meta_cols_out),any_of(report_meta_cols_out),
         any_of(species_etc_cols_out),any_of(extract_date_cols))

Projects <- read.xlsx(paste('M01 ',extract_date,'.xlsx',sep=''),
                      sheet='Projects',
                      startRow = 1) %>%
  clean_names()

projects_species <- Projects %>%
  left_join(primary_secondary_investment_priorities,by='grant_id') %>%
  left_join(primary_investment_priority,by='grant_id') %>%
  left_join(secondary_investment_priority,by='grant_id') %>%
  left_join(project_assets,by='grant_id') %>%
  mutate(across(any_of(species_etc_cols_out),as.character)) %>%
  left_join(meri_outcomes_indicators,by='grant_id') %>%
  left_join(EPBC,by='grant_id') %>%
  left_join(TEC,by='grant_id') %>%
  left_join(RAMSAR,by='grant_id') %>%
  left_join(primary_secondary_outcomes,by='grant_id') %>%
  left_join(primary_outcomes,by='grant_id') %>%
  left_join(secondary_outcomes,by='grant_id') %>%
  left_join(report_species,by='grant_id') %>%
  left_join(management_units,by='management_unit')%>%
  left_join(meri_priorities,by='grant_id') %>%
  mutate(extract_date=extract_date) %>%
  rename(project_status=status,project_start_date=start_date,
         project_end_date=end_date,
         project_contracted_start_date=contracted_start_date,
         project_contracted_end_date=contracted_end_date,
         project_name=name) %>%
  select(any_of(project_cols_out),service_provider,description,
         any_of(species_etc_cols_out),any_of(extract_date_cols))

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

wb <- createWorkbook()
addWorksheet(wb=wb,sheetName="Projects-Species")
writeData(wb=wb,sheet="Projects-Species",
          projects_species,
          withFilter=TRUE,
          headerStyle = headerStyle)

addWorksheet(wb=wb,sheetName="Projects-Reports-Species")
writeData(wb=wb,sheet="Projects-Reports-Species",
          projects_reports_species,
          withFilter=TRUE,
          headerStyle = headerStyle)
load('dataset_metadata.Rdata')
addWorksheet(wb=wb,sheetName="MetaData")
writeData(wb=wb,sheet="MetaData",
          metadata,
          withFilter=TRUE,
          headerStyle = headerStyle)

saveWorkbook(wb=wb,file=paste0("analytical dataset ",extract_date,".xlsx"),
             overwrite=TRUE)

driver <- dbDriver("SQLite")
con <- dbConnect(driver, dbname = "database2.db")
dbWriteTable(con, "projects_species", projects_species,overwrite=TRUE)
dbWriteTable(con, "projects_reports_species", projects_reports_species,
             overwrite=TRUE)
dbDisconnect(con)
