import yargy
import os
import win32com.client

import yargy


filename = "9_ФОС_Операционные системы"



def startmacros():
    '''
    This function gets file ("name".doc) and runs macros inside it
    It should returns file ("name".txt) (or not)
    :return:
    '''
    if os.path.exists(filename+".doc"):
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = True
        print(os.getcwd())
        word.Documents.Open(os.getcwd()+"\\"+(filename+".doc")) #It should open, but it doesnt
        print("found \\")

        word.Application.Run("DeleteText")
        print("one")
        word.Application.Run("Tables")
        print("two")
        word.Application.Run("SaveAsTXT")
        print("I saved")
        word.Application.Quit()
    else:
        print("nofile")




def opentxtfile():
    '''
    This function opens file "name".txt for yargy parser
    :return:
    '''
    myfile = open(filename+".txt","r")
    print("closed? "+str(myfile.closed))
    print("mode "+str(myfile.mode))
    print("name "+str(myfile.name))
    '''print(myfile.read())  #it works'''

startmacros()
opentxtfile()
