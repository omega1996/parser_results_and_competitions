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
        mmm = pars.findall("Содержание дисциплины, структурированное\ по тема, тема, темам, темы (разделам) с указанием отведенного на них количества академических часов и видов учебных занятий Таблица 2.1 – Разделы дисциплины и трудоемкость по видам учебных занятий ( в академических часах)  для очной формы обучения")
        index = 0
        for i in mmm:
            print(i.tokens[0].value)
            index +=1
        print(index)



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