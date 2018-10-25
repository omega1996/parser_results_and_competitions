from yargy import *
from docx import *
from yargy.predicates import gram, is_capitalized, dictionary, is_upper, length_eq
from yargy.pipelines import morph_pipeline
import re
import glob
import os


class RPD_Parser:

    def __init__(self):
        rpd_task_and_goals = morph_pipeline([
            'цели и задачи освоения',
            'цели освоения',
            'задачи освоения',
            'краткое содержание',
            'краткое описание',
            'аннотация'
        ])

        rpd_education_result = morph_pipeline([
            'планируемый результат обучение'
        ])
        rpd_discipline_link = morph_pipeline([
            'место учебный дисциплина',
            'место дисциплины'
        ])
        rpd_discipline_structure = morph_pipeline([
            'содержание дисциплина'
        ])
        rpd_lecture_theme = morph_pipeline([
            'лекции'
        ])
        rpd_practice_theme = morph_pipeline([
            'практическое занятие',
            'семинар',
            'семинарские занятия'
        ])
        rpd_selfwork_theme = morph_pipeline([
            'самостоятельная работа обучающихся',
            'самостоятельная работа студентов'
        ])
        rpd_literature = morph_pipeline([
            'литература'
        ])
        parser_RPD_task_and_goals = Parser(rpd_task_and_goals)
        parser_RPD_education_result = Parser(rpd_education_result)
        parser_RPD_discipline_link = Parser(rpd_discipline_link)
        parser_PRD_discipline_structure = Parser(rpd_discipline_structure)
        parser_PRD_lecture_theme = Parser(rpd_lecture_theme)
        parser_RPD_practice_theme = Parser(rpd_practice_theme)
        parser_RPD_selfwork_theme = Parser(rpd_selfwork_theme)
        parser_RPD_literature = Parser(rpd_literature)

        parsers = list()
        parsers.append(parser_RPD_task_and_goals)
        parsers.append(parser_RPD_education_result)
        parsers.append(parser_RPD_discipline_link)
        parsers.append(parser_PRD_discipline_structure)
        parsers.append(parser_PRD_lecture_theme)
        parsers.append(parser_RPD_practice_theme)
        parsers.append(parser_RPD_selfwork_theme)
        parsers.append(parser_RPD_literature)

        docs_headers = list()
        fullText = list()

        get_rpd_headers_and_text("test/5_РПД _Математический анализ, Дифференциальные и разностные уравнения.docx",
                                 docs_headers, fullText)
        for p in parsers:
            text = find_boundries(docs_headers, fullText, p)
            print(text)


def is_bold_paragraph(paragraph):
    for run in paragraph.runs:
        if run.bold:
            return True


def iter_headings(paragraphs):
    text_paragraph = ""
    for paragraph in paragraphs:
        if (((re.match('\d.\d.+', paragraph.text) or re.match('\d.+', paragraph.text)) and is_bold_paragraph(
                paragraph) is True)
            or paragraph.style.name.startswith('Heading')
            or paragraph.style.name.startswith('Subtitle')) \
                and (not (re.match(' Таблица ', paragraph.text))):
            yield paragraph


def get_rpd_headers_and_text(filename, docs_headers=list(), fullText=list()):
    document = Document(filename)
    for heading in iter_headings(document.paragraphs):
        if heading.text != '' and heading.text != '\n':
            docs_headers.append(heading.text)
    for para in document.paragraphs:
        fullText.append(para.text)


def find_boundries(docs_headers, fullText, parser):
    start_index = 0
    end_index = 0
    text = ""
    start_header = ""
    end_header = ""
    for i in range(len(docs_headers) - 1):
        for match in parser.findall(docs_headers[i]):
            start_header = docs_headers[i]
            end_header = docs_headers[i + 1]

        for j in range(len(fullText) - 1):
            if re.match(start_header, fullText[j]):
                start_index = j + 1
            if re.match(end_header, fullText[j]):
                end_index = j - 1
        for i in range(start_index, end_index):
            text += fullText[i] + '\n'
    return text


parser = RPD_Parser()
