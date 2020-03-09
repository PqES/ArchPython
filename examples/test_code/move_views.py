import os

class MoveViews:

    def __init__(self, app_name, project_path):
        self.project_path = project_path
        self.file_dictionary = {}
        self.app_name = app_name
        self.view_directory = ""

        self.find_views()
        self.move_views()

    def find_views(self):
        rootdir = os.getcwd()
        directory = os.path.join(rootdir, self.project_path)

        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".html"):
                    self.file_dictionary[name] = os.path.join(root, name)

    def move_views(self):
        self.create_view_folder()
        for key, value in self.file_dictionary.items():
            os.system("cp " + value + " " + self.view_directory + key)
    
    def get_files_directories(self):
        return self.file_dictionary
    
    def create_view_folder(self):
        self.view_directory = self.app_name + "/views/"
        os.system("mkdir -p " + self.view_directory)
    
