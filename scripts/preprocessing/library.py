def segmenting(doc, seglen):
    if seglen is None:
        return doc
    segments = [doc[i: i + seglen] for i in range(0, len(doc), seglen)]
    return segments