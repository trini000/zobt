# -*- coding: utf-8 -*- http://blog.csdn.net/warmb123/article/details/6193629
import os
import pdb
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

sys.path = [os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./pdfminer"))] + sys.path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar

fp = open("hb.pdf", "rb")  #打开pdf文件
parser = PDFParser(fp)      #用文件对象来创建一个pdf文档分类器
doc = PDFDocument(parser)   #创建一个pdf文档
rs = PDFResourceManager()   #创建pdf资源管理器来管理共享资源

#创建一个pdf设备对象
lapara = LAParams()  
device = PDFPageAggregator(rs, laparams=lapara)
inte = PDFPageInterpreter(rs, device)

#处理文档对象中每一页的内容
#doc.get_pages()获取page列表
#循环遍历列表，每次处理一个page的内容，
#这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括
#LTTextBox， LTFigure, ,LTImage,LTTextBoxHorizontal 等等   想要获取文本就获得对象的txt属性

for page in PDFPage.create_pages(doc):
        inte.process_page(page)
        layout = device.get_result()
        count = 0
        name = None
        id = None
        # pdb.set_trace()
        for x in layout:
                count += 1
                if not isinstance(x, LTTextBox):
                        continue
                line = x.get_text()
                # 很奇怪,似乎所有行的TextBox都包含2个重复的line...
                content = line.split("\n")[0]
                # print content
                # PDF太变态,最多只能这样安全检查一下..
                if count == 6:
                        assert u"被查询者姓名" in content
                elif count == 7:
                        assert u"被查询者证件类型" in content
                elif count == 8:
                        assert u"被查询者证件号码" in content
                elif count == 10:
                        # name box
                        name = line[:len(line)/2]
                elif count == 11:
                        # 检查必须身份证 (?)
                        assert u"身份证" in content
                elif count == 12:
                        # id box
                        id = line[:line.find(' ')]
                else:
                        if name is not None and id is not None:
                                break

        print u"终于特么找出来了:\n\t姓名 %s\n\t身份证号 %s\n" %(name, id)
        exit()


