# -*- coding: utf-8 -*-
import os
import pdb
import sys

sys.path=[os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'./pdfminer'))]+sys.path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar

a=raw_input('enter the file name:\n')
if len(a)<1: a='HB.pdf'
fp=open(a,'rb')
parser=PDFParser(fp)
doc=PDFDocument(parser)
rs=PDFResourceManager()

lapara=LAParams()
device=PDFPageAggregator(rs, laparams=lapara)
inte=PDFPageInterpreter(rs, device)

name=None
ID=None
state=None
phone=None
a=[]

for page in PDFPage.create_pages(doc):
    inte.process_page(page)
    layout=device.get_result()
    count=0
    # pdb.set_trace()
    state_index = None
    phone_index = None
    for x in layout:
        if name and ID and state and phone:
            break

        count+=1
        if not isinstance(x,LTTextBox):
            continue
        line=x.get_text()
        textline=line[:]
        a.append(textline)

        if u"婚姻状况" in line:
            state_index = count + 1
        elif u"手机号码" in line:
            phone_index = count + 2
     
        # print count, line
        if count==10 and name==None:
            name=line[:len(line)/2]
        elif count==12 and ID==None:
            ID=line[:line.find(' ')]
        elif count==state_index and state==None:
            state=line[:len(line)/2]
        elif count==phone_index and phone==None:
            phone=line[:line.find(' ')]


print 'name:',name
print 'ID:',ID
print 'state',state
print 'phone',phone

#print a

