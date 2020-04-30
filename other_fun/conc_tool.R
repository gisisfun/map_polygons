if(!require("tidyr")){
  install.packages("tidyr")
  library(tidyr)
}

if(!require("dplyr")) {
  install.packages("dplyr")
  library(dplyr)
}

if(!require("tcltk")){
  install.packages("tcltk")
  library(tcltk)
}

Filters <- matrix(c("Text",".txt"), byrow=TRUE)

from_geog_file <- file.path("Inputs","SA22016.TXT") 
#or file.choose(caption="Select source geography file",multi=FALSE,filter=Filters)

to_geog_file <- file.path("Inputs","FED2019.TXT") #or file.choose()
#or file.choose(caption="Select destination geography file",multi=FALSE,filter=Filters)

weights_file <- file.path"Inputs","ABS_MB_2016_with_URP16.TXT")
#or file.choose(caption="Select geography weighting file",multi=FALSE,filter=Filters)
conc_file <- "Results/SA22016_AECFED2019_MB2016_based-test.txt"
#or file.choose(caption="Select concordance file name",multi=FALSE,filter=Filters)

# weights file
mb_pops <- read.table(weights_file, sep="\t",header=TRUE)
print(paste('mb_pops',names(mb_pops)))

#from geography
from_geog <- read.table(from_geog_file, sep="\t",header=TRUE)
print(paste('from_geog',names(from_geog)))
from_names <- names(from_geog)[2:3]
from_mb_source_pop <- inner_join(from_geog,mb_pops,by="MB_CODE_2016", suffix = c(".x",".y"))
from_mb_source_pop <- data.frame(from_mb_source_pop$MB_CODE_2016,
                                 from_mb_source_pop[2],
                                 from_mb_source_pop[3],
                                 from_mb_source_pop$URP16_POP)

names(from_mb_source_pop) <- c('mb_code_2016','from_code','from_name','from_pop')
print(head(from_mb_source_pop))
print(from_names)

# to gegography
to_geog <- read.table(to_geog_file, sep="\t",header=TRUE)
print(paste('to_geog',names(to_geog)))

to_names <- names(to_geog)[2:3]
to_mb_source_pop <-inner_join(to_geog,mb_pops,by="MB_CODE_2016", suffix = c(".x",".y"))
to_mb_source_pop <- data.frame(to_mb_source_pop$MB_CODE_2016,
                               to_mb_source_pop[2],
                               to_mb_source_pop[3],
                               to_mb_source_pop$URP16_POP)
names(to_mb_source_pop) <- c('mb_code_2016','to_code','to_name','to_pop')
print(head(to_mb_source_pop))
print(to_names)

# Sum URP16 for from_geog_pop
#
# DQ_MB16_POA16_Pop (mb_from_pop)
#
# SELECT MB16_POA16_Source.POA_CODE_2016, 
# Sum(MB16_POA16_Source!Persons_Usually_Resident_2016) AS MB_Pop
# FROM MB16_POA16_Source
# GROUP BY MB16_POA16_Source.POA_CODE_2016;

from_pop <- from_mb_source_pop %>%
  group_by(from_code,from_name) %>%
  summarise(mb_pop = sum(from_pop))

print(head(from_pop))

# DQ_MB16_POA16_SSC16_Pop (from_to_pop)

# SELECT MB16_POA16_Source.POA_CODE_2016, 
#        MB16_SSC16_Source.SSC_CODE_2016, 
#        MB16_SSC16_Source.SSC_NAME_2016, 
#        Sum(MB16_SSC16_Source.Persons_Usually_Resident_2016) AS PC_POP
# FROM MB16_POA16_Source INNER JOIN MB16_SSC16_Source 
# ON MB16_POA16_Source.MB_CODE_2016 = MB16_SSC16_Source.MB_CODE_2016
# GROUP BY MB16_POA16_Source.POA_CODE_2016, 
#          MB16_SSC16_Source.SSC_NAME_2016, 
#          MB16_SSC16_Source.SSC_CODE_2016
# ORDER BY MB16_POA16_Source.POA_CODE_2016;

from_to_pop <- from_mb_source_pop %>%
  inner_join(to_mb_source_pop,by="mb_code_2016", suffix = c(".x",".y")) %>%
  select(-to_pop) %>%
  group_by(from_code,from_name,to_code,to_name) %>%
  summarise(partial_pop = sum(from_pop)) %>%
  arrange(to_code)

print(head(from_to_pop,50))

#from_to_pop <- mb_from_to_pop 

# Q_SSC16_to_POA16_MB16_Based (from_to_concordance)
#
# SELECT [DQ_MB16_SSC16_POA16_Pop].POA_CODE_2016, 
#         DQ_MB16_SSC16_Pop!MB_Pop*([DQ_MB16_SSC16_POA16_Pop]!PC_POP/DQ_MB16_SSC16_Pop!MB_Pop) AS Shared_2011_Pop,
#         IIf(DQ_MB16_SSC16_Pop!MB_Pop=0,0,IIf(([DQ_MB16_SSC16_POA16_Pop]!PC_POP/DQ_MB16_SSC16_Pop!MB_Pop)>1,100,(([DQ_MB16_SSC16_POA16_Pop]!PC_POP/DQ_MB16_SSC16_Pop!MB_Pop)*100))) AS Percentage, IIf(DQ_MB16_SSC16_Pop!MB_Pop=0,0,IIf(([DQ_MB16_SSC16_POA16_Pop]!PC_POP/DQ_MB16_SSC16_Pop!MB_Pop)>1,1,(([DQ_MB16_SSC16_POA16_Pop]!PC_POP/DQ_MB16_SSC16_Pop!MB_Pop)))) AS Proportion,
#         [DQ_MB16_SSC16_POA16_Pop].SSC_CODE_2016, 
#         [DQ_MB16_SSC16_POA16_Pop].SSC_NAME_2016
# FROM DQ_MB16_SSC16_Pop INNER JOIN DQ_MB16_SSC16_POA16_Pop
# ON DQ_MB16_SSC16_Pop.SSC_CODE_2016=[DQ_MB16_SSC16_POA16_Pop].SSC_CODE_2016;

from_to_conc <- from_to_pop %>%
  inner_join(from_pop, by="from_code", suffix = c(".x",".y")) %>%
  select(from_code,from_name=from_name.x,to_code,to_name,Shared_2016_Pop=partial_pop,-from_name.y,Tot_Pop=mb_pop) %>%
  mutate(Proportion = Shared_2016_Pop/Tot_Pop) %>%
  select(from_code, from_name, Shared_2016_Pop, Proportion, to_code, to_name,-Tot_Pop) %>%
  arrange(from_code) %>%
  replace_na(list(Proportion=0))

# apply original geography codes and names
names(from_to_conc) <- c(from_names[1],from_names[2],'Shared_2016_Pop','Proportion',to_names[1],to_names[2])
print(head(from_to_conc))

# write file to server
write.table(from_to_conc,file=conc_file,append=FALSE,sep='\t',row.names=FALSE)

