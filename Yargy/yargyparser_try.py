from docx import Document
from docx.shared import Inches
import yargy
import os
from yargy.tokenizer import Tokenizer, TokenRule
from yargy.pipelines import morph_pipeline
import input_test as inp


class YargyParser:




    def __init__(self, filename="none"):
        if filename == "none":
            print("print the name of the file (yargy)")
            filename = input()
        self.filename = filename
        self.document = Document(os.getcwd() + "\\" + (self.filename + ".docx"))



    def text_prepare(self):
        my_text = ""
        for i in self.document.paragraphs:
            my_text += "\n" + i.text
        return my_text

    def search_place(self):
        FOS_list = self.token_FOS(self.text_prepare())
        #document
        k = FOS_list[0]
        for i in FOS_list:
            len = i.span[1]-k.span[1]
            text = self.text_prepare()
            print(len)
            print(text[i.span[1]:i.span[1]+len])
            print(i)
            k = i

    def token_FOS(self, text):
        tokenizer = Tokenizer()
        FOS_RULE = TokenRule('FOS', '[А-Я]+-[0-9]') #  букв не больше 3 и последняя к
        tokenizer.remove_types('EOL', 'RU','PUNCT','OTHER','INT','LATIN')
        tokenizer.add_rules(FOS_RULE)
        return list(tokenizer(text))




mytry = YargyParser("ОП ВО 09.03.01, 2016, (4.0), Информатика и вычислительная техника (19610)")
mytry.search_place()
#  mytry.token_FOS()
