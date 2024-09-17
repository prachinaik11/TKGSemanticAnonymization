import re
import pandas as pd

anony_path = "/home/prachi/PycharmProjects/Anonymization/"
input_file = anony_path + 'freebase_outputs_final'
# Define the input and output file names
output_file = anony_path + 'Freebase/freebase_extracted_values.csv'

# Initialize an empty list to store the extracted data
data = []

# Read the text file
with open(input_file, 'r') as file:
    content = file.read()

# Regular expressions to extract the snapshot IDs and values
snapshot_pattern = re.compile(r'final_with_new_col_country_freebase_dataset_snapshot_\d{4}_\d{4}\.tsv')
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
            snapshot_year.replace("final_with_new_col_country_freebase_dataset_snapshot_","").replace(".tsv",""),
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
            snapshot_year.replace("final_with_new_col_country_freebase_dataset_snapshot_","").replace(".tsv",""),
            k,
            l,
            1,# AAIL,
            1,# AIL,
            0,# final_SE_similarity,
            1,# final_SA_similarity,
            "MAX",
            "MAX",
            "NA",
            "NA"
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
