#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:30:08 2023

@author: uchenna
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score, median_absolute_error

# Load datasets
labels_df = pd.read_csv("label_matrix_clean.csv")
features_df = pd.read_csv("feature_matrix_clean.csv")

# Ensure no NaN or infinite values
assert not features_df.isnull().any().any(), "Data contains NaN values"
assert not labels_df.isnull().any().any(), "Label contains NaN values"
assert not np.isinf(features_df).any().any(), "Data contains infinity values"
assert not np.isinf(labels_df).any().any(), "Label contains infinity values"

# Remove columns with zero variance (if any)
features_df = features_df.loc[:, features_df.std() > 0]

# Z-transform for features
scaler_features = StandardScaler()
features_df = pd.DataFrame(scaler_features.fit_transform(features_df), columns=features_df.columns)

# Prepare dictionaries to store data
y_data = {}
feature_importance_data = {}

# Prepare a list to store metrics
results = []

# Loop over all columns in labels_df
for col in labels_df.columns:
    labels = labels_df[col]

    # Splitting data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(features_df, labels, test_size=0.2, random_state=42)

    # Apply Ridge regression
    ridge_model = Ridge(alpha=11000)
    ridge_model.fit(X_train, y_train)

    # Predict using Ridge regression
    y_pred = ridge_model.predict(X_test)

    # Save y_test and y_pred in the dictionary
    y_data[f'{col}_ytest'] = y_test.tolist()
    y_data[f'{col}_ypred'] = y_pred.tolist()

    # Save feature importances
    feature_importance_data[col] = ridge_model.coef_.tolist()

    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    medae = median_absolute_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    y_test_mean = np.mean(y_test)
    y_pred_mean = np.mean(y_pred)
    cv_test = np.std(y_test) / y_test_mean
    cv_pred = np.std(y_pred) / y_pred_mean
    perc_25_test = np.percentile(y_test, 25)
    perc_50_test = np.percentile(y_test, 50)
    perc_75_test = np.percentile(y_test, 75)
    perc_25_pred = np.percentile(y_pred, 25)
    perc_50_pred = np.percentile(y_pred, 50)
    perc_75_pred = np.percentile(y_pred, 75)
    corr = np.corrcoef(y_test, y_pred)[0, 1]



    # Save metrics to results list
    results.append([col, r2, medae, mae, y_test_mean, y_pred_mean, cv_test, cv_pred, 
                    perc_25_test, perc_50_test, perc_75_test, perc_25_pred, 
                    perc_50_pred, perc_75_pred, corr])

# Save y_data dictionary to DataFrame and to a CSV file
pd.DataFrame(y_data).to_csv('y_test_ypred_data.csv', index=False)

# Save feature importance data to DataFrame and to a CSV file
pd.DataFrame(feature_importance_data, index=features_df.columns).to_csv('feature_importance_data.csv', index=True)

# Save results to a CSV file
columns = ['Label', 'R-squared', 'Median Abs Err', 'Mean Abs Err', 'Mean of y_test', 
           'Mean of y_pred', 'CV of y_test', 'CV of y_pred', '25th percentile y_test', 
           '50th percentile y_test', '75th percentile y_test', '25th percentile y_pred', 
           '50th percentile y_pred', '75th percentile y_pred', 'Correlation']
pd.DataFrame(results, columns=columns).to_csv('results_metrics.csv', index=False)

print("Metrics, y_test, y_pred data, and feature importances saved.")

