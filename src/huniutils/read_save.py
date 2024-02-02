import os
import pickle
import yaml
import pandas as pd
import warnings

def read_pkl(pickle_file_path: str):
    r"""read pickle file"""
    pk = open(pickle_file_path, 'rb')
    pk_obj = pickle.load(pk)
    pk.close()
    return pk_obj

def save_pkl(file_dir: str, py_file) -> bool:
    r"""save pickle file"""
    if '.pkl' != file_dir[-4:]:
        warnings.warn(f'huni-utils automatically add file extension as ".pkl" ')
        file_dir = file_dir + '.pkl'

    with open(file_dir, 'wb') as handle:
        pickle.dump(py_file, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return True

def read_yaml(yaml_dir: str) -> dict:
    r"""read yaml file"""
    _, file_extension = os.path.splitext(yaml_dir)
    assert file_extension == '.yaml', 'only yaml file is allowed'
    with open(yaml_dir, encoding='utf-8') as cfg:
        config = yaml.safe_load(cfg)
    return config

def pandize_folder(folder_dir: str,
                     extension: str) -> bool:
    r"""
    convert all data to pickle at once

    Motivation
    -------
    once you get raw data as csv, tsv, sort of.. to enhance read speed and presever data is necessary
    
    Parameter
    ---------
    extension: str
        확장자명
    """
    if extension not in 'csv xlsx'.split():
        raise ValueError('invalid argument')
    
    fle_ls = list()
    for fle in os.listdir(folder_dir):
        if fle[-len(extension):] == extension:
            fle_ls.append(fle)
    if len(fle_ls) == 0:
        warnings.warn(f'check folder, data is not found: {extension}', UserWarning)
    
    data_ls = list()
    
    cleaned_fle_ls = list()
    for fle in fle_ls:
        if extension == 'csv':
            try:
                df = pd.read_csv(os.path.join(folder_dir, fle),
                                        keep_default_na=False # to preserve data as it was
                                        )
            except UnicodeDecodeError:
                warnings.warn(f'csv data encoding problem: {fle}')
                continue
        elif extension == 'xlsx':
            df = pd.read_excel(os.path.join(folder_dir, fle))    
        cleaned_fle_ls.append(fle)
        data_ls.append(df)
    
    assert len(data_ls) == len(cleaned_fle_ls)
    for df, fle in zip(data_ls, cleaned_fle_ls):
        pkl_fle = fle[:-len(extension)] + 'pkl'
        save_pkl(os.path.join(folder_dir, pkl_fle), df)
    return True

if __name__ == '__main__':
    print(1)