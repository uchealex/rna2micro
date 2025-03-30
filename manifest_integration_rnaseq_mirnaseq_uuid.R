#if (!require("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
#BiocManager::install("TCGAutils")

library(TCGAutils)
library(dplyr)
library(tidyr)

#test
#head(UUIDtoUUID("ae55b2d3-62a1-419e-9f9a-5ddfac356db4", to_type = "file_id"))
#head(UUIDtoUUID("1432ce04-3c54-4876-a878-c44536d5451b", to_type = "case_id"))

#correct directory
setwd("~/Documents/GDC project")

#read in manifest files
genes=read.csv("gene_manifest_merge.csv",sep="")
mirna=read.csv("mirna_manifest_merge.csv",sep = "")

#extract column with file id
genes_file_ids=genes$id
mirna_file_ids=mirna$id

#get the filenames, not file ids
genes_file_names=genes$filename
mirna_file_names=mirna$filename

#get the case ids
genes_case_id= UUIDtoUUID(genes_file_ids, to_type="case_id")
mirna_case_id= UUIDtoUUID(mirna_file_ids, to_type="case_id")

#get the barcode
genes_barcode=UUIDtoBarcode(genes_file_ids, from_type = "file_id")
mirna_barcode=UUIDtoBarcode(mirna_file_ids, from_type = "file_id")
#genes_barcode=filenameToBarcode(genes_file_names)
#mirna_barcode=filenameToBarcode(mirna_file_names)

genes_final=merge(genes, genes_barcode, by.x="id", by.y="file_id")
mirna_final=merge(mirna, mirna_barcode, by.x="id", by.y="file_id")
#genes_final=merge(genes, genes_barcode, by.x="filename", by.y="file_name")
#mirna_final=merge(mirna, mirna_barcode, by.x="filename", by.y="file_name")

#put case_ids to original df
genes_final=merge(genes_final, genes_case_id, by.x = "id", by.y = "file_id")
mirna_final=merge(mirna_final, mirna_case_id, by.x = "id", by.y = "file_id")

#add info if tumor or not
genes_final <- genes_final %>% 
  mutate(status = ifelse(as.numeric(substr(associated_entities.entity_submitter_id, 14, 15)) <= 9, "tumor", "normal"))

mirna_final <- mirna_final %>% 
  mutate(status = ifelse(as.numeric(substr(associated_entities.entity_submitter_id, 14, 15)) <= 9, "tumor", "normal"))
#genes_final=genes_final %>% mutate(status = ifelse(as.numeric(substr(cases.samples.portions.analytes.aliquots.submitter_id,14,15))>9, "tumor", "normal"))
#mirna_final=mirna_final %>% mutate(status = ifelse(as.numeric(substr(cases.samples.portions.analytes.aliquots.submitter_id,14,15))>9, "tumor", "normal"))

#table= left_join(mirna_final,genes_final, join_by(cases.case_id == cases.case_id , status == status), relationship = "many-to-many")         

#table
#save files
write.csv(genes_final,"gene_manifest_merge_uuid3.csv",row.names = F)
write.csv(mirna_final,"mirna_manifest_merge_uuid3.csv",row.names = F)


#check how many different cases for genes and mirna
#length(unique(genes_case_id$cases.case_id))
#length(unique(mirna_case_id$cases.case_id))


#table(genes_final$cases.case_id)
