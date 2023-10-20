#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 16:43:43 2023

@author: uchenna
"""


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# Load label matrix
label_matrix = pd.read_csv("label_matrix_clean.csv")
feature_matrix = pd.read_csv("feature_matrix_clean.csv")

# Determine the total number of columns in the feature matrix without actually loading the data
#num_cols = len(pd.read_csv("feature_matrix_clean.csv", nrows=1).columns)

correlation_all = {}
roc_auc_rf_all = {}
train_score_rf_all = {}
test_score_rf_all = {}
roc_auc_lr_all = {}
train_score_lr_all = {}
test_score_lr_all = {}
important_features_rf_all = {}
coefficients_lr_all = {}

# Loop through each column in the label_matrix
for label_col in range(315):  # Assuming 315 columns
    
    # Compute correlations between features and label using numpy for performance
    correlations = feature_matrix.apply(lambda x: np.corrcoef(x, label_matrix.iloc[:, label_col])[0, 1])
    correlation_all[label_matrix.columns[label_col]] = correlations

    # Feature reduction based on correlations
    filtered_genes = correlations[correlations.abs() >= 0.15].index.tolist()
    reduced_features_df = feature_matrix[filtered_genes]

    # Apply z-transform on the reduced features
    scaler_features = StandardScaler()
    features_scaled = scaler_features.fit_transform(reduced_features_df)

    # Binarize the label and apply RF and LR
    percentile_list = [round(x * 0.01, 2) for x in range(70, 97, 2)]
    quantiles = [label_matrix.iloc[:, label_col].quantile(p) for p in percentile_list]
    print(label_col)
    for q in quantiles:
        #print(q)
        label_binarized_df = np.where(label_matrix.iloc[:, label_col] < q, 0, 1)
        X_train, X_test, y_train, y_test = train_test_split(features_scaled, label_binarized_df, test_size=0.2, random_state=42)
        
        # Random Forest
        rf_model = RandomForestClassifier(n_estimators=500, random_state=42, max_depth=13, bootstrap=True)
        rf_model.fit(X_train, y_train)
        y_prob_rf = rf_model.predict_proba(X_test)[:, 1]
        roc_auc_rf_all[(label_matrix.columns[label_col], q)] = roc_auc_score(y_test, y_prob_rf)
        train_score_rf_all[(label_matrix.columns[label_col], q)] = rf_model.score(X_train, y_train)
        test_score_rf_all[(label_matrix.columns[label_col], q)] = rf_model.score(X_test, y_test)
        important_features_rf_all[(label_matrix.columns[label_col], q)] = rf_model.feature_importances_

        # Logistic Regression
        lr_model = LogisticRegression(max_iter=10000)
        lr_model.fit(X_train, y_train)
        y_prob_lr = lr_model.predict_proba(X_test)[:,1]
        roc_auc_lr_all[(label_matrix.columns[label_col], q)] = roc_auc_score(y_test, y_prob_lr)
        train_score_lr_all[(label_matrix.columns[label_col], q)] = lr_model.score(X_train, y_train)
        test_score_lr_all[(label_matrix.columns[label_col], q)] = lr_model.score(X_test, y_test)
        coefficients_lr_all[(label_matrix.columns[label_col], q)] = lr_model.coef_[0]

# Save the dictionaries to CSV
pd.DataFrame(correlation_all).to_csv("correlation_all.csv", index=False)
pd.DataFrame(roc_auc_rf_all, index=[0]).T.to_csv("roc_auc_rf_all.csv")
pd.DataFrame(train_score_rf_all, index=[0]).T.to_csv("train_score_rf_all.csv")
pd.DataFrame(test_score_rf_all, index=[0]).T.to_csv("test_score_rf_all.csv")
pd.DataFrame(roc_auc_lr_all, index=[0]).T.to_csv("roc_auc_lr_all.csv")
pd.DataFrame(train_score_lr_all, index=[0]).T.to_csv("train_score_lr_all.csv")
pd.DataFrame(test_score_lr_all, index=[0]).T.to_csv("test_score_lr_all.csv")
pd.DataFrame(important_features_rf_all).T.to_csv("important_features_rf_all.csv", index=False)
pd.DataFrame(coefficients_lr_all).T.to_csv("coefficients_lr_all.csv", index=False)
