#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:59:34 2024

@author: uchenna
"""



import pandas as pd
from gprofiler import GProfiler

# Load the CSV file
data = pd.read_csv('/home/uchenna/Documents/python/micro_rna/Result From Mert/top_631_genes_per_mirna_above0_5.csv')

# Initialize GProfiler instance
gp = GProfiler(return_dataframe=True)

# Prepare an empty DataFrame to store the results
results_df = pd.DataFrame()

# Iterate over each microRNA (each column except the first one)
for micro_rna in data.columns:
    gene_set = data[micro_rna].dropna().tolist()  # Convert gene list to a list, dropping NaN values
    
    # Perform enrichment analysis
    result = gp.profile(organism='hsapiens', query=gene_set, sources=["HP"], 
                        user_threshold=1e-2, significance_threshold_method='false_discovery_rate')
    
    # If the result is not empty, proceed to record the p-values
    if not result.empty:
        # Create a dictionary to hold the microRNA and p-values
        p_values = {"micro-rna": micro_rna}
        
        # Iterate over the results and collect p-values for each disease
        for _, row in result.iterrows():
            disease_name = row['name']
            p_value = row['p_value']  # Adjusted to use "p value" column
            p_values[disease_name] = p_value
        
        # Append the results for this microRNA to the DataFrame
        results_df = results_df.append(p_values, ignore_index=True)

# Fill missing diseases with NaN for consistent column structure
results_df = results_df.fillna(value=pd.NA)

# Remove any rows where there are no diseases (i.e., only NaN values)
results_df = results_df.dropna(axis=0, how='all', subset=results_df.columns[1:])
results_df1 = results_df.T
# Save the results to a CSV file
results_df1.to_csv('/home/uchenna/Documents/python/micro_rna/enrichment_results1.csv')

# Convert the DataFrame to numeric values (in case of any string NaNs)
results_df1 = results_df1.apply(pd.to_numeric, errors='coerce')

# Set the figure size for the heatmap
plt.figure(figsize=(12, 8))

# Generate a heatmap
sns.heatmap(results_df1, annot=True, cmap="viridis", cbar=True, linewidths=.5, fmt=".2g")

# Add title and labels
plt.title("Heatmap of P-values for Micro-RNAs and Diseases")
plt.xlabel("Micro-RNAs")
plt.ylabel("Diseases")

# Rotate the x labels for better readability
plt.xticks(rotation=45, ha='right')

# Show the plot
plt.tight_layout()
plt.show()