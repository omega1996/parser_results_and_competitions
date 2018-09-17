from yargy import Parser, rule, and_
from yargy.predicates import gram, is_capitalized, dictionary
import input_test as inp

GEO = rule(
    and_(
        gram('ADJF'),  # так помечается прилагательное, остальные пометки описаны в
                       # http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
        is_capitalized()
    ),
    gram('ADJF').optional().repeatable(),
    dictionary({
        'процессы',
        'ресурсы',
        'системы',
        'безопасность'
    })
)

fname = "ИС в предметной области+"
text = inp.Inputdoc(filename = fname).opentxtfile()


parser = Parser(GEO)

for match in parser.findall(text):
    print([_.value for _ in match.tokens])