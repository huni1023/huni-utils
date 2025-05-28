import os

def check_prerequisite_dir(
        upper_dir: str,
        folder_name_ls: list,
    ) -> bool:
    r"""
    check validity of folder existance under target directory
    
    Motivation
    -------
    The secured data file is often protected as `.gitignore` with `*.csv`, `*.xlsx` command line.
    It makes us hard to replicate methods in other device since all dependency directory like `data`, `result` is hidden when right after `git pull`.
    So, this method can verify lower directory of python project and relieve misunderstand when trying to replicate project.
    

    Parameters
    ---------
    upper_dir: str
        main directory
    folder_name_ls: list
        check folders in `upper_dir`, if folders are not existed, create folder
    """
    for fld in folder_name_ls:
        if not os.path.isdir(os.path.join(upper_dir, fld)):
            os.mkdir(os.path.join(upper_dir, fld))
    return True

def clear_folder(folder_dir: str, extension: str, **kwargs):
    r"""
    remove all files in specific folder with extension

    Parameters
    ----------
    folder_dir: str
        directory of folder
    extension: str
        target extension

    Keywargs
    --------
    starts_with: str
        first N string condition
    extra_kw: str
        insert option with keyword contain
        예) extra_kw = "-설문" --> 설문이 안들어있는 파일만 고름
        예2 extra_kw = "설문" --> 설문이 들어있는 파일만 고름
    """
    fle_ls = list()
    if os.path.isdir(folder_dir):
        for fle in os.listdir(folder_dir):
            if fle.endswith(extension):
                fle_ls.append(fle)

    if 'starts_with' in kwargs.keys():
        search_key = kwargs['starts_with']
        len_search_area = len(search_key)
        fle_ls = [fle for fle in fle_ls if fle[:len_search_area] == search_key]

    if 'extra_kw' in kwargs.keys():
        if kwargs['extra_kw'][0] == '-':
            fle_ls = [fle for fle in fle_ls if kwargs['extra_kw'][1:] not in fle]
        else:
            fle_ls = [fle for fle in fle_ls if kwargs['extra_kw'] in fle]
    
    [os.remove(os.path.join(folder_dir, fle)) for fle in fle_ls]
    return True

def split_task(
        task_ls: list,
        n_worker = 8
    ) -> list:
    r"""
    split function as chunk

    Motivation
    ----------
    when multiprocessing python task,
    due to limit of cpu count, not all tasks cannot be inserted at once
    so, spliting task as chunk can change 
    """
    sliced_task = [task_ls[i:i+n_worker] for i in range(0, len(task_ls), n_worker)]
    return sliced_task

def search_file(
        main_dir: str,
        extension: str
    ) -> list:
    r"""
    search specific files in hierarchical directory

    Parameters
    ----------
    main_dir: str
        directory where to search
    extension: str
        extension of target files with dot or not
    """
    if os.path.isfile(main_dir):
        raise OSError('invalid input, input directory not a file')
    
    matched_fle_ls = list()
    for root, dirs, files in os.walk(main_dir):
        for f in files:
            if f.endswith(extension):
                fullpath = os.path.join(root, f)
                matched_fle_ls.append(fullpath)
    return matched_fle_ls
