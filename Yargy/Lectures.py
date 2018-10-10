from docx import Document
import yargy
import os
import copy
from yargy import Parser, rule, and_, or_
from yargy.predicates import gram, is_capitalized, dictionary, is_upper, length_eq


class LecturePaser:

    def __init__(self,name=None):
        self.section_rule = rule(
            dictionary(
                {
                    "раздел", "тема", "дисциплина", "наименование"
                }
                        ))
        self.docxdoc=DocumentPrepare(name)


    def sections(self):
        pars = Parser(self.section_rule)
        '''
        идея в том, чтобы искать по всем ячейкам таблицы и 
        находить хотя бы 3 слова из словаря считать что подходит
        
        '''
        docum = Document(os.getcwd() + "/Git/parser_results_and_competitions/Yargy/docs/" + "РПД Схемотехника ЭВМ и аппаратура персональных компьютеров (09.03.01, 2016, (4.0), Информатика и вычислительная техника(19610)).docx")
        found = False
        for table in docum.tables:
            for column in table.columns:
                for cell in column.cells:
                    particles = pars.findall(cell.text)
                    index = 0
                    for each in particles:
                        index+=1
                    if index > 2:
                        self.themes (column)
                        found = True
                        break 
                if found: break
            if found: break
        print(index)



    def themes(self,column):
        key = column.cells[0].text
        themes_dict={key:[]}
        for cell in column.cells[1::]:
            #print (cell.text)
            if (cell.text == "Контроль") or (cell.text == "Всего") :
                break
            if (cell.text == key):
                continue
            themes_dict[key].append(cell.text)
            
        print(themes_dict)




class DocumentPrepare:

    def __init__(self,name='None'):
        self.namedoc=name
        print(name)

    def open_doc(self, docname='None'):
        if self.namedoc is not 'None':
            docname = self.namedoc
        print(docname)
        print(self.namedoc)
        if (docname is 'None') and (self.namedoc is 'None'):
            print("print the name of the file (yargy)")
            docname = input()
        #  path = "docs\\" + name  //windows
        path = os.getcwd() + "/Git/parser_results_and_competitions/Yargy/docs/" +docname #  Linux
        docx = Document(path)
        return docx

#mydoc = DocumentPrepare()
#mydoc.open_doc()


mytext = LecturePaser('15.Сети ЭВМ и телекоммуникации.docx')
mytext.sections()