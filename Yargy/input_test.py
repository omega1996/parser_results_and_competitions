import os
import win32com.client


class Inputdoc:

    def __init__(self, filename="none", vision=False):

        if filename=="none":
            print ("print name of the file")
            filename = input()

        self.filename = filename
        self.vision = vision    # Set True if you want to open Word

    def startmacros(self):
        '''
        This function gets file ("name".doc) and runs macros inside it
        It should returns file ("name".txt) (or not)
        :return:
        '''
        if os.path.exists(self.filename+".doc"):
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = self.vision
            print(os.getcwd())
            word.Documents.Open(os.getcwd()+"\\"+(self.filename+".doc"))  # it  works
            # os.path.join('', '*.doc') if you want to open several files
            print("found \\")

            word.Application.Run("DeleteText")  # Exclude it if you need to save text
            print("one")
            word.Application.Run("Tables")
            print("two")
            word.Application.Run("SaveAsTXT")
            print("I saved")
            word.Application.Quit()
        else:
            print("no file")



    def opendocfile(self):

        word = win32com.client.Dispatch("Word.Application")
        word.Visible = self.vision
        if os.path.exists(self.filename + ".doc"):
            word.Documents.Open(os.getcwd() + "\\" + (self.filename + ".doc"))
        elif os.path.exists(self.filename + ".docx"):
            word.Documents.Open(os.getcwd() + "\\" + (self.filename + ".docx"))
        elif os.path.exists(self.filename + ".rtf"):
            word.Documents.Open(os.getcwd() + "\\" + (self.filename + ".rtf"))
        else:
            print("Path is not exist")

    def tablescreate(self):

        self.opendocfile()
        word = win32com.client.Dispatch("Word.Application")
        word.Application.Run("Tables")
        word.Application.Run("SaveAsTXT")
        word.Application.Quit()

    def opentxtfile(self):
        '''
        This function opens file "name".txt for yargy parser
        return readed file
        :return:
        '''
        myfile = open(self.filename+".txt","r")
        print("closed? "+str(myfile.closed))
        print("mode "+str(myfile.mode))
        print("name "+str(myfile.name))
        return myfile.read()
        '''print(myfile.read())  #it works'''

#myfos = Inputdoc()  # put here your filename
#myfos.opendocfile()
#myfos.startmacros()
#myfos.opentxtfile()
