import pandas as pd
import os

def list_files_in_directory(directory_path):
    """
    List all file names in the given directory.

    :param directory_path: The path to the directory from which to list files.
    :return: A list of filenames found in the directory.
    """
    # Check if the provided path is a directory
    if not os.path.isdir(directory_path):
        print("The provided path is not a directory.")
        return []

    # List all entries in the directory
    file_names = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    return sorted(file_names)

# Assuming the data is stored in 'data.csv' and is tab-separated
# file_path = 'updated_data.csv'
# directory_path = 'snapshots/snapshots_yago_big_dataset/outputs'  # Change this to your directory path
# directory_path = 'snapshots/snapshots_yago_big_dataset'  # Change this to your directory path
directory_path = 'dataset/snapshots_yago_big_dataset'  # Change this to your directory path

files = list_files_in_directory(directory_path)
print(files)
# files = ['snapshot_1893_1939','snapshot_1940_1969','snapshot_1970_1986','snapshot_1987_2002','snapshot_2003_2017']


for file in files:
    # file_path = f'snapshots/snapshots_yago_big_dataset/outputs/output_final_{file}.csv'
    # file_path = f'snapshots/snapshots_yago_big_dataset/outputs/{file}'
    # file_path = f'snapshots/snapshots_yago_big_dataset/{file}'
    file_path = f'dataset/snapshots_yago_big_dataset/{file}'

    # Read the CSV file
    df = pd.read_csv(file_path, sep='\t', names=['subject', 'predicate', 'object'])

    # Filter rows where predicate is 'isCitizenOf'
    citizenship_df = df[df['predicate'] == '<isCitizenOf>'][['subject', 'object']].rename(columns={'object': 'isCitizenOf'})

    # Remove the <isCitizenOf> triples from the original DataFrame
    df = df[df['predicate'] != '<isCitizenOf>']

    # Merge the citizenship information back to the original dataframe
    result_df = pd.merge(df, citizenship_df, on='subject', how='left')

    # Saving the updated DataFrame to a new CSV file
    # result_df.to_csv(f'snapshots/snapshots_yago_big_dataset/outputs/o_final/with_new_col_isCitizenOf_{file}', sep='\t', index=False)
    result_df.to_csv(f'dataset/snapshots_yago_big_dataset/newcol_for_citizenOf/with_new_col_isCitizenOf_{file}', sep='\t', index=False)
    # Optionally, print the head of the resulting DataFrame to check
    print(result_df.head())
