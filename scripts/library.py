from os.path import exists, join

import pandas as pd


def check_outfile_path(srcfolder, params):
    seglen = params["seglen"]
    filename = f"src-{seglen}.txt"
    outfile_path = join(srcfolder, filename)
    if exists(outfile_path):
        print("--clearing existing file: " + filename)
        f = open(outfile_path, "w")
        f.close()
    return outfile_path


def get_topic_dfs(path, element="topic"):
    xpath = f"//{element}"
    dfs =[]
    if path.is_dir():
        for file in path.glob("*.xml"):
            df = pd.read_xml(file, xpath=xpath).drop(columns="id")
            dfs.append(df)
    elif path.is_file():
        df = pd.read_xml(path, xpath=xpath).drop(columns="id")
        dfs.append(df)
    return dfs