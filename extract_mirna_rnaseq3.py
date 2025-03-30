#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:52:54 2023

@author: uchenna
"""


import pandas as pd

#read general manifest (gene manifest aligned to mirna manifest)
manifest_merged_df = pd.read_csv("merged_manifest3.csv")


#download_directory = "/home/uchenna/Documents/GDC project/" # folder where the files are. #folder where you are running GDC client from

experiment_no = 10464 #10000 #number of patients
# Create a new DataFrame with 60660 columns (60,660 genes) and 10000 rows (# of experiment or #Proj id's)
feature_matrix = pd.DataFrame(columns=range(60660), index=range(experiment_no))
# Create a new DataFrame with 1881 columns (1,881 mirnas) and 10000 rows (# of experiment or #Proj id's)
label_matrix = pd.DataFrame(columns=range(1880), index=range(experiment_no))

#loop through the rnaseq manifest
for index, row in manifest_merged_df.iterrows():
    
    #compute the directory of gene file corresponding to the row
    filedir_gene = row['id_gene'] + "/" + row['filename_gene'] 
    
    #compute the directory of mirna file corresponding to the row
    filedir_mirna = row['id_mirna'] + "/" + row['filename_mirna']
    
    #open the files
    df_gene = pd.read_csv(filedir_gene, sep='\t', skiprows=1)
    df_mirna = pd.read_csv(filedir_mirna, delimiter="\t")
    
    #enter the gene
    feature_matrix.iloc[index,:] = df_gene.iloc[4:60664,6]
    #enter the mirna
    label_matrix.iloc[index,:] = df_mirna.iloc[1:1881,2]
    
    
#Save the feature_matrix and label_matrix dataframes to a new CSV file
output_features = "feature_matrix.csv"
output_labels = "label_matrix.csv"

feature_matrix.to_csv(output_features, index=False)
label_matrix.to_csv(output_labels, index=False)
