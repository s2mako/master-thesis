from os.path import exists, join


def check_outfile_path(srcfolder, params):
    seglen = params["seglen"]
    filename = f"src-{seglen}.txt"
    outfile_path = join(srcfolder, filename)
    if exists(outfile_path):
        print("--clearing existing file: " + filename)
        f = open(outfile_path, "w")
        f.close()
    return outfile_path