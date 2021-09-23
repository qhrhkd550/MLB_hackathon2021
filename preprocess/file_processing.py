import pandas as pd
import numpy as np
import pathlib

def take_file_path(data_path='./'):
    '''
    args:
        data_path    : data folder,
                       ./data/AIS_SH856/AIS_History_info.xlsx, AIS_History_info (1).xlsx ....
                       data_path='./data'
    output:
        file_dict    : dict, Key : ship code, Value: excel file path list
                       file_dict[AIS_SH856][file_path.xlsx, file_path.xlsx, ...]
    '''
    import pathlib
    file_dict = {}
    p = pathlib.Path(data_path)
    for folder in p.iterdir():
        if folder.is_dir() and folder.match('AIS*'):
            _folder_name = folder.name
            _file_list = []
            for file in pathlib.Path(folder).rglob('*.xlsx'):
                file_abs_path = str(file.resolve())
                #print(file_abs_path)
                _file_list.append(file_abs_path)

            file_dict[_folder_name] = _file_list
    return file_dict

def merge_excel_file(file_path_list):
    '''
    args:
        file_path_list    : excel file path list,
                            [file1.xlsx, file2.xlsx ...]
    output:
        df                : Pandas dataframe, removed duplicated data(by Seq No.)
                            *'Seq No.' must be last column.*
    '''
    df_list = []
    for _file in file_path_list:
        __data = pd.read_excel(_file,index_col=-1)
        df_list.append(__data)
    df = pd.concat(df_list)
    df = df.groupby(df.index).first()
    return df



if __name__ == '__main__':
    pass
