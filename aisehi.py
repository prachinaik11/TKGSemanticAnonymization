#added 14feb
num_valid_groups = 0
new_SE_groups = {}
new_SA_groups = {}
non_unique_SAs_per_group = []
new_index = 0
temp_group = []
#print("new_SE_groups: ",new_SE_groups)
#print("new_SE_groups: ",len(new_SE_groups))
#print("new_SA_groups: ",new_SA_groups)
#print("new_SA_groups: ",len(new_SA_groups))
#print("new_index: ",new_index)

# print("INVALID GROUPS : ")
invalid_to_valid_groups = {}
valid_groups_with_count_of_nodes = {}
count_for_node_keys = {}  # added on 6May
fake_nodes = 0
discarded_entries = 0
VtU_num = 0    #### Doesn't contain fake nodes as of now



# countries_sum = 0
# ages_sum = 0
# alumniOf_sum = 0
all_category_sum = defaultdict(lambda: 0)  ### has total sum for all predicates
# print("all_category_sum", all_category_sum)

# all_countries = set()
# all_ages = set()
# all_alumniOfs = set()
all_category_sets = defaultdict(set)   ### has all unique values for each tag(predicate)



# category_sets = defaultdict(set)

pattern = r'<([^>]+)>([^,<]+)'



for group in groups:
    num_of_nodes_in_a_group = len(group)
    node_key = ""
    node_val = ""

    # country_set = set()
    # age_set = set()
    # alumni_of_set = set()
    # lang_spoken_set = set()

    # Dictionary to hold sets for each category
    category_sets = defaultdict(set)  ### for each group, it contains all attributes shared within that group for each predicate

    unique_SA = set()
    fake_nodes_in_a_group = 0

    non_unique_SAs_per_group = []   #added 14feb
    # temp_group = []  #added 14feb
    temp_group = group   #added 14feb

    print("\n New group of ", len(group))


    for i in group:
        print("i: ",i, " ----SA: ",sentences_dict[i])
        unique_SA.add(sentences_dict[i])
        non_unique_SAs_per_group.append(sentences_dict[i])  #added 14feb
        matches = re.findall(pattern, i)
        for tag, value in matches:
            # print(f"Match Tag: {tag}, Value: {value}")
            category_sets[tag].add(value)

    # print("Category Sets:", category_sets)
    # category_strings = {tag: ', '.join(sorted(values)) for tag, values in category_sets.items()}
    category_strings = ', '.join(f"{tag}: Values: {', '.join(sorted(values))}" for tag, values in category_sets.items())
    print("Category Sets: ", category_strings)
    print("unique_SA: ", unique_SA)
    # for tag, values in category_sets.items():
    #     print(f"Tag: {tag}, Values: {', '.join(values)}")


    ####### cluster size less than k
    if len(group) < k:
      print("less than k")
      ######### cluster size less than k/2
      if len(group)< k/2:
        print("discarding group -- len<k/2")
        discarded_entries = discarded_entries + len(group)

      ######### cluster size more than k/2, less k
      else:
        VtU_num = VtU_num + len(group)
        #########  l-diversity not satisfied (SAs < l)
        if len(unique_SA) < l:
          print("l-diversity not satisfied --- selecting random SA which will satisfy l-diversity")

          fake_nodes_in_a_group = max( (l - len(unique_SA)) , (k -len(group)) )
          fake_nodes = fake_nodes + fake_nodes_in_a_group
          num_of_nodes_in_a_group = num_of_nodes_in_a_group + fake_nodes_in_a_group

          for i in range(0, fake_nodes_in_a_group):
            random_SA = random.choice(list(all_unique_SA))
            if random_SA in unique_SA:
              random_SA = random.choice(list(all_unique_SA))
            # print('random_SA:',random_SA)
            unique_SA.add(random_SA)
            non_unique_SAs_per_group.append(random_SA)  #added 14feb
            temp_group.append(group[0])  #added 14feb


          # node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
          node_key = category_strings
          node_val = unique_SA

          # print("new l : ",unique_SA)
          # # added on 6May
          if node_key not in count_for_node_keys:
            invalid_to_valid_groups[node_key] = node_val
            valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group
            count_for_node_keys[node_key] = 1
          else:
            count_for_node_keys[node_key] = count_for_node_keys[node_key] + 1
            node_key = node_key + "_" + str(count_for_node_keys[node_key])
            invalid_to_valid_groups[node_key] = node_val
            valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group


          # countries_sum = countries_sum + len(group) * (len(country_set) -1)
          # ages_sum = ages_sum +  len(group) * (len(age_set)-1)
          # alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
          # langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)

          for tag, value in matches:
            # print(f"Match Tag: {tag}, Value: {value}")
            all_category_sum[tag] = all_category_sum[tag] + len(group) * (len(category_sets[tag]) -1)
          print("all_category_sum", all_category_sum)

          #added 14feb
          print("temp_group: ",temp_group)
          print("non_unique_SAs_per_group: ",non_unique_SAs_per_group)
          new_SE_groups[new_index] = temp_group
          new_SA_groups[new_index] = non_unique_SAs_per_group
          new_index = new_index + 1

        #########  l-diversity satisfied, k not satisfied
        else:
          print("l-diversity satisfied, k not satisfied")
          fake_nodes_in_a_group = k -len(group)
          fake_nodes = fake_nodes + fake_nodes_in_a_group

          for i in range(0, fake_nodes_in_a_group):    #added 14feb
            random_SA = random.choice(list(all_unique_SA))
            if random_SA in unique_SA:
              random_SA = random.choice(list(all_unique_SA))
            #print('random_SA:',random_SA)
            unique_SA.add(random_SA)
            non_unique_SAs_per_group.append(random_SA)
            temp_group = group
            temp_group.append(group[0])  #added 14feb

          #added 14feb
          print("temp_group: ",temp_group)
          print("non_unique_SAs_per_group: ",non_unique_SAs_per_group)
          new_SE_groups[new_index] = temp_group
          new_SA_groups[new_index] = non_unique_SAs_per_group
          new_index = new_index + 1

          num_of_nodes_in_a_group = num_of_nodes_in_a_group + fake_nodes_in_a_group
          # node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
          node_key = category_strings
          node_val = unique_SA
          # print(node_key)
          # invalid_to_valid_groups[node_key] = node_val
          # valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group
          # # added on 6May
          if node_key not in count_for_node_keys:
            invalid_to_valid_groups[node_key] = node_val
            valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group
            count_for_node_keys[node_key] = 1
          else:
            count_for_node_keys[node_key] = count_for_node_keys[node_key] + 1
            node_key = node_key + "_" + str(count_for_node_keys[node_key])
            invalid_to_valid_groups[node_key] = node_val
            valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group


          # countries_sum = countries_sum + len(group) * (len(country_set) -1)
          # ages_sum = ages_sum +  len(group) * (len(age_set)-1)
          # alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
          # langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)
          for tag, value in matches:
            # print(f"Match Tag: {tag}, Value: {value}")
            all_category_sum[tag] = all_category_sum[tag] + len(group) * (len(category_sets[tag]) -1)
          print("all_category_sum", all_category_sum)



    ########## unique SAs less than l, k satisfied
    elif len(unique_SA) < l:
      print("l-diversity not satisfied --- selecting random SA which will satisfy l-diversity")
      VtU_num = VtU_num + len(group)
      fake_nodes_in_a_group = l - len(unique_SA)
      fake_nodes = fake_nodes + fake_nodes_in_a_group
      num_of_nodes_in_a_group = num_of_nodes_in_a_group + fake_nodes_in_a_group

      for i in range(0, fake_nodes_in_a_group):
        random_SA = random.choice(list(all_unique_SA))
        if random_SA in unique_SA:
          random_SA = random.choice(list(all_unique_SA))
        # print('random_SA:',random_SA)
        unique_SA.add(random_SA)
        non_unique_SAs_per_group.append(random_SA)  #added 14feb
        temp_group.append(group[0])  #added 14feb

      #added 14feb
      print("temp_group: ",temp_group)
      print("non_unique_SAs_per_group: ",non_unique_SAs_per_group)
      new_SE_groups[new_index] = temp_group
      new_SA_groups[new_index] = non_unique_SAs_per_group
      new_index = new_index + 1

      # node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
      node_key = category_strings
      node_val = unique_SA
      # print("new l : ",unique_SA)
      # invalid_to_valid_groups[node_key] = node_val
      # valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group
      # # added on 6May
      if node_key not in count_for_node_keys:
        invalid_to_valid_groups[node_key] = node_val
        valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group
        count_for_node_keys[node_key] = 1
      else:
        count_for_node_keys[node_key] = count_for_node_keys[node_key] + 1
        node_key = node_key + "_" + str(count_for_node_keys[node_key])
        invalid_to_valid_groups[node_key] = node_val
        valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group

      # countries_sum = countries_sum + len(group) * (len(country_set) -1)
      # ages_sum = ages_sum +  len(group) * (len(age_set)-1)
      # alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
      # langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)

      for tag, value in matches:
          all_category_sum[tag] = all_category_sum[tag] + len(group) * (len(category_sets[tag]) -1)
      # print("all_category_sum", all_category_sum)


    ######## cluster size more than 2k-1
    elif len(group) > (2*k-1):
      print(f"length of the group {len(group)} is more than 2k-1 --- splitting the group")
      num_of_groups = int(len(group) / k)
      # print("num_of_groups : ",num_of_groups)
      subgroups = [group[i:i + (k+1)] for i in range(0, len(group), (k+1))]
      # print(len(subgroups))
      groups.extend(subgroups)

    ######## Cluster is valid
    else:
      print("in else: Cluster is valid")
      # valid_groups.append(group)
      num_valid_groups = num_valid_groups + 1
      VtU_num = VtU_num + len(group)
      for i in group:
        # print(i+"---"+sentences_dict[i])
        unique_SA.add(sentences_dict[i])
      # node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
      node_key = category_strings
      node_val = unique_SA
      # invalid_to_valid_groups[node_key] = node_val
      # valid_groups_with_count_of_nodes[node_key] = len(group)
      # # added on 6May
      if node_key not in count_for_node_keys:
        invalid_to_valid_groups[node_key] = node_val
        valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group
        count_for_node_keys[node_key] = 1
      else:
        count_for_node_keys[node_key] = count_for_node_keys[node_key] + 1
        node_key = node_key + "_" + str(count_for_node_keys[node_key])
        invalid_to_valid_groups[node_key] = node_val
        valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group



      #added 14feb
      print("temp_group: ",temp_group)
      print("non_unique_SAs_per_group: ",non_unique_SAs_per_group)
      new_SE_groups[new_index] = temp_group
      new_SA_groups[new_index] = non_unique_SAs_per_group
      new_index = new_index + 1

      # countries_sum = countries_sum + len(group) * (len(country_set) -1)
      # ages_sum = ages_sum +  len(group) * (len(age_set)-1)
      # alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
      # langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)
      for tag, value in matches:
          all_category_sum[tag] = all_category_sum[tag] + len(group) * (len(category_sets[tag]) -1)
      # print("all_category_sum", all_category_sum)
    # print("----------------------------------------")

    for tag, value in matches:
      all_category_sets[tag] = all_category_sets[tag].union(category_sets[tag])
    # all_countries = all_countries.union(country_set)
    # all_ages = all_ages.union(age_set)
    # all_alumniOfs = all_alumniOfs.union(alumni_of_set)
    # all_langs = all_langs.union(lang_spoken_set)