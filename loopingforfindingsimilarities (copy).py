# -*- coding: utf-8 -*-
"""loopingForFindingSimilarities

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IDyFJfysnT2MMm7jxQQ9VVDQbSFe1KG8
"""

# !pip install -U sentence-transformers
# !pip install scikit-learn-extra

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
df=pd.read_csv("dataset.csv")
# print(type(df.iloc[:, 0]))
all_dict = df.set_index('sentences').to_dict()
sentences_dict = all_dict.get('sensitiveAttr')

sentences = list(sentences_dict.keys())

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

embeddings = model.encode(sentences, convert_to_tensor=True)

from sklearn_extra.cluster import KMedoids
import random
from math import comb


all_z = [3,4,5,6,7,8,9,10]
all_l = [2,3,4]

# all_z = [3]
# all_l = [2,3]
for l in all_l:
  for z in all_z:
    print(z," -- ",l)
    k = z
    # Use PCA to reduce the dimensionality to 2 for visualization
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)

    # Use K-Medoids clustering
    num_clusters = int(len(sentences_dict)/k)

    kmedoids = KMedoids(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmedoids.fit_predict(embeddings)

    # # Visualize clusters
    # plt.figure(figsize=(8, 6))
    # for i in range(num_clusters):
    #     cluster_points = reduced_embeddings[cluster_labels == i]
    #     plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i + 1}', alpha=0.7)

    # plt.title('Visualization of Sentence Embeddings with Clusters (PCA)')
    # plt.xlabel('Principal Component 1')
    # plt.ylabel('Principal Component 2')
    # plt.legend()
    # plt.show()

    # Create groups of three from each cluster
    groups = [[] for _ in range(num_clusters)]
    for i, sentence in enumerate(sentences):
        cluster_index = cluster_labels[i]
        groups[cluster_index].append(sentence)

    # Display groups
    #for i, group in enumerate(groups):
        #print(f'Group {i + 1}:', group)
        #print(f'Group {i + 1} size:', len(group))

    valid_groups = []
    invalid_groups = []
    all_unique_SA = set()

    for group in groups:
      #print(len(group))
      unique_SA = set()
      for i in group:
        #print(i)
        unique_SA.add(sentences_dict[i])
        all_unique_SA.add(sentences_dict[i])
      #print("Unique l values : ",unique_SA)
      if len(unique_SA) >= l and len(group) >= k and len(group) <= (2*k-1):
        valid_groups.append(group)
      else:
        invalid_groups.append(group)
      #print("------------------------------------------")

    #print("VALID GROUPS : ")
    #for group in valid_groups:
      #print(group)


    #added 14feb
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


    #added 14feb
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



    #print("INVALID GROUPS : ")
    invalid_to_valid_groups = {}
    valid_groups_with_count_of_nodes = {}
    fake_nodes = 0
    discarded_entries = 0

    countries_sum = 0
    ages_sum = 0
    alumniOf_sum = 0
    langs_sum = 0
    VtU_num = 0

    all_countries = set()
    all_ages = set()
    all_alumniOfs = set()
    all_langs = set()

    for group in groups:

      num_of_nodes_in_a_group = len(group)
      node_key = ""
      node_val = ""
      country_set = set()
      age_set = set()
      alumni_of_set = set()
      lang_spoken_set = set()
      unique_SA = set()
      non_unique_SAs_per_group = []   #added 14feb
      temp_group = []  #added 14feb
      temp_group = group   #added 14feb
      fake_nodes_in_a_group = 0

      for i in group:
        split_sentence = i.split(",")
        #print("i ---",split_sentence)

        unique_SA.add(sentences_dict[i])
        non_unique_SAs_per_group.append(sentences_dict[i])  #added 14feb
        country_set.add(split_sentence[0])
        age_set.add(split_sentence[1])
        alumni_of_set.add(split_sentence[2])
        lang_spoken_set.add(split_sentence[3])

      #### cluster size less than k
      if len(group) < k:
        #print("less than k")
        #### cluster size less than k/2, discard the group
        if len(group)< k/2:
          #print("discarding group -- len<k/2")      #################### Need to add new code for assigning these groups to valid groups here
          discarded_entries = discarded_entries + len(group)
        #### cluster size > k/2
        else:
          VtU_num = VtU_num + len(group)
          #### cluster size > k/2 and l-diversity not satisfied
          if len(unique_SA) < l:
            #print("l-diversity not satisfied --- selecting random SA which will satisfy l-diversity")

            fake_nodes_in_a_group = max( (l - len(unique_SA)) , (k -len(group)) )
            fake_nodes = fake_nodes + fake_nodes_in_a_group
            num_of_nodes_in_a_group = num_of_nodes_in_a_group + fake_nodes_in_a_group

            for i in range(0, fake_nodes_in_a_group):
              random_SA = random.choice(list(all_unique_SA))
              if random_SA in unique_SA:
                random_SA = random.choice(list(all_unique_SA))
              #print('random_SA:',random_SA)
              unique_SA.add(random_SA)
              non_unique_SAs_per_group.append(random_SA)  #added 14feb
              temp_group.append(group[0])  #added 14feb


            node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
            node_val = unique_SA
            #print("new l : ",unique_SA)
            invalid_to_valid_groups[node_key] = node_val
            valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group

            countries_sum = countries_sum + len(group) * (len(country_set) -1)
            ages_sum = ages_sum +  len(group) * (len(age_set)-1)
            alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
            langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)

            #added 14feb
            new_SE_groups[new_index] = temp_group
            new_SA_groups[new_index] = non_unique_SAs_per_group
            new_index = new_index + 1


          #### cluster size > k/2 and l-diversity satisfied
          else:
            #print("adding fake node")
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
            new_SE_groups[new_index] = temp_group
            new_SA_groups[new_index] = non_unique_SAs_per_group
            new_index = new_index + 1


            num_of_nodes_in_a_group = num_of_nodes_in_a_group + fake_nodes_in_a_group
            node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
            node_val = unique_SA
            invalid_to_valid_groups[node_key] = node_val
            valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group

            # countries_sum = countries_sum + num_of_nodes_in_a_group * len(country_set) -1
            # ages_sum = ages_sum +  num_of_nodes_in_a_group * len(age_set)-1
            # alumniOf_sum = alumniOf_sum + num_of_nodes_in_a_group* len(alumni_of_set)-1
            # langs_sum = langs_sum + num_of_nodes_in_a_group* len(lang_spoken_set)-1

            countries_sum = countries_sum + len(group) * (len(country_set) -1)
            ages_sum = ages_sum +  len(group) * (len(age_set)-1)
            alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
            langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)


      #### l-diversity not satisfied
      elif len(unique_SA) < l:
        #print("l-diversity not satisfied --- selecting random SA which will satisfy l-diversity")
        VtU_num = VtU_num + len(group)
        fake_nodes_in_a_group = l - len(unique_SA)
        fake_nodes = fake_nodes + fake_nodes_in_a_group
        num_of_nodes_in_a_group = num_of_nodes_in_a_group + fake_nodes_in_a_group

        for i in range(0, fake_nodes_in_a_group):
          random_SA = random.choice(list(all_unique_SA))
          if random_SA in unique_SA:
            random_SA = random.choice(list(all_unique_SA))
          #print('random_SA:',random_SA)
          unique_SA.add(random_SA)
          non_unique_SAs_per_group.append(random_SA)  #added 14feb
          temp_group.append(group[0])  #added 14feb

        #added 14feb
        new_SE_groups[new_index] = temp_group
        new_SA_groups[new_index] = non_unique_SAs_per_group
        new_index = new_index + 1


        node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
        node_val = unique_SA
        #print("new l : ",unique_SA)
        invalid_to_valid_groups[node_key] = node_val
        valid_groups_with_count_of_nodes[node_key] = num_of_nodes_in_a_group

        countries_sum = countries_sum + len(group) * (len(country_set) -1)
        ages_sum = ages_sum +  len(group) * (len(age_set)-1)
        alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
        langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)

      #### cluster size more than 2k-1
      elif len(group) > (2*k-1):
        #print(f"length of the group {len(group)} is more than 2k-1 --- splitting the group")
        num_of_groups = int(len(group) / k)
        #print("num_of_groups : ",num_of_groups)
        subgroups = [group[i:i + (k+1)] for i in range(0, len(group), (k+1))]
        #print(len(subgroups))
        groups.extend(subgroups)


      #### group satisfies k-anonimity and l-diversity
      else:
        #print("in else")
        # valid_groups.append(group)
        VtU_num = VtU_num + len(group)
        for i in group:
          #print(i+"---"+sentences_dict[i])
          unique_SA.add(sentences_dict[i])

        node_key = f" {country_set}, {age_set}, {alumni_of_set}, {lang_spoken_set}"
        node_val = unique_SA
        invalid_to_valid_groups[node_key] = node_val
        valid_groups_with_count_of_nodes[node_key] = len(group)

        #added 14feb
        new_SE_groups[new_index] = temp_group
        new_SA_groups[new_index] = non_unique_SAs_per_group
        new_index = new_index + 1


        countries_sum = countries_sum + len(group) * (len(country_set) -1)
        ages_sum = ages_sum +  len(group) * (len(age_set)-1)
        alumniOf_sum = alumniOf_sum + len(group)* (len(alumni_of_set)-1)
        langs_sum = langs_sum + len(group)* (len(lang_spoken_set)-1)
      #print("----------------------------------------")

      all_countries = all_countries.union(country_set)
      all_ages = all_ages.union(age_set)
      all_alumniOfs = all_alumniOfs.union(alumni_of_set)
      all_langs = all_langs.union(lang_spoken_set)

    m = z

    small_SE_avgs = 0
    small_SA_avgs = 0
    SE_similarity = 0
    SA_similarity = 0

    # Create groups of three from each cluster
    # groups = [[] for _ in range(num_clusters)]
    # for i, sentence in enumerate(sentences):
    #     cluster_index = int(labels[i])
    #     groups[cluster_index].append(sentence)

    groups = list(new_SE_groups.values())

    valid_groups_count = 0


    for i, group in enumerate(groups):
          # print(group)
          small_SE_avgs = 0

          unique_SA = set()
        # if len(group) >= m:
          # print((group))
          # print('size:', len(group))
          SE_embeddings = model.encode(group)

          for sentence_index in range(len(group)):
            # print(sentence_index)
            # print(group[sentence_index])
            unique_SA.add(sentences_dict[group[sentence_index]])
            for sentence_index1 in range(sentence_index+1, len(group)):
              small_SE_avgs = small_SE_avgs + util.cos_sim(SE_embeddings[sentence_index], SE_embeddings[sentence_index1])
          # print("small_SE_avgs/comb(len(group), 2) :",small_SE_avgs/comb(len(group), 2))


          SE_similarity = SE_similarity + small_SE_avgs/comb(len(group), 2)
          valid_groups_count = valid_groups_count + 1
          # print(unique_SA)

    groups1 = list(new_SA_groups.values())

    for i, group in enumerate(groups1):
          small_SA_avgs = 0
          SE_embeddings = model.encode(group)

          for sentence_index in range(len(group)):
            # print(sentence_index)
            # print(group[sentence_index])
            for sentence_index1 in range(sentence_index+1, len(group)):
              small_SA_avgs = small_SA_avgs + util.cos_sim(SE_embeddings[sentence_index], SE_embeddings[sentence_index1])
          SA_similarity = SA_similarity + small_SA_avgs/comb(len(group), 2)
          # print("small_SE_avgs/comb(len(group), 2) :",small_SE_avgs/comb(len(group), 2))
          # unique_SA_list = list(unique_SA)
          # SA_embeddings2 = model.encode(unique_SA_list)
          # for sentence_index in range(len(unique_SA_list)):
          #   for sentence_index1 in range(sentence_index+1, len(unique_SA_list)):
          #     # print(sentence_index1)
          #     small_SA_avgs = small_SA_avgs + util.cos_sim(SA_embeddings2[sentence_index], SA_embeddings2[sentence_index1])
          # # print(unique_SA_list)
          # if len(unique_SA_list) >= l:
          # # print(small_SA_avgs/comb(len(unique_SA_list), 2))
          #   SA_similarity = SA_similarity + small_SA_avgs/comb(len(unique_SA_list), 2)


    print(SE_similarity)
    print("valid_groups_count : ", valid_groups_count)
    print("len(groups) : ", len(groups))
    final_SE_similarity = SE_similarity / valid_groups_count
    final_SA_similarity = SA_similarity / valid_groups_count
    print("final_SE_similarity : ",final_SE_similarity)
    print("final_SA_similarity : ",final_SA_similarity)

    # number of users in anonymized KG
    # VtU_num = sum(valid_groups_with_count_of_nodes.values())
    print("VtU_num :",VtU_num)

    # number of user-attribute relationship types (country, age, alumniOf, languageKnown)
    RtUA_num = 4

    loss1 = (countries_sum/(len(all_countries)-1)) + (ages_sum/(len(all_ages)-1)) + (alumniOf_sum/(len(all_alumniOfs)-1)) + (langs_sum/(len(all_langs)-1))
    AL = loss1 / RtUA_num
    AAIL = AL / VtU_num
    print("AAIL :",AAIL)

    #fake_nodes
    #discarded_entries

    # number of users in union of set of users in anonymized KG and original KG
    Utu = len(sentences_dict) - discarded_entries + fake_nodes
    print(Utu)

    AIL = (AL + (fake_nodes+discarded_entries)) / Utu

    print("AIL :",AIL)

