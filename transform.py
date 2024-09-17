import csv

# The path to the input CSV file
input_csv_file = 'to_be_transformed.csv'

# The path to the output CSV file
output_csv_file = 'transformed.csv'

def process_csv(input_file, output_file):
    # Dictionary to store the birthplace of each individual
    birthplaces = {}
    # List to store all rows to retain existing data
    all_rows = []

    # Read the input CSV file
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='\t', fieldnames=['subject', 'predicate', 'object', 'birthPlace'])
        for row in reader:
            subject = row['subject']
            birthPlace = row['birthPlace']
            # Store each person's birthplace
            if subject not in birthplaces:
                birthplaces[subject] = birthPlace
            # Save row for output
            all_rows.append(row)

    # Write the output CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['subject', 'predicate', 'object']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for row in all_rows:
            # Write original data, excluding the birthPlace field
            writer.writerow({'subject': row['subject'], 'predicate': row['predicate'], 'object': row['object']})
        # Write additional birthPlace rows
        for subject, birthPlace in birthplaces.items():
            writer.writerow({'subject': subject, 'predicate': '<birthPlace>', 'object': f'{birthPlace}'})

# Process the CSV files
process_csv(input_csv_file, output_csv_file)