import os

def pjoin(*args) -> str:
    r"""
    it works same as 'os.path.join' but it's more shorter!

    Purpose
    -------
    When automating job or processing scattered files, there are lots of needs to exactly parse directory on the device.
    Utilizing simplistic path-calling method (e.g. `df=pd.read_csv('data.csv')`) might leads to OSError when excuting python scripts in various senarios,
    such as calling the script directly, excuting it in a Jupyter notebook, or invoking it on other python file.

    To address this issue, I emphasized the use of `os.path.join` to explicitly define path,
    aiming to minimize redundant instances of this function.
    """
    combined_path = ""
    for p in args:
        assert type(p) == str, "string input allowed"
        combined_path = os.path.join(combined_path, p)
    return combined_path


if __name__ == '__main__':
    print(pjoin(os.getcwd(), 'sample'))