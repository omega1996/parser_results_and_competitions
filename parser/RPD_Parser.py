import glob
import os
from itertools import groupby

from yargy import *
from docx import *
from yargy.pipelines import morph_pipeline, caseless_pipeline
import re
import docx
from docx.document import Document
from docx.oxml import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from yargy.predicates import dictionary, is_title
from yargy.tokenizer import Tokenizer, TokenRule
import csv


class RPD_Parser:

    def __init__(self, filename, university):

        self.filename = filename
        self.university = university

        self.rpd_task_and_goals = morph_pipeline([
            'цели и задачи',
            'цели освоения',
            'задачи освоения',
            'аннотация',
            'краткое содержание',
            'краткое описание'
        ])

        self.rpd_education_result = morph_pipeline([
            'планируемый результат обучение',
            'компетенции'
        ])

        self.rpd_discipline_link = morph_pipeline([
            'место учебный дисциплина',
            'место дисциплины'
        ])

        self.rpd_discipline_structure = caseless_pipeline([
            'содержание дисциплины',
            'структура дисциплины'
        ])

        self.rpd_lecture_theme = morph_pipeline([
            'лекции'
        ])

        self.rpd_practice_theme = morph_pipeline([
            'практические занятия',
            'семинар',
            'семинарские занятия'
        ])

        self.rpd_selfwork_theme = morph_pipeline([
            'самостоятельная работа обучающихся по дисциплине',
            'самостоятельная работа студентов'
        ])

        self.rpd_education_zyn = rule(
            dictionary({
                'Знать',
                'Уметь',
                'Владеть'
            })
        )
        self.section_rule = rule(
            dictionary(
                {
                    "раздел", "тема", "дисциплина", "наименование"
                }))

        self.prd_lectures = rule(
            morph_pipeline([
                'тема лекций',
                'содержание занятий',
                'содержание лекционного занятия'
            ]))

        self.prd_practices = rule(
            morph_pipeline(
                [
                    'наименование',
                    'лабораторные работы',
                    'содержание практического занятия'
                ]))

        self.rpd_srs = rule(
            morph_pipeline(
                [
                    'СРС',
                    'содержание занятий',
                    'содержание задания',
                    'тема СРО',
                    'тема СРС'
                ]))
        self.rpd_name = rule(
            and_(dictionary({
                'рабочая'})),
            dictionary({
                'программа'}),
        )
        self.table_rpd_name = rule(
            dictionary({
                'дисциплина'
            })
        )

        self.rpd_lectures_optional = rule(
            morph_pipeline(
                [
                    'содержание'
                ]))
        self.rpd_practices_optional = rule(
            morph_pipeline(
                [
                    'содержание',
                    'cодержание практического занятия'
                ]))
        self.rpd_srs_optional = rule(
            morph_pipeline(
                [
                    'содержание',
                    'содержание задания'
                ]))

        self.documentText = dict()
        self.docs_headers = list()
        self.fullText = list()

        parser_RPD_task_and_goals = Parser(self.rpd_task_and_goals)
        parser_RPD_education_result = Parser(self.rpd_education_result)
        parser_RPD_discipline_link = Parser(self.rpd_discipline_link)
        parser_PRD_discipline_structure = Parser(self.rpd_discipline_structure)
        parser_PRD_lecture_theme = Parser(self.rpd_lecture_theme)
        parser_RPD_practice_theme = Parser(self.rpd_practice_theme)
        parser_RPD_selfwork_theme = Parser(self.rpd_selfwork_theme)
        parser_PRD_zyn_result = Parser(self.rpd_education_zyn)
        parser_PRD_themes = Parser(self.section_rule)
        parser_PRD_lectures = Parser(self.prd_lectures)
        parser_PRD_practices = Parser(self.prd_practices)
        parser_RPD_srs = Parser(self.rpd_srs)
        parser_RPD_name = Parser(self.rpd_name)
        self.parser_table_RPD_name = Parser(self.table_rpd_name)
        parser_RPD_lectures_desc = Parser(self.rpd_lectures_optional)
        parser_RPD_practices_desc = Parser(self.rpd_practices_optional)
        parser_RPD_srs_desc = Parser(self.rpd_srs_optional)

        self.get_rpd_text(filename)
        self.documentText['университет'] = self.university
        self.documentText['название дисциплины'] = self.get_rpd_name(parser_RPD_name)

        self.documentText['направление подготовки'] = self.get_direction_of_preparation()

        self.documentText['цели и задачи'] = self.find_boundries(parser_RPD_task_and_goals)

        self.documentText['результаты обучения'] = self.find_boundries(parser_RPD_education_result)
        fgos_table = ""
        flag = True
        if self.documentText['результаты обучения'] != None:
            for item in self.documentText['результаты обучения']:
                if "Таблица: " in item:
                    fgos_table = item[8:]

            if fgos_table == "":
                fgos_table = self.documentText['результаты обучения']
                flag = False
        self.documentText['ЗУН'] = self.get_zyn_results(fgos_table, parser_PRD_zyn_result, flag)
        self.documentText['компетенции'] = self.search_place_fgos("".join(fgos_table))



        self.documentText['связь дисциплины'] = self.find_boundries(parser_RPD_discipline_link)

        self.documentText['структура дисциплины'] = self.find_boundries(parser_PRD_discipline_structure)

        discipline_themes_table = ""
        for item in self.documentText['структура дисциплины']:
            if "Таблица: " in item:
                discipline_themes_table = item
                break

        self.documentText['темы структуры дисципилны'] = self.convert_string_to_table(discipline_themes_table[8:],
                                                                                      parser_PRD_themes)

        self.documentText['лекции'] = self.find_boundries(parser_PRD_lecture_theme)
        if self.documentText['лекции'] is not None:
            discipline_lectures_table = ""
            for item in self.documentText['лекции']:
                if "Таблица: " in item:
                    discipline_lectures_table = item
                    break
            self.documentText['темы лекций'] = self.convert_string_to_table(discipline_lectures_table[8:],
                                                                            parser_PRD_lectures)
            self.documentText['описание лекций'] = self.convert_string_to_table(discipline_lectures_table[8:],
                                                                                parser_RPD_lectures_desc)

        self.documentText['практики'] = self.find_boundries(parser_RPD_practice_theme)
        if self.documentText['практики'] is not None:
            discipline_practises_table = ""
            for item in self.documentText['практики']:
                if "Таблица: " in item:
                    discipline_practises_table = item
                    break

            self.documentText['темы практик'] = self.convert_string_to_table(discipline_practises_table[8:],
                                                                             parser_PRD_practices)
            self.documentText['описание практик'] = ""
            #self.convert_string_to_table(discipline_lectures_table[8:],parser_RPD_practices_desc)

        self.documentText['СРС'] = self.find_boundries(parser_RPD_selfwork_theme)
        if self.documentText['СРС'] is not None:
            discipline_srs_table = ""
            for item in self.documentText['СРС']:
                if "Таблица: " in item:
                    discipline_srs_table = item
                    break

            self.documentText['темы СРС'] = self.convert_string_to_table(discipline_srs_table[8:], parser_RPD_srs)
            self.documentText['описание СРС'] = ""
                #self.convert_string_to_table(discipline_srs_table[8:], parser_RPD_srs_desc)

        for key, val in self.documentText.items():
            print(key, val)

    def is_bold_paragraph(self, paragraph):
        for run in paragraph.runs:
            if run.bold:
                return True

    def get_direction_of_preparation(self):
        for item in self.fullText:
            if "Таблица: " in item:
                cell = item[8:]
                span = self.token_direction_of_preparation(cell)[0].span
                return cell[span[0]:cell.find('\n', span[0])]
            else:
                for i in range(len(self.fullText)):
                    if len(self.token_direction_of_preparation(self.fullText[i])) > 0:
                        if "Таблица: " in self.fullText[i]:
                            cell = self.fullText[i][8:]
                            span = self.token_direction_of_preparation(cell)[0].span
                            return cell[span[0]:cell.find('\n', span[0])]
                        else:
                            return self.fullText[i]

    def get_rpd_name(self, parser):
        for item in self.fullText:
            if "Таблица: " in item:
                cell = item[8:]
                span = self.parser_table_RPD_name.find(cell).span
                return cell[span[1]:cell.find('\n', span[1])]
            else:
                for i in range(len(self.fullText)):
                    for match in parser.findall(self.fullText[i]):
                        return self.fullText[i + 1]

    def iter_rpd_headings(self, paragraphs):
        for paragraph in paragraphs:
            if (((re.match('\d.\d.+', paragraph.text) or re.match('\d.+', paragraph.text)) and self.is_bold_paragraph(
                    paragraph) is True)
                or paragraph.style.name.startswith('Heading')
                or paragraph.style.name.startswith('Subtitle')) \
                    and (not (re.match(' Таблица ', paragraph.text))):
                yield paragraph

    def get_rpd_text(self, filename):
        document = docx.Document(filename)
        for heading in self.iter_rpd_headings(document.paragraphs):
            if heading.text != '' and heading.text != '\n' and heading.text != ' ' and heading.text.isspace() is False:
                self.docs_headers.append(heading.text)
        for block in self.iter_block_rpd_items(document):
            if block != '' and block != '\n' and block != ' ' and block.isspace() is False:
                self.fullText.append(block)

    def token_direction_of_preparation(self, text):
        CODE_RULE = TokenRule('Code', '\d{2}.\d{2}.\d{2}(?!\d)')
        tokenizer = Tokenizer()
        tokenizer.remove_types('EOL', 'LATIN', 'RU', 'INT', 'PUNCT', 'OTHER')
        tokenizer.add_rules(CODE_RULE)
        return list(tokenizer(text))

    def find_boundries(self, parser):
        start_index = 0
        end_index = 0
        text = list()
        start_header = ""
        end_header = ""
        for i in range(len(self.docs_headers) - 1):
            # compare = re.sub(r'[^\w\s]+|[\d]+', r'', self.docs_headers[i].lower()).strip()
            compare = self.docs_headers[i].lower()
            for match in parser.findall(compare):
                start_header = self.docs_headers[i]
                end_header = self.docs_headers[i + 1]
                for j in range(len(self.fullText) - 1):
                    if start_header.lower() == self.fullText[j].lower():
                        start_index = j + 1
                    if end_header.lower() == self.fullText[j].lower():
                        end_index = j - 1
                if start_index != end_index:
                    for t in range(start_index, end_index + 1):
                        text.append(self.fullText[t])
                else:
                    text.append(self.fullText[start_index])
                return text

    def iter_block_rpd_items(self, parent):
        if isinstance(parent, Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            raise ValueError("something's not right")

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent).text
            elif isinstance(child, CT_Tbl):
                table = Table(child, parent)
                my_table = "Таблица: "

                for row in table.rows:
                    try:
                        for cell in row.cells:
                            my_table += cell.text
                            my_table += '~'

                    except:
                        print('out of range')
                        pass
                    my_table += '@'
                text = my_table
                yield text

    def search_place_fgos(self, text):
        FGOS_list = self.token_fgos(text)
        competence = dict()
        if len(FGOS_list) > 0:
            for i in FGOS_list:
                competence[i.value] = self.separate(text[i.span[1]:text.find('@', i.span[1])])
        return competence

    def separate(self, text):
        competence = text[1:text.find('~', 1)]
        return competence

    def token_fgos(self, text):
        tokenizer = Tokenizer()
        fgos_rule = TokenRule('FOS', '[А-Я]+К+-+[0-9]+')  # букв не больше 3 и последняя к
        tokenizer.remove_types('EOL', 'RU', 'PUNCT', 'OTHER', 'INT', 'LATIN')
        tokenizer.add_rules(fgos_rule)
        return list(tokenizer(text))

    def get_zyn_results(self, text, parser, flag):
        parts = list()
        dict_result = {}
        if flag:
            parts = text.split("@")
            for part in parts:
                current = None
                for next in parser.findall(part):
                    if current is not None:
                        res = part[current.tokens[0].span[1] + 1:next.tokens[0].span[0]]
                        if current.tokens[0].value not in dict_result:
                            dict_result[current.tokens[0].value] = []
                        dict_result[current.tokens[0].value].append(res.split(';'))
                    current = next
                if current is not None:
                    if current.tokens[0].value not in dict_result:
                        dict_result[current.tokens[0].value] = []
                    dict_result[current.tokens[0].value].append(part[current.tokens[0].span[1] + 1:].split(';'))
            return dict_result
        else:
            parts = text
            for i in range(len(parts)):
                for next in parser.findall(parts[i]):
                    k = i+1
                    while parts[i] != '\n' or parts[i]!= next.tokens[k]:
                        if next.tokens[0].value not in dict_result:
                            dict_result[next.tokens[0].value] = []
                        dict_result[next.tokens[0].value].append(parts[k])
                        k+=1
            return dict_result


    def convert_string_to_table(self, text, pattern):

        rows = text.split('@')
        cells = list()
        for row in rows:
            cells.append(row.split('~'))
        data_column_number = 0
        if 'Выполнение СРС' in cells[0][0]:
            cells.pop(0)
        for j in range(len(cells[0]) - 1):
            for match in pattern.findall(cells[0][j]):
                data_column_number = j
                break
        temp = list()
        for k in range(len(cells) - 1):
            temp.append(cells[k][data_column_number])
        for t in range(len(temp) - 1):
            if temp[t] == temp[t + 1]:
                temp[t] = ""
        results = list()
        for i in range(len(temp)):
            if temp[i] != '' and temp != " " and temp is not None:
                results.append(temp[i])
        if len(results) != 0:
            results.pop(0)
        return results

#
#parser = RPD_Parser("/home/autumn_mint/Desktop/project_practice/docx/ЮУрГУ/РПД Алгоритмы и методы представления графической информации (09.03.01, 2016, (4.0), Информатика и вычислительная техника(19610)).docx", "ЮУрГУ")
# parser = RPD_Parser("/home/autumn_mint/Desktop/project_practice/docx/ЧелГУ/47_1_РПД_Гибкое управление проектами.docx", 'ЧелГУ')
#parser = RPD_Parser("/home/autumn_mint/Desktop/project_practice/docx/УрФУ/02.04.02 Менеджмент в Информационных технологиях.docx", 'УрФУ')
# # # #parser = RPD_Parser("/home/autumn_mint/Desktop/project_practice/docx/ЮГРА/14.Тестирование и отладка ПО.docx")
class dataset_writer:
    def __init__(self):
        self.headers = ['университет', 'направление подготовки', 'название дисциплины', 'цели и задачи/аннотации', 'место дисциплины в структуре ОП', 'результаты обучения', 'компетенции', 'разделы дисциплины', 'описание разделов', 'темы лекций', 'описание лекций', 'темы практик', 'описание практик', 'темы СРС', 'описание СРС']
        self.filename = "dataset.csv"
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)

    def write_dataset(self, document_text):
        data = document_text.values()
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)

def test_search(univer='all'):
    datawr = dataset_writer()
    unilist = ['ЧелГУ', 'ЮУрГУ']
    if univer != 'all':
        unilist = [univer]

    for uni in unilist:
        print(uni)
        path = os.getcwd() + "/docx/" + uni + "/"
        for file in glob.glob(os.path.join(path, '*.docx')):
            print(file + '\n')
            parser = RPD_Parser(file, uni)

            datawr.write_dataset(parser.documentText)
            print('end of file')

test_search()




