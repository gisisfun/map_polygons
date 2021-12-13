library(dplyr)
library(tidymodels)
library(rpart.plot)
library(fastDummies)

set.seed(420)
loans_df <-readRDS("loan_df.rds")
# Create data split object
loans_split <- initial_split(loans_df, 
                             strata = loan_default)

# Build training data
loans_training <- loans_split %>% 
  training()

# Build test data
loans_test <- loans_split %>% 
  testing()

dt_model <- decision_tree() %>% 
  # Specify the engine
  set_engine('rpart') %>% 
  # Specify the mode
  set_mode('regression')

# Build feature engineering pipeline
loans_recipe <- recipe(loan_amount ~ .,
                       data = loans_training) %>% 
  # Correlation filter
  step_corr(all_numeric(), threshold = 0.85) %>% 
  # Normalize numeric predictors
  #step_normalize(all_numeric(),-all_outcomes()) %>% 
  # Create dummy variables
  step_dummy(all_nominal(),-all_outcomes())

loans_recipe

# Create a workflow
loans_dt_wkfl <- workflow() %>% 
  # Include the model object
  add_model(dt_model) %>% 
  # Include the recipe object
  add_recipe(loans_recipe)

# View workflow specification
loans_dt_wkfl

# Train the workflow
loans_dt_wkfl_fit <- loans_dt_wkfl %>% 
  last_fit(split = loans_split)

# Calculate performance metrics on test data
loans_dt_wkfl_fit %>% 
  collect_metrics()

# Create cross validation folds
set.seed(290)
loans_folds <- vfold_cv(loans_training, v = 10,
                        strata = loan_default)

loans_folds

# Create custom metrics function
loans_metrics <- metric_set(rmse,rsq)

# Fit resamples
loans_dt_rs <- loans_dt_wkfl %>% 
  fit_resamples(resamples = loans_folds,
                metrics = loans_metrics)

# View performance metrics
loans_dt_rs %>% 
  collect_metrics()


# logistic_model <- logistic_reg() %>% 
#   # Specify the engine
#   set_engine("glm") %>% 
#   # Specify the mode
#   set_mode('classification')
# 
# # Create workflow
# loans_logistic_wkfl <- workflow() %>% 
#   # Add model
#   add_model(logistic_model) %>% 
#   # Add recipe
#   add_recipe(loans_recipe)
# 
# # Fit resamples
# loans_logistic_rs <- loans_logistic_wkfl %>% 
#   fit_resamples(resamples = loans_folds,
#                 metrics = loans_metrics)
# 
# # View performance metrics
# loans_logistic_rs %>% 
#   collect_metrics()

# Detailed cross validation results
dt_rs_results <- loans_dt_rs %>% 
  collect_metrics(summarize=FALSE)

# Explore model performance for decision tree
dt_rs_results %>% 
  group_by(.metric) %>% 
  summarize(min = min(.estimate),
            median = median(.estimate),
            max = max(.estimate))


# Detailed cross validation results
logistic_rs_results <- loans_logistic_rs %>% 
  collect_metrics(summarize=FALSE)

# Explore model performance for logistic regression
logistic_rs_results %>% 
  group_by(.metric) %>% 
  summarize(min = min(.estimate),
            median = median(.estimate),
            max = max(.estimate))

# Back to the Decision tree

# Set tuning hyperparameters
dt_tune_model <- decision_tree(cost_complexity = tune(),
                               tree_depth = tune(),
                               min_n = tune()) %>% 
  # Specify engine
  set_engine('rpart') %>% 
  # Specify mode
  set_mode('regression')

dt_tune_model

# Create a tuning workflow
loans_tune_wkfl <- loans_dt_wkfl %>% 
  # Replace model
  update_model(dt_tune_model)

loans_tune_wkfl


# Hyperparameter tuning with grid search
set.seed(214)
dt_grid <- grid_random(parameters(dt_tune_model),
                       size = 5)

# Hyperparameter tuning
dt_tuning <- loans_tune_wkfl %>% 
  tune_grid(resamples = loans_folds,
            grid = dt_grid,
            metrics = loans_metrics)

# Extract the summarized tuning results from your tuning object.
# View results
dt_tuning %>% 
  collect_metrics()

# Collect detailed tuning results
dt_tuning_results <- dt_tuning %>% 
  collect_metrics(summarize=FALSE)

dt_tuning_results

# Explore detailed ROC AUC results for each fold
dt_tuning_results %>% 
  filter(.metric=="rmse") %>% 
  group_by(id) %>% 
  summarize(min_rmse = min(.estimate),
            median_rmse = median(.estimate),
            max_rmse = max(.estimate))

# Display 5 best performing models
dt_tuning %>% 
  show_best(metric = 'rmse', n = 5)

# Select based on best performance
best_dt_model <- dt_tuning %>% 
  # Choose the best model based on roc_auc
  select_best(metric = 'rmse')

best_dt_model

# Finalize your workflow
final_loans_wkfl <- loans_tune_wkfl %>% 
  finalize_workflow(best_dt_model)

final_loans_wkfl

# Train finalized decision tree workflow
loans_final_fit <- final_loans_wkfl %>% 
  last_fit(split = loans_split)

# View performance metrics
loans_final_fit %>% 
  collect_metrics()

# # Create an ROC curve
# loans_final_fit %>% 
#   # Collect predictions
#   collect_predictions() %>%
#   # Calculate ROC curve metrics
#   roc_curve(truth = loan_default, .pred_yes) %>%
#   # Plot the ROC curve
#   autoplot()

# predictions <- predict(loans_final_fit,
#                        new_data=loans_test) %>%
#   # Add the test set
#   bind_cols(loans_test)

# back to Base R via tidymodels and tidyverse
tree_fit_model <- loans_final_fit %>% 
  extract_fit_parsnip() 

par(mar=c(1,0,0,0),oma=c(0,0,0,0))
rpart.plot(tree_fit_model$fit,roundint=FALSE,main = "Loans - Loan Amount Model",
           type=3,
           clip.right.labs=FALSE,
           branch=.3,
           cex=0.5)

rpart.rules(tree_fit_model$fit,roundint=FALSE,cover=TRUE)



new_loans_df <- loans_df %>% dummy_cols(select_columns=c("loan_default","loan_purpose",
                                                         "missed_payment_2_yr")) #%>% 
# select(interest_rate,debt_to_income,annual_income,
#        installment,loan_purpose_medical,loan_amount,loan_purpose_credit_card,
#        loan_purpose_small_business,loan_purpose_home_improvement,
#        missed_payment_2_yr_no)

predictions <- predict(tree_fit_model,new_loans_df)

new_loans_df <- new_loans_df %>% bind_cols(predictions)
