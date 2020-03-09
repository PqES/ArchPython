import os

class ReadPyFiles():

    def __init__(self, project_path):
        self.files_name = []
        self.files_path = []
        self.files_dicitonary = {}
        
        self.project_path = project_path

    def find_pys(self):
        rootdir = os.getcwd()
        directory = os.path.join(rootdir, self.project_path)

        #TODO Lançar exceção quando a pasta não existir

        self.create_list_of_files(directory)
                    
        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".py"):
                    file_path = os.path.join(root, name)
                    self.files_path.append(file_path)
        
    def create_list_of_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".py"):
                    self.files_name.append(name)

    def get_files_name(self):
        return self.files_name

    def get_files_path(self):
        return self.files_path
    
    def get_files_dictionary(self): 
        if self.files_dicitonary == {}:
            index = 0
            for index, file_name in enumerate(self.files_name):
                if file_name in self.files_path[index]:
                    #TODO: Passar essa estrutura para uma classe separada
                    self.files_dicitonary[index] = {'file': file_name, 'path':self.files_path[index], 'types': set()}
                else:
                    raise Exception("Deu ruim na criação do dict")
                index = index + 1
        return self.files_dicitonary
            
        
