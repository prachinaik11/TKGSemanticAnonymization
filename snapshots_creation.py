# Sample Data
# data = [
#     "<Jon_Bon_Jovi>\t<isCitizenOf>\t<United_States>",
#     "<Daniel_Hernández_(soccer)>\t<isCitizenOf>\t<England>",
#     "<Etta_James>\t<hasWonPrize>\t<Grammy_Award>",
#     "<Rolando_Bianchi>\t<isAffiliatedTo>\t<Bologna_F.C._1909>",
#     "<Alan_Rickman>\t<isCitizenOf>\t<Wales>",
#     "<Simon_Grayson>\t<playsFor>\t<Aston_Villa_F.C.>\t<occursSince>\t\"1997-##-##\"",
#     "<Simon_Grayson>\t<playsFor>\t<Aston_Villa_F.C.>\t<occursUntil>\t\"1999-##-##\"",
#     "<Corrado_Colombo>\t<playsFor>\t<U.C._Sampdoria>\t<occursSince>\t\"2002-##-##\"",
#     "<Corrado_Colombo>\t<playsFor>\t<U.C._Sampdoria>\t<occursUntil>\t\"2006-##-##\"",
#     "<Alphonse_Tchami>\t<isAffiliatedTo>\t<Odense_Boldklub>",
#     "<Abdulai_Bell-Baggie>\t<playsFor>\t<Tranmere_Rovers_F.C.>\t<occursSince>\t\"2012-##-##\"",
#     "<Abdulai_Bell-Baggie>\t<playsFor>\t<Tranmere_Rovers_F.C.>\t<occursUntil>\t\"2015-##-##\"",
#     "<Ferenc_Puskás>\t<isCitizenOf>\t<Greece>",
#     "<Myles_Weston>\t<isAffiliatedTo>\t<Charlton_Athletic_F.C.>",
#     "<Nathan_Blake>\t<playsFor>\t<Bolton_Wanderers_F.C.>\t<occursSince>\t\"1995-##-##\"",
#     "<Nathan_Blake>\t<playsFor>\t<Bolton_Wanderers_F.C.>\t<occursUntil>\t\"1998-##-##\""
# ]

from tqdm import tqdm

# Parsing Function
def parse_triples(file_path):
    triples = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split('\t')
            # print(parts)
            triple = {
                "subject": parts[0].strip('<>'),
                "predicate": parts[1].strip('<>'),
                "object": parts[2].strip('<>\n'),
                "since": None,
                "until": None
            }
            if len(parts) > 3:
                for i in range(3, len(parts), 2):
                    if "occursSince" in parts[i]:
                        triple["since"] = int(parts[i + 1].strip('"-#\n'))
                        # print("since: ",int(parts[i + 1].strip('"-#\n')))
                    elif "occursUntil" in parts[i]:
                        triple["until"] = int(parts[i + 1].strip('"-#\n'))
                        # print("until: ", int(parts[i + 1].strip('"-#\n')))
            triples.append(triple)
    # # print("triples: ",triples)
    return triples


# Grouping Function
def generate_snapshots(triples, year_groups):
    # print("in generate_snapshots")
    # snapshots = {group: [] for group in year_groups}
    snapshots = {group: set() for group in year_groups}
    subjects_with_dates = {}
    triples_with_dates = {}
    # print("triples: ",triples)
    for triple in triples:
        triple_str = triple['subject']+','+triple['predicate']+','+triple['object']
        for group in year_groups:
            group_key = str(group)
            if group_key not in triples_with_dates:
                triples_with_dates[group_key] = set()
            if group_key not in subjects_with_dates:
                subjects_with_dates[group_key] = set()
            if ((triple['since'] is not None and triple['since'] >= group[0] and triple['since'] <= group[1]) or
                    (triple['until'] is not None and triple['until'] <= group[1] and triple['until'] >= group[0])): #or
                    # (triple['since'] is not None and triple['since'] <= group[0]) or
                    # (triple['until'] is not None and triple['until'] >= group[1])):
                # subjects_with_dates.add(triple['subject'])
                subjects_with_dates[group_key].add(triple['subject'])
                triples_with_dates[group_key].add(triple_str)
    # print("final triples_with_dates: ",triples_with_dates)

    #for triple in triples:
    for triple in tqdm(triples, desc="Processing triples"):

        # always_include = triple['since'] is None and triple['until'] is None
        for group in year_groups:
            # if((triple['since'] is not None and triple['since'] >= group[0] and triple['since'] <= group[1]) or
            #         (triple['until'] is not None and triple['until'] <= group[1] and triple['until'] >= group[0])):
            #     subjects_with_dates.add(triple['subject'])

            # # print("triple: ",triple)
            # # print("group: ", group)
            # # print(group[0])
            # if always_include or (triple['since'] is not None and triple['since'] <= group[-1]) and (
            #         triple['until'] is None or triple['until'] >= group[0]):
            # if triple['subject'] in subjects_with_dates:
            #     continue  # Skip subjects that have any dates
            triple_str = triple['subject'] + ',' + triple['predicate'] + ',' + triple['object']
            # print("str(triple): ", triple_str)
            always_include = triple['since'] is None and triple['until'] is None
            # print("triple: ",triple)
            # print("str(group): ",str(group))
            # print("always_include_before: ",always_include)
            # print("triples_with_dates.keys(): ",triples_with_dates.keys())
            # print("triples_with_dates[str(group)]: ",triples_with_dates[str(group)])
            subjects_with_dates_values = set()
            triples_with_dates_values = set()
            flag = False
            for s in triples_with_dates.values():
                triples_with_dates_values.update(s)
            for s in subjects_with_dates.values():
                subjects_with_dates_values.update(s)
            # print("triples_with_dates_values: ",triples_with_dates_values)
            if str(group) in triples_with_dates.keys():
                # print("in if  triples_with_dates.values(): ",triples_with_dates_values)
                # if triple['subject'] in subjects_with_dates_values:
                if triple_str in triples_with_dates_values or triple['subject'] in subjects_with_dates_values:
                    # print("always_include = False")
                    always_include = False
                    # flag = True
            # print("always_include_after: ", always_include)

            # if triple['subject'] in subjects_with_dates[str(group)]:
            #     always_include = False

            # print("str(group): ",str(group))
            if ((triple['since'] is not None and triple['since'] >= group[0] and triple['since'] <= group[1]) or
                    (triple['until'] is not None and triple['until'] <= group[1] and triple['until'] >= group[0]) or
                    (triple_str in triples_with_dates[str(group)] and triple['subject'] in subjects_with_dates[str(group)])):
                # str_for_triple_since_and_until = '(' + triple['since'] + ', ' + triple['until'] + ')'
                flag = True
                # # print("str_for_triple_since_and_until: ",flag)
            # print("are these same? ", flag)
            # print("triple['subject']: ",triple['subject'])


            # if str(group) in triples_with_dates.keys():
            #     # print("triples_with_dates[str(group)]: ", triples_with_dates[str(group)])
            #     # if triple['subject'] in subjects_with_dates[str(group)]:
            #     if triple_str in triples_with_dates[str(group)]:
            #         # print("bingo")

            # if str(group) in subjects_with_dates.keys():
            if (always_include or (triple['since'] is not None and triple['since'] >= group[0] and triple['since'] <= group[1]) or
                    (triple['until'] is not None and triple['until'] <= group[1] and triple['until'] >= group[0]) or
                    # (triple['subject'] in subjects_with_dates[str(group)] and flag)):
                    (triple_str in triples_with_dates[str(group)] or flag) or
                    (triple['subject'] in subjects_with_dates[str(group)] and triple['since'] is None and triple['until'] is None)): # or
                    # (triple['since'] is not None and triple['since'] <= group[0]) or
                    # (triple['until'] is not None and triple['until'] >= group[1])):
                    # snapshots[group].append(triple)
                    triple_tuple = (triple['subject'], triple['predicate'], triple['object'])
                    snapshots[group].add(triple_tuple)
                    # print("always_includeaaaaa: ",always_include)
            # else:
            #     if (always_include or (triple['since'] is not None and triple['since'] >= group[0] and triple['since'] <= group[1]) or
            #             (triple['until'] is not None and triple['until'] <= group[1] and triple['until'] >= group[0])):
            #             # snapshots[group].append(triple)
            #             triple_tuple = (triple['subject'], triple['predicate'], triple['object'])
            #             snapshots[group].add(triple_tuple)
            #             # print("always_includeaaaaa: ",always_include)
    return snapshots

def parse_year_ranges(file_path):
    with open(file_path, 'r') as file:
        data = file.read().strip()

    year_groups = []
    ranges = data.split('\n')
    for range_str in ranges:
        years = list(map(int, range_str.split(',')))
        start_year = years[0]
        end_year = years[-1]
        year_groups.append((start_year, end_year))

    return year_groups

file_path = "timegroups"  # Replace with the path to your file
year_groups = parse_year_ranges(file_path)
# print(year_groups)
# print(len(year_groups))

# Define Year Groups
# year_groups = [(1893, 1939), (1940, 1969), (1970, 1986), (1987, 2002), (2003, 2017)]

# Parse the data
# file_path = "yago15k_trainaaaa.csv"
file_path = "dataset/myYagoDataset.csv"
# file_path = "dataset/yago15k_train.csv"
triples = parse_triples(file_path)

# Generate Snapshots
snapshots = generate_snapshots(triples, year_groups)

# # print the Results
for group, snapshot in snapshots.items():
    # print(f"Snapshot for years {group}:")
    group_name = f"{group[0]}_{group[1]}"
    output_file_path = f"/home/prachi/PycharmProjects/Anonymization/snapshots/snapshots_yago_big_dataset/snapshot_{group_name}.tsv"
    with open(output_file_path, 'w') as output_file:
        for snapshot in snapshots[group]:
            output_file.write(f"<{snapshot[0]}>\t<{snapshot[1]}>\t<{snapshot[2]}>\n")

    # print(f"Snapshot for years {group_name} has been written to {output_file_path}.")

#for group, snapshot in snapshots.items():
    # print(f"Snapshot for years {group}:")

  #  for triple in snapshot:
        # print(f"  {triple}")

