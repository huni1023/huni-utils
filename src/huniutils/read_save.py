import os
import pickle
import yaml
import pandas as pd
import warnings

def read_pkl(pickle_file_path: str):
    r"""read pickle file"""
    assert type(pickle_file_path) == str

    pk = open(pickle_file_path, 'rb')
    pk_obj = pickle.load(pk)
    pk.close()
    return pk_obj

def save_pkl(file_dir: str, py_file) -> bool:
    r"""save pickle file"""
    assert type(file_dir) == str

    if file_dir.endswith('.pkl') == False:
        file_dir = file_dir + '.pkl'
        warnings.warn(f'huni-utils automatically add file extension as ".pkl": {file_dir}')

    with open(file_dir, 'wb') as handle:
        pickle.dump(py_file, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return True

def read_yaml(yaml_dir: str) -> dict:
    r"""
    read yaml file
    
    Note
    ----
    - handle korean character (24.03.18)
        - ref: https://powerofsummary.tistory.com/236
    """
    assert os.path.isfile(yaml_dir)
    assert yaml_dir.endswith(".yaml"), f"file must end with yaml, {yaml_dir}"

    with open(yaml_dir, 'rb') as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print("Parsing YAML string failed")
            print("Reason:", e.reason)
            print("At position: {0} with encoding {1}".format(e.position, e.encoding))
            print("Invalid char code:", e.character)
            raise ValueError
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
        name of extension
    """
    if extension not in 'csv xlsx'.split():
        raise ValueError('invalid argument')
    
    fle_ls = list()
    for fle in os.listdir(folder_dir):
        if fle.endswith(extension):
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
