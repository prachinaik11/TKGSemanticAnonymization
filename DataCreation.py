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

def process_csv(input_file, output_file):
    # Read CSV into a pandas DataFrame
    df = pd.read_csv(input_file, delimiter='\t')
    gk = df.groupby('subject')
    # Write output to file
    with open(output_file, 'w') as f:
        f.write(f'sentences\tsensitiveAttr')
        f.write(f'\n')
        for subject, group_data in gk:
            preds = group_data['predicate'].tolist()
            objs = group_data['object'].tolist()
            objs = [value.replace('<', '').replace('>', '') for value in objs]
            sen_attr = group_data['isCitizenOf'].iloc[0]
            # f.write(f'Name: {subject}\n')
            # f.write(f'sensitive_attribute: {sen_attr}\n')
            # f.write(f'sentence: ')
            sent = ''
            for i in range(0, len(preds)):
                sent = sent + preds[i]+objs[i] + ','
                # sent = sent + objs[i] + ','

            f.write(f'{sent}\t{sen_attr}')
            f.write(f'\n')

if __name__ == "__main__":
    directory_path = 'dataset/snapshots_yago_big_dataset/newcol_for_citizenOf'  # Change this to your directory path
    files = list_files_in_directory(directory_path)
    print(files)
    # files = ['snapshot_1893_1939', 'snapshot_1940_1969', 'snapshot_1970_1986', 'snapshot_1987_2002',
    #          'snapshot_2003_2017']
    for file in files:
        input_file = f'dataset/snapshots_yago_big_dataset/newcol_for_citizenOf/{file}'
        output_file = f'dataset/snapshots_yago_big_dataset/final_sentences/final_{file}'
        process_csv(input_file, output_file)
