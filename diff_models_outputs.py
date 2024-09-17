import re
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def extract_values_from_model_files(input_file, output_file):
    # Initialize an empty list to store the extracted data
    data = []

    # Read the text file
    with open(input_file, 'r') as file:
        content = file.read()

    # Regular expressions to extract the snapshot IDs and values
    snapshot_pattern = re.compile(r'final_with_new_col_isCitizenOf_snapshot_\d{4}_\d{4}\.tsv')
    k_l_pattern = re.compile(r'(\d+)\s+--\s+(\d+)')
    aail_pattern = re.compile(r'AAILavg\s*:\s*([\d\.eE+-]+)')
    ail_pattern = re.compile(r'AIL\s*:\s*([\d\.eE+-]+)')
    final_se_similarity_pattern = re.compile(r'final_SE_similarity\s*:\s*tensor\(\[\[([\d\.]+)\]\]\)')
    final_sa_similarity_pattern = re.compile(r'final_SA_similarity\s*:\s*tensor\(\[\[([\d\.]+)\]\]\)')
    fake_nodes_pattern = re.compile(r'fake_nodes\s*:\s*(\d+)')
    discarded_entries_pattern = re.compile(r'discarded_entries\s*:\s*(\d+)')
    original_num_of_individuals_pattern = re.compile(r'original number of individuals:\s*(\d+)')
    num_of_individuals_post_anonymization_pattern = re.compile(r'Sum of values:\s*(\d+)')

    # Find all occurrences of the snapshot IDs and other patterns
    snapshot_years = snapshot_pattern.findall(content)
    k_l_matches = k_l_pattern.findall(content)
    aail_matches = aail_pattern.findall(content)
    ail_matches = ail_pattern.findall(content)
    final_se_similarity_matches = final_se_similarity_pattern.findall(content)
    final_sa_similarity_matches = final_sa_similarity_pattern.findall(content)
    fake_nodes_matches = fake_nodes_pattern.findall(content)
    discarded_entries_matches = discarded_entries_pattern.findall(content)
    original_num_of_individuals_matches = original_num_of_individuals_pattern.findall(content)
    num_of_individuals_post_anonymization_matches = num_of_individuals_post_anonymization_pattern.findall(content)

    print("len(k_l_matches): ",len(k_l_matches))
    # Extract the values and append them to the data list
    for i in range(len(k_l_matches)):
        snapshot_id = int(i/20)
        snapshot_year = snapshot_years[int(i/20)] #if i < len(snapshot_years) else 'N/A'
        k, l = k_l_matches[i]
        AAIL = aail_matches[i]
        AIL = ail_matches[i]
        final_SE_similarity = final_se_similarity_matches[i]
        final_SA_similarity = final_sa_similarity_matches[i]
        fake_nodes = fake_nodes_matches[i]
        discarded_entries = discarded_entries_matches[i]
        original_num_of_individuals = original_num_of_individuals_matches[i]
        num_of_individuals_post_anonymization = num_of_individuals_post_anonymization_matches[i]

        # print("k: ",type(int(k)),"-- l: ",l)
        if int(k) >= int(l):
            data.append([
                snapshot_id,
                snapshot_year.replace("final_with_new_col_isCitizenOf_snapshot_","").replace(".tsv",""),
                k,
                l,
                AAIL,
                AIL,
                final_SE_similarity,
                final_SA_similarity,
                fake_nodes,
                discarded_entries,
                original_num_of_individuals,
                num_of_individuals_post_anonymization
            ])
        else:
            data.append([
                snapshot_id,
                snapshot_year.replace("final_with_new_col_isCitizenOf_snapshot_","").replace(".tsv",""),
                k,
                l,
                1,# AAIL,
                1,# AIL,
                0,# final_SE_similarity,
                1,# final_SA_similarity,
                fake_nodes,
                discarded_entries,
                original_num_of_individuals,
                num_of_individuals_post_anonymization
            ])

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=[
        'snapshot_id',
        'snapshot_year',
        'k',
        'l',
        'AAIL',
        'AIL',
        'final_SE_similarity',
        'final_SA_similarity',
        'fake_nodes',
        'discarded_entries',
        'original_num_of_individuals',
        'num_of_individuals_post_anonymization'
    ])

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)


def compare_diff_models(files, file_labels):
    # Initialize a list to store dataframes
    dataframes = []

    # Read the data from each file and store in the dataframes list
    for file in files:
        df = pd.read_csv("diff_models/"+file, sep='\,')
        print(f"Columns in {file}: {df.columns}")  # Check columns
        dataframes.append(df)

    # Assuming columns 'k' and 'l' are correctly named
    unique_combinations = dataframes[0][['k', 'l']].drop_duplicates()

    # Initialize a dictionary to store AIL values for each combination for each file
    ail_data = {label: [] for label in file_labels}

    # Fill the dictionary with AIL values
    for label, df in zip(file_labels, dataframes):
        for _, row in unique_combinations.iterrows():
            k, l = row['k'], row['l']
            ail_value = df[(df['k'] == k) & (df['l'] == l)]['AIL'].iloc[0]
            ail_data[label].append(ail_value)

    # Plot the data
    plt.figure(figsize=(12, 6))

    x_labels = [f'({row["k"]},{row["l"]})' for _, row in unique_combinations.iterrows()]

    for label in file_labels:
        plt.plot(x_labels, ail_data[label], marker='o', label=label)

    plt.xlabel('Unique Combinations of (k, l)')
    plt.ylabel('AIL Values')
    plt.title('Comparison of AIL Values Across Files')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    # Save the plot to a file
    output_file = 'comparison_diff_models.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()
    plt.show()




# Define the input and output file names
# input_file = 'diff_models/outputs_for_paraphrase-MiniLM-L12-v2'  # Assuming the input text file is named 'results.txt'
# output_file = 'diff_models/paraphrase-MiniLM-L12-v2.csv'
# extract_values_from_model_files(input_file, output_file)




# File names
files = ['all-MiniLM-L6-v2 (copy).csv', 'paraphrase-MiniLM-L12-v2.csv',
         'distilbert-base-nli-stsb-mean-tokens.csv', 'all-mpnet-base-v2.csv']
file_labels = ['all-MiniLM-L6-v2', 'paraphrase-MiniLM-L12-v2',
               'distilbert-base-nli-stsb-mean-tokens', 'all-mpnet-base-v2']
# files = ['all-MiniLM-L6-v2 (copy).csv']
compare_diff_models(files, file_labels)