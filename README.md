#Evaluating Genetic Regulators of MicroRNAs Using Machine Learning Models. 

First, we used the command line to download bulk RNA-seq and miRNA-seq data (from solid tumor and healthy samples) of 10 thousand patients from GDC portal through APIs. The process is explained under the download section of gdcportal. 

We created a manifest that aligns RNA-seq data to the corresponding patient's miRNA-seq data using TCGAutils library from Bioconductor in R, ensuring data accuracy (The file is named "manifest_integration_rnaseq_mirnaseq_uuid.R"). 
Using the manifest file, we extracted, transformed, and loaded RNAseq and miRNAseq data into downstream machine learning models as features and labels for model training/testing (The file is named "extract_mirna_rnaseq3.py").
Trained machine learning models to predict the state of miRNAs of patients from their gene expression levels using Scikit-learn; revealing miRNA-gene regulatory relationships (The file is named "ridge_ensemble3.py"). 
Utilized the top features of the trained model to annotate miRNAs according to molecular functions and disease enrichment, using Over-Representation Analysis (The file is named "mirna_disease_enrichment_analysis1.py"). 

For citation:
Cihan M, Anyaegbunam UA, Albrecht S, Andrade-Navarro MA, Sprang M. Evaluating Genetic Regulators of MicroRNAs Using Machine Learning Models. BioRxiv. 2025 doi:10.1101/2025.01.09.632215. Under Review in Cell Patterns. 
