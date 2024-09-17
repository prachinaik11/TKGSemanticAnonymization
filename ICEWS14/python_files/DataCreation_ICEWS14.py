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
            sen_attr = group_data['MakeStatement'].iloc[0]
            # f.write(f'Name: {subject}\n')
            # f.write(f'sensitive_attribute: {sen_attr}\n')
            # f.write(f'sentence: ')
            sent = ''
            preds_obs_set = set()
            # print("preds : ", preds)

            for i in range(0, len(preds)):
                pred_ob_str =  preds[i] + objs[i]
                # print("objs : ", pred_ob_str)
                preds_obs_set.add(pred_ob_str)
            # print("preds_obs_set : ",preds_obs_set)
            for pred_ob in preds_obs_set:
                sent = sent + pred_ob + ','
                # sent = sent + objs[i] + ','
            print("sent: ",sent)
            f.write(f'{sent}\t{sen_attr}')
            f.write(f'\n')

if __name__ == "__main__":
    anony_path = "/home/prachi/PycharmProjects/Anonymization/"
    directory_path = anony_path + 'ICEWS14/dataset/snapshots_ICEWS14/withNewCol'
    # directory_path = 'snapshots/snapshots_yago_big_dataset/outputs/o_final'  # Change this to your directory path
    files = list_files_in_directory(directory_path)
    print(files)
    # files = ['snapshot_1893_1939', 'snapshot_1940_1969', 'snapshot_1970_1986', 'snapshot_1987_2002',
    #          'snapshot_2003_2017']
    for file in files:
        input_file = f'{anony_path}ICEWS14/dataset/snapshots_ICEWS14/withNewCol/{file}'
        output_file = f'{anony_path}ICEWS14/dataset/snapshots_ICEWS14/finalSentences_ICEWS14/final_{file}'
        process_csv(input_file, output_file)
