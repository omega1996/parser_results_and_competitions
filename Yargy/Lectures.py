from docx import Document
import yargy
import os
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
                'содержание занятий'
            ])
        )

        self.docxdoc=DocumentPrepare(name).open_doc()


    def sections(self):
        themes = Parser(self.section_rule)
        lectures = Parser(self.lectures_rule)
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

                    
                    for each in cell_search_themes:
                        index+=1
                    if index > 2:
                        self.themes(column)
                        found = True
                        print("this is theme")
                        break 
                    
                if found: break
            if found: break
        #print(index)


    def lectures(self,table,lect_column):
        key = "Тема лекции"
        lect_dict={key:[]}
        flag = False
        separator =False
        for cell in lect_column.cells:
            lect = cell.text
            
            for row in table.rows:
                for cell in row.cells:
                    if flag:
                        precision = cell.text
                        lect_dict[key].append(lecture+'=')
                        lect_dict[key].append(precision+'|')
                        flag = False
                    '''
                    if separator:
                        lect_dict[key].append('%'+cell.text+'%')
                        separator = False

                    if cell.text == '':
                        separator = True
                    '''

                    if (cell.text == lect) and lect != '':
                        lecture = cell.text
                        flag = True
                    
                    if cell.text == 'Итого':
                        break
                        
                    
        print(lect_dict)


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

    def open_doc(self, docname='None'):
        if self.namedoc is not 'None':
            docname = self.namedoc
        if (docname is 'None') and (self.namedoc is 'None'):
            print("print the name of the file (yargy)")
            docname = input()
        #  path = "docs\\" + name  //windows
        path = os.getcwd() + "/Git/parser_results_and_competitions/Yargy/docs/" +docname #  Linux
        docx = Document(path)
        return docx

#mydoc = DocumentPrepare()
#mydoc.open_doc()


#mytext = LecturePaser('25_РПД Разработка приложений для работы с БД.docx')
mytext = LecturePaser('31. Сетевые технологии.docx')

mytext.sections()