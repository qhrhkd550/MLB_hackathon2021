import file_preprocessing as fp
import data_preprocessing as dp

import argparse

def executor(data_folder, xml_folder, json_folder):
    data_folder = data_folder
    file_dict = fp.take_file_path(data_folder)
    print(file_dict.items())

    xml_folder = xml_folder
    for key in file_dict.keys():
       dataframe = fp.merge_excel_file(file_dict[key])
       dataframe = dp.header_update(dataframe)
       dp.groupby_mmsi(dataframe, xml_folder, json_folder)

def main():
    parser = argparse.ArgumentParser(description='Hackaton')

    parser.add_argument('-f', '--data_folder',required=True,help='Data file folder')
    parser.add_argument('-x', '--xml_folder', required=True, help='XML file folder')
    parser.add_argument('-j', '--json_folder', required=True, help='JSON file folder')

    args = parser.parse_args()
    executor(args.data_folder, args.xml_folder, args.json_folder)

if __name__ == '__main__':
    main()
