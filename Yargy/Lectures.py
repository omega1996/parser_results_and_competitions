from docx import Document
import yargy
from yargy import Parser, rule, and_, or_
from yargy.predicates import gram, is_capitalized, dictionary, is_upper, length_eq


class LecturePaser:

    def __init__(self):
        self.section_rule = rule(
            dictionary(
                {
                    "раздел", "тема", "дисциплина", "наименование"
                }
                        ))


    def sections(self):
        pars = Parser(self.section_rule)
        print(pars)
        print(pars.find("Содержание дисциплины, структурированное по тема (разделам) с указанием отведенного на них количества академических часов и видов учебных занятий Таблица 2.1 – Разделы дисциплины и трудоемкость по видам учебных занятий ( в академических часах)  для очной формы обучения"))


class DocumentPrepare:

    def open(self, name=None):
        if name is None:
            print("print the name of the file (yargy)")
            name = input()
        path = "docs\\" + name
        docx = Document(path)
        return docx

mydoc = DocumentPrepare()
mydoc.open("15.Сети ЭВМ и телекоммуникации.docx")

mytext = LecturePaser()
mytext.sections()