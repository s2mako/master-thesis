# =================================
# Import statements
# =================================


# ====================================
# FUNCTIONS
# ====================================



# ====================================
# MAIN
# ====================================
def main(tknsource, tknpseudodir):
    print("tkn_to_plain")
    for file in tknsource.glob("*.txt"):
        write_to_file(tknpseudodir, file, read(file))
