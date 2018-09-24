from IPython.display import display
from yargy import Parser, rule, and_, or_
from yargy.interpretation import fact, attribute
from yargy.predicates import dictionary, gte, lte


Date = fact(
    'Date',
    [attribute('year', 2017), 'month', 'day']
)


MONTHS = {
    'январь',
    'февраль',
    'март',
    'апрель',
    'мая',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь'
}


MONTH_NAME = dictionary(MONTHS)
DAY = and_(
    gte(1),
    lte(31)
)
YEAR = and_(
    gte(1900),
    lte(2100)
)
DATE = rule(
    DAY.interpretation(
        Date.day
    ),
    MONTH_NAME.interpretation(
        Date.month
    ),
    YEAR.interpretation(
        Date.year
    ).optional()
).interpretation(
    Date
)


text = '''18 июля 2016
15 марта
'''


parser = Parser(DATE)
for line in text.splitlines():
    match = parser.match(line)
    display(match.fact)

parser = Parser(DATE)
for line in text.splitlines():
    match = parser.match(line)
    display(match.tree.as_dot)
