


def create_text(lines):
    for l in lines:


# ====================================
# MAIN
# ====================================
def main(sourcedir, targetdir, params):
    print("running: frq_to_plain")
    print(f"source format: {params['format']}")
    for file in sourcedir.glob("*.csv"):
        with file.open("r") as f:
            print(f"--{file.stem}")
            lines = f.read().splitlines()
            create_text(lines)
            df = read_tdm(file)
            pos_set = get_pos(params["filter"], df.pos)
            text = create_text(df[df.pos.isin(pos_set)], params)
            outfile = get_outfile(file, targetdir)
            write_to_file(outfile, text)


if __name__ == "__main__":
    main(formatsdir, sourcedir, params)
