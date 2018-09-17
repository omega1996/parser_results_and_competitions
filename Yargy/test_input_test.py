import input_test as inp


testname = "ИС в предметной области+"

document = inp.Inputdoc(filename = testname)


def test_file_adder():
    document.startmacros()
    document.opentxtfile()


test_file_adder()  # ok test passed