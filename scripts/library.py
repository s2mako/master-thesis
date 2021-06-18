from pathlib import Path

def segmenting(str_iterator, seglen):
    i = 0
    for s in str_iterator:
        if (i < seglen):
            yield s