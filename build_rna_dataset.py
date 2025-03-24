import os
import pandas as pd

#Get one sample to see the structure of the data
sample = pd.read_csv('rna/0a4e0b83-7afa-475b-8586-e9e79e31d6d2.rna_seq.augmented_star_gene_counts.tsv', sep = '\t',skiprows=5)
sample.columns = pd.read_csv('rna/0a4e0b83-7afa-475b-8586-e9e79e31d6d2.rna_seq.augmented_star_gene_counts.tsv', sep='\t', skiprows=1).columns

root_folder = 'rna'

rna = pd.DataFrame(columns=['case_id'] + sample['gene_id'].tolist())
i=0
error_files = []


for file in os.listdir(root_folder):
    try:
        #Read the file
        seq = pd.read_csv(os.path.join(root_folder, file), sep='\t', skiprows=5)
        
        #Add the sample to the dataframe
        rna.loc[i] = [file] + seq.iloc[:, -3].tolist()
        i += 1
        print(f"File {file} processed, {i} samples processed in total")

    except Exception as e:
        # Handling errors
        error_files.append(file)
        print(f"Failed to process file {file} because of error {e}")


rna.to_csv('rna1.csv', index=False)