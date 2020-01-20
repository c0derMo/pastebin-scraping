from html.parser import HTMLParser
import re

class Paste():
    def __init__(self):
        self.title = ""
        self.id = ""
        self.language = ""

class ArchiveParser(HTMLParser):
    inTable = False
    allElements = []
    postHeader = False
    inElement = False

    tdCount = 0

    def handle_starttag(self, tag, attrs):
        if tag == "table" and ('class', 'maintable') in attrs:
            self.inTable = True
        if self.inTable and tag == "tr" and not self.postHeader:
            self.postHeader = True
        if self.inTable and tag == "tr" and self.postHeader:
            self.inElement = True
            self.tdCount = 0

        if self.inElement and tag == "td":
            self.tdCount += 1
        
        if tag == "a" and self.tdCount == 1:
            self.allElements.append(attrs[0][1])
 
    def handle_endtag(self, tag):
        if self.inTable and tag == "table":
            self.inTable = False
        if self.inTable and tag == "tr" and self.inElement:
            self.inElement = False

    def handle_data(self, data):
        pass

class PasteParser(HTMLParser):
    def setup(self):
        self.title = ""
        self.language = ""
        self.user = ""
        self.creationdate = ""
        self.expiresat = ""
        self.content = ""

        self.nextData = ""
        self.insideBox2 = False
        self.insideBox3 = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "textarea" and ("id", "paste_code") in attrs:
            self.nextData = "content"
        if tag == "div" and ('class', 'paste_box_line1') in attrs:
            self.nextData = "title"
        if tag == "div" and ('class', 'paste_box_line2') in attrs:
            self.insideBox2 = True
            self.nextData = "user"
        if tag == "span" and self.insideBox2:
            for attr, val in attrs:
                if attr == "title":
                    self.creationdate = val
            self.nextData = "expires"
        if tag == "div" and ('id', 'code_buttons') in attrs:
            self.insideBox3 = True
        if tag == "span" and self.insideBox3 and ('class', 'go_right') not in attrs:
            self.nextData = "language"
    
    def handle_endtag(self, tag):
        if tag == "div" and self.insideBox2:
            self.insideBox2 = False
            self.nextData = ""
        if tag == "div" and self.insideBox3:
            self.insideBox3 = False
    
    def handle_data(self, data):
        if self.nextData == "content":
            self.content = data
            self.nextData = ""
        if self.nextData == "title":
            self.title = data
            self.nextData = ""
        if self.nextData == "user":
            r = re.compile("\s*\S+\s*")
            if not r.match(self.user):
                if data.startswith(' '):
                    self.user = data[1:].replace('\n', '')
                else:
                    self.user = data.replace('\n', '')
        if self.nextData == "expires":
            self.expiresat = data.replace('\n', '').replace(' ', '')
        if self.nextData == "language":
            self.language = data
            self.nextData = ""