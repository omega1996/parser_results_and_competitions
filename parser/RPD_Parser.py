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
from yargy.predicates import dictionary
from yargy.tokenizer import Tokenizer, TokenRule


class RPD_Parser:

    def __init__(self):

        self.rpd_task_and_goals = morph_pipeline([
            'цели и задачи',
            'цели освоения',
            'задачи освоения',
            'краткое описание',
            'аннотация'
        ])

        self.rpd_education_result = morph_pipeline([
            'планируемый результат обучение'
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
            'практическое занятие',
            'семинар',
            'семинарские занятия'
        ])

        self.rpd_selfwork_theme = morph_pipeline([
            'самостоятельная работа обучающихся по дисциплине',
            'самостоятельная работа студентов'
        ])

        # rpd_literature = morph_pipeline([
        #     'литература'
        # ])

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
                    'наименование'
                ]))

        self.rpd_srs = rule(
            morph_pipeline(
                [
                    'СРС'
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

        self.get_rpd_text("docx/ЧелГУ/5_РПД _Математический анализ, Дифференциальные и разностные уравнения.docx")

        self.documentText['цели и задачи'] = self.find_boundries(parser_RPD_task_and_goals)
        self.documentText['результаты обучения'] = self.find_boundries(parser_RPD_education_result)
        self.documentText['связь дисциплины'] = self.find_boundries(parser_RPD_discipline_link)
        self.documentText['структура дисциплины'] = self.find_boundries(parser_PRD_discipline_structure)
        self.documentText['темы лекций'] = self.find_boundries(parser_PRD_lecture_theme)
        self.documentText['темы практик'] = self.find_boundries(parser_RPD_practice_theme)
        self.documentText['темы СРС'] = self.find_boundries(parser_RPD_selfwork_theme)
        # documentText['литература'] = find_boundries(docs_headers, fullText, parser_RPD_literature)

        # print компетенции и результаты обучения
        fgos_table = ""
        for item in self.documentText['результаты обучения']:
            if "Таблица: " in item:
                fgos_table = item
                break
        competence = self.search_place_fgos(fgos_table)
        zyn = self.get_zyn_results(fgos_table, parser_PRD_zyn_result)

        # внедрить разбиение по лекциям, практикам и срс

        for key, val in self.documentText.items():
            print(key, val)

    def is_bold_paragraph(self, paragraph):
        for run in paragraph.runs:
            if run.bold:
                return True

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
            self.fullText.append(block)

    def find_boundries(self, parser):
        start_index = 0
        end_index = 0
        text = list()
        start_header = ""
        end_header = ""
        is_boundaries_found = False
        for i in range(len(self.docs_headers) - 1):
            compare = re.sub(r'[^\w\s]+|[\d]+', r'', self.docs_headers[i].lower()).strip()
            for match in parser.findall(compare):
                start_header = self.docs_headers[i]
                end_header = self.docs_headers[i + 1]
                for j in range(len(self.fullText) - 1):
                    if start_header.lower() == self.fullText[j].lower():
                        start_index = j + 1
                    if end_header.lower() == self.fullText[j].lower():
                        end_index = j - 1
                for t in range(start_index, end_index + 1):
                    text.append(self.fullText[t])
                is_boundaries_found = True
                break
            if is_boundaries_found:
                break
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
                    for cell in row.cells:
                        my_table += cell.text
                        my_table += '\t'
                    my_table += '\n'
                text = my_table
                yield text

    def search_place_fgos(self, text):
        FGOS_list = self.token_fgos(text)
        competence = dict()
        if len(FGOS_list) > 0:
            for i in FGOS_list:
                competence[i.value] = self.separate(text[i.span[1]:text.find('\n', i.span[1])])
        return competence

    def separate(self, text):
        competence = text[1:text.find('\t', 1)]
        return competence

    def token_fgos(self, text):
        tokenizer = Tokenizer()
        fgos_rule = TokenRule('FOS', '[А-Я]+К+-+[0-9]+')  # букв не больше 3 и последняя к
        tokenizer.remove_types('EOL', 'RU', 'PUNCT', 'OTHER', 'INT', 'LATIN')
        tokenizer.add_rules(fgos_rule)
        return list(tokenizer(text))

    def get_zyn_results(self, part, parser):
        dict_result = {}
        current = None
        for next in parser.findall(part):
            if current is not None:
                res = part[current.tokens[0].span[1] + 1:next.tokens[0].span[0]]
                if current.tokens[0].value not in dict_result:
                    dict_result[current.tokens[0].value] = []
                dict_result[current.tokens[0].value] = res.split(';')
            current = next
        if current is not None:
            if current.tokens[0].value not in dict_result:
                dict_result[current.tokens[0].value] = []
            dict_result[current.tokens[0].value] = part[current.tokens[0].span[1] + 1:].split(';')
        return dict_result

    def get_rpd_theme(self):
        pass

    def get_rpd_lectures(self):
        pass

    def get_prd_practices(self):
        pass

    def get_srs_themes(self):
        pass


parser = RPD_Parser()
