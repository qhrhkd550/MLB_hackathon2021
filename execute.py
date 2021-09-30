import file_preprocessing as fp
import data_preprocessing as dp

import argparse

def executor(data_folder, xml_folder, json_folder):
    data_folder = data_folder
    file_dict = fp.take_file_path(data_folder)
    print(file_dict.items())

    # xml_folder = './XML'
    # for key in file_dict.keys():
    #    dataframe = fp.merge_excel_file(file_dict[key])
    #    dataframe = dp.header_update(dataframe)
    #    dp.groupby_mmsi(dataframe, xml_folder)

def main():
    parser = argparse.ArgumentParser(description='Hackaton')

    parser.add_argument('-f','--data_folder',required=True,help='Data file folder')

    args = parser.parse_args()

    data_folder = args.data_folder
    file_dict = fp.take_file_path(data_folder)
    print(file_dict.items())

    #xml_folder = './XML'
    #for key in file_dict.keys():
    #    dataframe = fp.merge_excel_file(file_dict[key])
    #    dataframe = dp.header_update(dataframe)
    #    dp.groupby_mmsi(dataframe, xml_folder)

if __name__ == '__main__':
    main()
