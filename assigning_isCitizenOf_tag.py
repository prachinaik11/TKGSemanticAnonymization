# import random
#
# # Sample data
# data = [
#     ("<Abel_Xavier>", "<isAffiliatedTo>", "<Middlesbrough_F.C.>"),
#     ("<Jamie_O'Hara_(footballer)>", "<playsFor>", "<Arsenal_F.C.>", "<occursSince>", "1998-##-##"),
#     ("<Jamie_O'Hara_(footballer)>", "<playsFor>", "<Arsenal_F.C.>", "<occursUntil>", "2003-##-##"),
#     ("<Jeffrey_Monakana>", "<isAffiliatedTo>", "<Bristol_Rovers_F.C.>"),
#     ("<Alfred_Hitchcock>", "<isCitizenOf>", "<United_States>"),
#     ("<Colin_Miller_(soccer)>", "<playsFor>", "<Heart_of_Midlothian_F.C.>", "<occursSince>", "1995-##-##"),
#     ("<Dougie_Freedman>", "<isAffiliatedTo>", "<Southend_United_F.C.>"),
#     ("<The_Walt_Disney_Company>", "<owns>", "<Disney_Interactive_Studios>"),
#     ("<Adel_Taarabt>", "<isAffiliatedTo>", "<RC_Lens>"),
#     ("<Leighton_Meester>", "<wasBornIn>", "<Fort_Worth,_Texas>"),
#     ("<Larry_Niven>", "<isCitizenOf>", "<United_States>"),
#     ("<Tomasz_Cywka>", "<isCitizenOf>", "<England>"),
#     ("<Paul_Rachubka>", "<isAffiliatedTo>", "<Bury_F.C.>"),
#     ("<David_McCracken>", "<isAffiliatedTo>", "<Dundee_United_F.C.>"),
#     ("<Ed_Asner>", "<actedIn>", "<Rich_Man,_Poor_Man_(miniseries)>"),
#     ("<Christian_Hanson_(footballer)>", "<wasBornIn>", "<Middlesbrough>")
# ]
#
# # Extract individuals and their citizenships
# individuals = {}
# for triple in data:
#     if triple[1] == "<isCitizenOf>":
#         individuals[triple[0]] = triple[2]
#
# # Assign random citizenship to individuals without citizenship
# for triple in data:
#     if triple[0] not in individuals and triple[1] != "<isCitizenOf>":
#         random_citizenship = random.choice(list(individuals.values()))
#         individuals[triple[0]] = random_citizenship
#
# # Output the individuals and their citizenships
# for individual, citizenship in individuals.items():
#     print(f"{individual} <isCitizenOf> {citizenship}")



import csv
import random

# Function to read TSV file
def read_tsv(file_path):
    data = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

# Function to write data to TSV file
def write_tsv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(data)

# Sample function to assign citizenship
def assign_citizenship(data):
    individuals = {}
    new_individuals = {}
    for triple in data:
        if triple[1] == "<isCitizenOf>":
            individuals[triple[0]] = triple[2]

    # for triple in data:
    #     if triple[0] not in individuals and triple[1] != "<isCitizenOf>":
    #         random_citizenship = random.choice(list(individuals.values()))
    #         new_individuals[triple[0]] = random_citizenship

    updated_data = []
    for triple in data:
        if triple[0] not in individuals and triple[1] != "<isCitizenOf>":
                random_citizenship = random.choice(list(individuals.values()))
                new_individuals[triple[0]] = random_citizenship
                updated_data.append(
                    [triple[0], "<isCitizenOf>", random_citizenship])
    return updated_data

# Read data from TSV file
file_path = "yago15k_train.txt"
data = read_tsv(file_path)

# Assign citizenship
updated_data = assign_citizenship(data)

# Write updated data to a new TSV file
output_file_path = "1_data.tsv"
write_tsv(output_file_path, updated_data)

print("Updated data has been written to 'updated_data.tsv'.")
