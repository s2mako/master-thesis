# =================================
# Import statements
# =================================

import numpy as np
import pandas as pd


# ====================================
# FUNCTIONS
# ====================================

@np.vectorize  # nifty pythonic way to apply a function on a returned value
def extract_token_component(raw_tokens, idx):
    """
    Returns a vector of strings
    """
    return raw_tokens.split("_")[idx]


def read_tdm(file):
    """
    Separates "token_POS_lemma" to 3 dedicated columns
    """
    df = pd.read_csv(file)
    df.rename(columns={"Unnamed: 0": "token"}, inplace=True)  # gives first column the name "token"
    # tranform vetors to a column
    tokens = df.token
    df["token"] = extract_token_component(tokens, 0)
    df["pos"] = extract_token_component(tokens, 1)
    df["lemma"] = extract_token_component(tokens, 2)
    return df


def create_text(df, params):
    """
    Creates a generator of tokens multiplied by their frequency
    Warning: Big text files may take very long to process
    """
    # reduce df to bare necessities. token is index now. every row is a pure int vector.
    df = df.set_index("token").drop(columns=['pos', 'lemma'] + [col for col in df.columns if col.endswith('_sum')])
    seg_split = ""
    # each column represents a segment
    for col in df.columns:
        yield seg_split  # is an empty string in first iteration
        if params["seglen"] > 0: seg_split = "<SEG>\n"
        # rows for current col
        for t, i in df[col].iteritems():
            for j in range(i):
                # extract multiplier for current token in current column
                yield t
                yield "\n"


def write_to_file(outfile, strings):
    with outfile.open("w", encoding="utf-8") as f:
        for s in strings:
            f.write(s)


def get_outfile(file, targetdir):
    targetdir.mkdir(exist_ok=True, parents=True)
    return targetdir.joinpath(file.stem + ".txt")


def get_pos(filter, pos):
    """
    Creates a duplicate-free set of filtered pos
    """
    return set([str for str in pos
                if any(sub in str for sub in filter)])


# ====================================
# MAIN
# ====================================
def main(sourcedir, targetdir, params):
    print("csv_to_plain")
    print(f"target format: {params['format']}")
    for file in sourcedir.glob("*.csv"):
        print(f"--{file.stem}")
        df = read_tdm(file)
        pos_set = get_pos(params["filter"], df.pos)
        text = create_text(df[df.pos.isin(pos_set)], params)
        outfile = get_outfile(file, targetdir)
        write_to_file(outfile, text)


if __name__ == "__main__":
    main(formatsdir, sourcedir, params)
