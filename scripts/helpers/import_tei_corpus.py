from pathlib import Path

import pandas as pd

from helpers.TEIFile import TEIFile


def extract_text(tei_file, plainfolder):
    file_name = tei_file.filename.stem + ".txt"
    plain_text = Path.joinpath(plainfolder, file_name)
    if tei_file.text is not None:
        with plain_text.open("w", encoding="utf-8") as f:
            f.write(tei_file.text)


def tei_to_csv_entry(tei):
    print(f"Handled {tei}")
    base_name = (tei.filename.stem)
    return base_name, tei.authors[0].firstnames, tei.authors[0].lastname, tei.title, tei.date


def main(teifolder, plainfolder):
    teifolder = Path(teifolder)
    files = []
    csv_entries = []
    for xml in teifolder.glob("*.xml"):
        print(f"processing: {xml.stem}")
        tei_file = TEIFile(xml)
        entry = tei_to_csv_entry(tei_file)
        extract_text(tei_file, plainfolder)
        files.append(TEIFile(xml))
        csv_entries.append(entry)
    result_csv = pd.DataFrame(csv_entries, columns=["Filename", "Lastname", "Firstnames", "Title", "Date"])
    result_csv.to_csv(r"tei\metadata.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    main(r"tei\xml", Path(r"tei\plain"))
