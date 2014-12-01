import json
import os

directory = '/home/david/git/cse_6242_PCA_Vis/dimension_reduction_code'
json_file = directory + '/12_samples_json_truncated_to_strain_375.JSON'

reduced_data = []
with open(json_file, 'rb') as f:
    for line in f:
        reduced_data.append(json.loads(line))

reduced_data_names = sorted(reduced_data[0].keys())
directory_property = directory + '/Data/Load_Strain_and_Crystallinity'


def _get_pic_suffix(sample_name, time):
    zeros = '_0000'
    time_str = str(time)
    return sample_name + zeros[:-len(time_str)] + time_str + '.png'

file_names = sorted(os.listdir(directory_property))
dict_list = []
name_index = 0
for file_name in file_names:
    f = open(os.path.join(directory_property, file_name), 'rb')
    data = f.readlines()
    data_cleaned = [i[:-1] for i in data]
    split_data = [i.split('\t') for i in data_cleaned]
    pt_index = 0
    for pt in split_data[1:]:
        pt_dict = {}
        sample_name = reduced_data_names[name_index]
        pt_dict['sample'] = sample_name
        pt_dict['time'] = pt_index
        pic_name = _get_pic_suffix(sample_name, pt_index)
        pt_dict['pic'] = pic_name
        points = reduced_data[0][sample_name][pt_index]
        pt_dict['points'] = reduced_data[0][sample_name][pt_index]
        pt_dict['percent_crystallinity'] = float(pt[0])
        pt_dict['percent_orthorhombic'] = float(pt[1])
        pt_dict['percent_monoclinic'] = float(pt[2])
        pt_dict['Load_in_Kgs'] = float(pt[3])
        pt_dict['strain'] = float(pt[4])
        dict_list.append(pt_dict)
        pt_index += 1
    name_index += 1


with open(os.path.join(directory, 'Vis_data.json'), 'w') as json_file:
    json.dump(dict_list, json_file)
