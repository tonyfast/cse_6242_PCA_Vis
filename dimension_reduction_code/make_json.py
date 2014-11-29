import json
import os

directory = '/home/david/git/cse_6242_PCA_Vis/dimension_reduction_code'

json_file = directory + '/Data/Json_Files/12_samples_json_' + \
    'truncated_to_strain_375.JSON'

reduced_data = []
with open(json_file, 'rb') as f:
    for line in f:
        reduced_data.append(json.loads(line))

reduced_data_names = sorted(reduced_data[0].keys())

directory_property = directory + '/Data/Load_Strain_and_Crystallinity'

file_names = sorted(os.listdir(directory_property))
dict_list = []
name_index = 0
for file_name in file_names:
    f = open(os.path.join(directory_property, file_name), 'rb')
    data = f.readlines()
    data_cleaned = [i[:-1] for i in data]
    split_data = [i.split('\t') for i in data_cleaned]
    converted_data = map(list, zip(*split_data))
    key = reduced_data_names[name_index]
    dict_list.append({'sample': key})
    dict_list.append({'points': reduced_data[0][key]})
    name_index += 1
    [dict_list.append({prop[:1][0]: prop[1:]}) for prop in converted_data]

with open(os.path.join(directory, 'Vis_data.json'), 'w') as json_file:
            json.dump(dict_list, json_file)
