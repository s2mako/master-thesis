# https://komax.github.io/blog/text/python/xml/parsing_tei_xml_python/
import re
from xml.etree import ElementTree as ET

from helpers.Author import Author


def read_tei(tei_file):
    with open(tei_file, 'r') as tei:
        tree = ET.parse(tei)
        return tree.getroot()
    raise RuntimeError('Cannot generate a tree from the input')


def elem_to_text(elem, default=''):
    if elem:
        return elem.getText()
    else:
        return default

class TEIFile(object):
    def __init__(self, filename):
        self.ns = {"xmlns": "http://www.tei-c.org/ns/1.0"}
        self.filename = filename
        self.root = read_tei(filename)
        self._text = None
        self._title = ''
        self._date = ''

    @property
    def title(self):
        if not self._title:
            xpath = ".//xmlns:titleStmt/xmlns:title"
            self._title = self.root.find(xpath, self.ns).text
        return self._title

    @property
    def date(self):
        if not self._date:
            xpath = ".//xmlns:bibl[@type='firstEdition']//xmlns:date"
            self._date = self.root.find(xpath, self.ns).text
        return str(self._date)

    @property
    def authors(self):
        authors_in_header = self.root.findall(".//xmlns:titleStmt/xmlns:author", self.ns)
        result = []
        # need to extract authors name
        for author in authors_in_header:
            p_fullname = re.compile("(^.+)?(?=\s+\()")
            p_partial = re.compile("^(\w+\-?\w+),\s(.+)")
            mo1 = p_fullname.search(author.text)
            fullname = mo1.group(1)
            mo2 = p_partial.search(fullname)
            lastname = mo2.group(1)
            firstnames = mo2.group(2)
            author = Author(lastname, firstnames)
            result.append(author)
        return result


    @property
    def text(self):
        if not self._text:
            divs_text = []
            liminal_xp = ".//xmlns:text//xmlns:div[@type='liminal']"
            body_xp = ".//xmlns:text//xmlns:body"
            liminalnode = self.root.find(liminal_xp, self.ns)
            bodynode = self.root.find(body_xp, self.ns)
            if liminalnode:
                for text in liminalnode.itertext():
                    divs_text.append(text)
            for text in bodynode.itertext():
                divs_text.append(text)
            plain_text = " ".join(divs_text)
            self._text = plain_text
        return self._text
