# https://cran.r-project.org/web/packages/textmineR/vignettes/c_topic_modeling.html

library(dplyr)
library(tidytext)

corpus <- data.frame(text = c("Due to bad loans, the bank agreed to pay the fines",
"If you are late to pay off your loans to the bank you will face fines",
"A new restaurant opened in downtown",
"There is a new restaurant that just opened on Warwick street",
"How will you pay off the loans you will need for the restaurant you want opened?"), 
id = c("d_1", "d_2", "d_3", "d_4", "d_5"))

dtm <- corpus %>% 
    # Specify the input column
	unnest_tokens(input=text, output=word, drop=TRUE) %>% 
	count(id, word) %>% 
    # Specify the token
	cast_dtm(document=id, term=word, value=n)

mod = LDA(x=dtm, k=2, method="Gibbs", control=list(alpha=1, delta=0.1, seed=10005))

posterior(mod)$topics
