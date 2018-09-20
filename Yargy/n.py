from yargy import Parser
from yargy.pipelines import morph_pipeline


TYPE = morph_pipeline(['электронный дневник'])

parser = Parser(TYPE)
text = 'электронным дневником, электронные дневники, электронное дневнику'
for match in parser.findall(text):
    print([_.value for _ in match.tokens])