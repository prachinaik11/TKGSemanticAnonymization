import random
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


def process_triples(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    print(lines)
    # Extract existing triples and collect citizenship information
    individuals = {}
    citizenships = []

    for line in lines:
        if line.strip():  # Ensure the line isn't empty
            subject, predicate, obj = line.strip().split('\t')
            print("subject: ",subject)
            print("predicate: ", predicate)
            print("obj: ", obj)
            if subject not in individuals:
                individuals[subject] = {}
            if predicate not in individuals[subject]:
                individuals[subject][predicate] = obj
            else:
                individuals[subject][predicate] = individuals[subject][predicate] + ',' + obj
            print("individuals: ",individuals)
            if predicate == '<isCitizenOf>':
                if obj not in citizenships:
                    citizenships.append(obj)
                print("citizenships: ", citizenships)

    # Assign random citizenships to individuals who lack them
    updated_triples = []
    for subject, predicates in individuals.items():
        # Add existing triples to the updated list
        for predicate, obj in predicates.items():
            updated_triples.append(f"{subject}\t{predicate}\t{obj}\n")

        # Check if '<isCitizenOf>' is missing and add it
        if '<isCitizenOf>' not in predicates:
            random_citizenship = random.choice(citizenships)  # Choose a random existing citizenship
            updated_triples.append(f"{subject}\t<isCitizenOf>\t{random_citizenship}\n")

    # print("updated_triples: ",updated_triples)
    # Write the updated triples back to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in updated_triples:
            file.write(line)


# input_file = 'yago15k_train (copy).txt'  # Input file containing the original triples
# output_file = 'updated_data.txt'  # File to write the updated triples
# Usage
directory_path = 'snapshots/snapshots_yago_smol/'  # Change this to your directory path
files = list_files_in_directory(directory_path)
print(files)
# files = ['snapshot_1893_1939.tsv','snapshot_1940_1969.tsv','snapshot_1970_1986.tsv','snapshot_1987_2002.tsv','snapshot_2003_2017.tsv']

for file in files:
    input_file = f'snapshots/snapshots_yago_smol/{file}'
    output_file = f'snapshots/snapshots_yago_smol/outputs/output_final_{file}.csv'
    process_triples(input_file, output_file)
# file = "snapshot_2003_2017_1.tsv"
# file = "snapshot_2003_2017 (copy).tsv"
# input_file = f'snapshots/snapshots_yago/{file}'
# output_file = f'snapshots/snapshots_yago/outputs1/output_final_{file}.csv'
# process_triples(input_file, output_file)