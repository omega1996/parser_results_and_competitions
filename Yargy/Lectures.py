from docx import Document
import yargy
import os
import re
import copy
from yargy import Parser, rule, and_, or_
from yargy.pipelines import morph_pipeline
from yargy.predicates import gram, is_capitalized, dictionary, is_upper, length_eq


class LecturePaser:

    def __init__(self,name=None):

        self.section_rule = rule(
            dictionary(
                {
                    "раздел", "тема", "дисциплина", "наименование"
                }
                        ))

        self.lectures_rule = rule(
            morph_pipeline([
                'тема лекций',
                'содержание занятий',
                'содержание лекционного занятия'
            ])
        )

        self.pract_rule = rule(
            morph_pipeline(
                [

                ]
            )


        )


        self.srs_rule = rule(
             morph_pipeline(
                [
                    
                ]
            )

        )


        self.docxdoc=DocumentPrepare(name).open_doc()


    def sections(self):
        themes = Parser(self.section_rule)
        lectures = Parser(self.lectures_rule)
        #practices = Parser(self.pract_rule)
        #srs = Parser(self.srs_rule)
        found = False
        for table in self.docxdoc.tables:
            for column in table.columns:
                for cell in column.cells:
                    cell_search_themes = themes.findall(cell.text) #поиск тем
                    cell_search_lectures = lectures.findall(cell.text)
                    index = 0

                    for each in cell_search_lectures:
                        self.lectures(table,column)
                        found = True
                        print("ЛЕКЦИИ")
                        break

                    '''
                    If you don't want to stop after finding
                    comment found = True 
                    '''
                    
                    for each in cell_search_themes:
                        index+=1
                    if index > 2:
                        self.lectures(table,column)
                        #found = True
                        print("this is theme")
                        break 
                    
                if found: break
            if found: break
        #print(index)


    def lectures(self,table, column):
        key = column.cells[0].text
        lect_dict={key:[]}
        flag = False
        separator =False
        save_pre=''
        save_lect=''
        for cell in column.cells:
            lect = cell.text
            
            for row in table.rows:
                for cell in row.cells:

                    if (cell.text == "Контроль") or (cell.text == "Всего:") or (cell.text == "Итого") :
                        break

                    if flag:
                    
                        precision = cell.text
                        if save_lect != lecture:
                            lect_dict[key].append(lecture+'=')
                            save_lect = lecture

                        if re.sub(r'[^\w\s]+|[\d]+',r'',precision).strip() != '' and save_pre!=precision:
                            lect_dict[key].append(precision+'|')
                            save_pre = precision
                            
                        flag = False

                    if (cell.text == lect) and lect != '':
                        lecture = cell.text
                        flag = True

        print(lect_dict)

        '''
        #legacy:

    def themes(self,column):
        key = column.cells[0].text
        themes_dict={key:[]}
        for cell in column.cells[1::]:
            #print (cell.text)
            if (cell.text == "Контроль") or (cell.text == "Всего") or (cell.text == "Итого") :
                break
            if (cell.text == key):
                continue
            themes_dict[key].append(cell.text)
            
        print(themes_dict)
        '''




class DocumentPrepare:

    def __init__(self,name='None'):
        self.namedoc=name

    def open_doc(self, docname='None'):
        if self.namedoc is not 'None':
            docname = self.namedoc
        if (docname is 'None') and (self.namedoc is 'None'):
            print("print the name of the file (yargy)")
            docname = input()
        
        if os.name == 'nt':
            path = "docs\\" + name 
        if os.name == 'posix':
            path = os.getcwd() + "/Git/parser_results_and_competitions/co-co-corpus" +docname #  Linux
        docx = Document(path)
        return docx

#mydoc = DocumentPrepare()
#mydoc.open_doc()


#mytext = LecturePaser('25_РПД Разработка приложений для работы с БД.docx')
#mytext = LecturePaser('31. Сетевые технологии.docx')#не работает
#mytext = LecturePaser('РПД Схемотехника ЭВМ и аппаратура персональных компьютеров (09.03.01, 2016, (4.0), Информатика и вычислительная техника(19610)).docx') #только разделы
#mytext = LecturePaser('5_РПД Математика.docx')
mytext = LecturePaser('/ЮГРА/15.Сети ЭВМ и телекоммуникации.docx')
mytext.sections()