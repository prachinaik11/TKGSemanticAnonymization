import pandas as pd

def process_csv(input_file, output_file):
    # Read CSV into a pandas DataFrame
    df = pd.read_csv(input_file, delimiter='\t')
    print(df)
    gk = df.groupby('subject')
    # Write output to file
    with open(output_file, 'w') as f:
        for subject, group_data in gk:
            preds = group_data['predicate'].tolist()
            objs = group_data['object'].tolist()
            # sen_attr = group_data['birthPlace'].iloc[0]
            f.write(f'Name: {subject}\n')
            # f.write(f'sensitive_attribute: {sen_attr}\n')
            # f.write(f'sentence: ')
            sent = ''
            for i in range(0, len(preds)):
                sent = sent + preds[i]+objs[i] + ','
            f.write(f' {sent}')
            f.write(f'\n')

if __name__ == "__main__":
    input_file = "yago15k_train.tsv"  # Replace with the path to your input CSV file
    output_file = "output_yago.txt"  # Replace with the desired output file path
    process_csv(input_file, output_file)
