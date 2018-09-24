import yargy
from yargy.pipelines import morph_pipeline
import input_test as inp

fromtext = inp.Inputdoc(filename = "10_РПД_Безопасность жизнедеятельности")
fromtext.tablescreate()
text = fromtext.opentxtfile()
literature = morph_pipeline(['лекции'])

parser = yargy.Parser(literature)

for match in parser.findall(text):
    print([_.value for _ in match.tokens])


