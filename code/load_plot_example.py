import lasio
import re
import os
import json


def run_example(path_name):
    # Get the list of all files
    file_list = get_file_list(path_name)

    # extract data from each las file and add to a large dict
    las_info = get_las_info(file_list)

    # print(las_info)
    # las_json = json.dumps(las_info)
    # print(las_info)
    with open('well_log_data.txt', 'w') as outfile:
        json.dump(las_info, outfile)

    # extract data from formation tops

    # get name of pdf file?


def get_file_list(path_name):
    # Get list of sub-directories in path_name
    sub_dirs = [os.path.join(path_name, f) for f in os.listdir(path_name)
                if os.path.isdir(os.path.join(path_name, f))]

    # Get list of all files in all of the sub directories
    file_list = []
    for sub_dir in sub_dirs:
        files = [os.path.join(sub_dir, f) for f in os.listdir(
            sub_dir) if os.path.isfile(os.path.join(sub_dir, f))]
        file_list = files + file_list

    return file_list


def get_las_info(file_list):
    # loop through all the files, read the las file
    las_file_data = []
    p = re.compile('Well-(.+)_finished')
    # loop through the files
    for file_name in file_list:
        # get file name and directory info
        file_head, file_tail = os.path.split(file_name)
        # break file name into parts
        f, ext = os.path.splitext(file_tail)
        # Check if it is a LAS file
        if ext.upper() == '.LAS':
            dir_head, dir_tail = os.path.split(os.path.dirname(file_name))
            # try and load the las file
            try:
                las = lasio.read(file_name, ignore_data=True)

                # Check to see if the file has:
                temp_data = {"Depth": [], "Res": [], "Gamma": [],
                             "Well": [], "File_Name": []}
                flags = [0, 0, 0]
                data_cols = [0, 0, 0]

                #   depth in m
                #   deep res in ohm m
                #   gamma in api
                #   sonic dt in us per foot
                print('File: ', file_tail)
                for i, curve in enumerate(las.curves):
                    print("mnem: ", curve.mnemonic.lower(), ", curve: ", curve.unit.lower())
                    if ('dep' in curve.mnemonic.lower()) and ('m' in curve.unit.lower()) and (flags[0] == 0):
                        flags[0] = 1
                        data_cols[0] = i

                    elif ('ohm' in curve.unit.lower()) and (flags[1] == 0):
                        flags[1] = 1
                        data_cols[1] = i

                    elif ('api' in curve.unit.lower()) and (flags[2] == 0):
                        flags[2] = 1
                        data_cols[2] = i


                # print(flags)

                # Check to see if file has all the data we want
                if all(flags):
                    # Re-read file and grab the data
                    try:
                        las = lasio.read(file_name)
                        temp_data["Depth"] = las.data[:, data_cols[0]].tolist()
                        temp_data["Res"] = las.data[:, data_cols[1]].tolist()
                        temp_data["Gamma"] = las.data[:, data_cols[2]].tolist()
                        temp_data["Well"] = p.findall(dir_tail)[0]
                        temp_data["File_Name"] = file_tail
                        print(p.findall(dir_tail)[0])
                        las_file_data = las_file_data + [temp_data]

                    except:
                        las = []


#                   las_file_info = las_file_info + [{"Keys": las.keys(),
#                                                  "WellName": p.findall(dir_tail)[0],
#                                                  "Curves": las.curves,
#                                                  "Version": las.version,
#                                                  "Well": las.well,
#                                                  "Params": las.params,
#                                                  "FileName": file_tail}]
            except lasio.exceptions.LASHeaderError:
                # Skip file
                las = []

    return las_file_data


if __name__ == "__main__":
    path_name = "../../data/EAGE2018"
    run_example(path_name)
