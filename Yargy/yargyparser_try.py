from docx import Document
from docx.shared import Inches
import yargy
import os
from yargy.tokenizer import Tokenizer, TokenRule
from yargy.pipelines import morph_pipeline
import input_test as inp

class CompetitionResult():

    def __init__(self, FGOS, competition, result=None):
        self.FGOS = FGOS
        self.competition = competition
        self.result = result




class YargyParser:

    def __init__(self, filename="none"):
        if filename == "none":
            print("print the name of the file (yargy)")
            filename = input()
        self.filename = filename
        self.document = Document(os.getcwd() + "\\" + (self.filename + ".docx"))


    def text_prepare(self):
        my_text = ""
        my_table = ""
        for i in self.document.paragraphs:
            my_text += "||" + i.text

        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    my_table += cell.text
                    my_table += "~"
                my_table += "@"

        text = my_text + my_table
        #print(text)
        #return my_table, my_text

        return text


    def search_place_FGOS(self):
        FGOS_list = self.token_FOS(self.text_prepare())
        k = FGOS_list[0]
        print(len(FGOS_list))
        entitis = []
        for i in FGOS_list:

            text = self.text_prepare()
            # print(i.value)
            k = i
            if i.value not in entitis:
                pr = text[k.span[1]:text.find('@',k.span[1])]
                entitis.append(i.value)
                print(i.value)
                #print(pr)
                competence, know, can, own = self.separate(pr)
                print(competence)


    def separate(self, text):
        competence = text[1:text.find('~',1)]
        know = ""
        can = ""
        own = ""
        return competence, know,can,own

    def search_place_goals(self):
        pass





    def token_FOS(self, text):
        tokenizer = Tokenizer()
        FOS_RULE = TokenRule('FOS', '[А-Я]+К+-+[0-9]+') #  букв не больше 3 и последняя к
        tokenizer.remove_types('EOL', 'RU','PUNCT','OTHER','INT','LATIN')
        tokenizer.add_rules(FOS_RULE)
        return list(tokenizer(text))




mytry = YargyParser("25_РПД Разработка приложений для работы с БД")
mytry.search_place_FGOS()
#  mytry.token_FOS()
