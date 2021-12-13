library(dplyr)
library(ggplot2)

loans_df <-readRDS("loan_df.rds")

data_for_scaling <- data.frame(loan_amount=loans_df$loan_amount,
                     annual_income=loans_df$annual_income)

scaled <- scale(data_for_scaling)

scaled_df <- data.frame(loan_amount = scaled[,1],annual_income=scaled[,2])
ggplot(scaled_df,aes(x=loan_amount,y=annual_income)) +
  geom_point()


data_dist <- dist(data_for_scaling,method="euclidean")

loans <- hclust(data_dist,method="complete")
loans_k2 <- cutree(loans,k=6)
loans_k2_complete <- mutate(scaled_df, cluster = loans_k2)
count(loans_k2_complete, cluster)

ggplot(loans_k2_complete, aes(x = loan_amount, y = annual_income, color = factor(cluster))) +
  geom_point()
