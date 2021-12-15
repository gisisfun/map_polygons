library(dplyr)
library(tidymodels)
library(xgboost)

set.seed(420)
loans_df <-readRDS("loan_df.rds")
# Create data split object
loans_split_class <- initial_split(loans_df, 
                             strata = loan_default)

# Build training data
loans_training_class <- loans_split_class %>% 
  training()

# Build test data
loans_test_class <- loans_split_class %>% 
  testing()

# # Specify the model class
# boost_spec_class <- boost_tree() %>%
#   # Set the mode
#   set_mode("classification") %>%
#   # Set the engine
#   set_engine("xgboost")
# 
# boost_spec_class
# 
# 
# boost_model_class <- fit(boost_spec_class,
#                    formula = loan_default ~ .,
#                    loans_training_class)
# 
# boost_model_class
# 
# # Evaluate the Ensemble
# set.seed(99)
# 
# # Create CV folds
# folds_class <- vfold_cv(loans_training_class,v = 5)
# 
# # Fit and evaluate models for all folds
# cv_results_class <- fit_resamples(boost_spec_class,
#                             loan_default ~ .,
#                             resamples = folds_class,
#                             metrics = metric_set(roc_auc))
# 
# # Collect cross-validated metrics
# collect_metrics(cv_results_class)
# 
# # Compare to a single classifier
# set.seed(100)
# 
# # Specify, fit, predict, and combine with training data
# predictions_boost_class <- boost_tree() %>%
#   set_mode("classification") %>%
#   set_engine("xgboost") %>% 
#   fit(loan_default ~ ., data = loans_training_class) %>%
#   predict(new_data = loans_training, type = "prob") %>% 
#   bind_cols(loans_training)
# 
# # Calculate AUC
# roc_auc(predictions_boost_class, 
#         truth = loan_default, 
#         estimate = .pred_yes)
# 
# # as decision Tree
# 
# set.seed(100)
# 
# 
# 

# Create the specification with placeholders
boost_spec_bt_class <- boost_tree(
  trees = 500,
  learn_rate = tune(),
  tree_depth = tune(),
  sample_size = tune()) %>%
  set_mode("classification") %>%
  set_engine("xgboost")

# Create the tuning grid
tunegrid_boost_bt_class <- grid_regular(parameters(boost_spec_bt_class), 
                               levels = 3)

tunegrid_boost_bt_class 

# Create CV folds of training data
folds_bt_class <- vfold_cv(loans_training_class, v=6)

# Tune along the grid
tune_results_bt_class <- tune_grid(boost_spec_bt_class,
                          loan_default ~ .,
                          resamples = folds_bt_class,
                          grid = tunegrid_boost_bt_class,
                          metrics = metric_set(roc_auc))

# Plot the results
autoplot(tune_results_bt_class)

# Select the final hyperparameters
best_params_bt_class  <- select_best(tune_results_bt_class )

best_params_bt_class 

# Finalize the specification
final_spec_bt_class  <- finalize_model(boost_spec_bt_class , best_params_bt_class )

final_spec_bt_class 


# # Finalize your workflow
# final_loans_wkfl_class <- loans_tune_wkfl_class %>% 
#   finalize_workflow(best_dt_model_class)
# 
# final_loans_wkfl_class

# Train the final model on the full training data
final_model_bt_class  <- final_spec_bt_class  %>%
  #last_fit(split = loans_split_class)
  fit(formula = loan_default ~ ., data = loans_training_class)

final_model_bt_class 

# The models were all tuned to perfection and trained on the same training set, 
# customers_train, and predictions were made for the customers_test dataset. 
# The results are numeric probabilities and are available as preds_combined 
# in your session:



# final_model_bt_class %>% 
#   collect_metrics()

pred_bt_prob_class  <- predict(final_model_bt_class,loans_test_class,type="prob") %>%
  bind_cols(loans_test_class)
pred_bt_prob_class %>%
  # Calculate ROC curve metrics
  roc_curve(truth = loan_default, .pred_yes) %>%
  # Plot the ROC curve
  autoplot()

pred_bt_prob_class %>%
  roc_auc(truth = loan_default, .pred_yes)

# Specify, fit, predict and combine with training data
preds_dt_class <- decision_tree() %>%
  set_mode("classification") %>%
  set_engine("rpart") %>% 
  fit(loan_default ~ ., data = loans_training_class) %>%
  predict(new_data = loans_training, type = "prob") %>% 
  bind_cols(loans_training)

# Calculate AUC
pred_bt_prob_class %>%
  roc_auc(truth = loan_default, .pred_yes)