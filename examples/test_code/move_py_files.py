import os
import ast
import shutil

from io import StringIO

from structure_crawler import StructureCrawler
from structure_transformer import Transformer
from io import StringIO
from Unparse import Unparser



class MovePyFiles():

    def __init__(self, app_name, project_path):
        self.project_path = project_path
        self.file_dictionary = {}
        self.possible_directories = ['controllers','models', 'dao','routes','views']
        self.file_classes = {}

        self.file_imports = {}
        self.file_module_cache = {}
        self.file_list = []
        self.imports_to_replace = []
        self.imports_to_replace_dict = {}

        self.app_name = app_name
        self.find_pys()
    
    def find_pys(self):
        rootdir = os.getcwd()
        directory = os.path.join(rootdir, self.project_path)

        self.create_list_of_files(directory)
                    
        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".py"):
                    file_path = os.path.join(root, name)
                    sc = StructureCrawler(file_path)
                    print("Arquivo: " + name)
                    print(sc.visitor.probabilitiesToString())

                    module = sc.get_file_module()
                    self.file_classes[name] = sc.get_file_classes()
                    self.file_imports[name] = sc.get_file_imports()

                    self.verify_imports(name, module)

                    self.copy_file_to_correct_folder(module, file_path)
                    self.file_module_cache[name] = module
        
        self.create_import_dictionary()
        self.create_folders_inits()
        self.make_import_replacements()
        self.fix_view_folder_call()
    
    def create_import_dictionary(self):
        for import_replacement in self.imports_to_replace:
            import_file = import_replacement + ".py"
            module = self.file_module_cache[import_file]
            self.imports_to_replace_dict[import_replacement] = module
        
    def copy_file_to_correct_folder(self, module, file_path):
        #Se não existe a pasta, então cria
        if not self.check_with_folder_exits(module):
            self.create_module_folder(module)
        self.copy_file_to_module(module, file_path)
    
    
    def check_with_folder_exits(self, module):
        if module == "main":
            return True
        folder_path = self.app_name + "/" + module
        return os.path.exists(folder_path)
    
    def create_module_folder(self, module):
        folder_path = self.app_name + "/" + module
        os.system('mkdir -p ' + folder_path)
    
    def copy_file_to_module(self, module, file_path):
        # Se é o main, copia para a raiz da pasta
        if module == "main":
            os.system('cp ' + file_path + ' ' + self.app_name + "/")
            return

        folder_path = self.app_name + "/" + module
        os.system('cp ' + file_path + ' ' + folder_path)
    
    def create_folders_inits(self):
        directory = os.path.join(os.getcwd(), self.app_name)
        for root, dirs, files in os.walk(directory):
            current_folder = root.split('/')[-1]
            if current_folder in self.possible_directories:
                self.create_init(root, files)
    
    def create_init(self, current_module_path, files):
        import_file = ""
        for file in files:
            file_without_py = file.replace(".py", "")
            if file in self.file_classes.keys():
                for class_in_file in self.file_classes[file]:
                    import_file += f"from .{file_without_py} import {class_in_file} \n"
        file = open(current_module_path + "/__init__.py", "w")
        file.write(import_file)
        file.close()
    
    def create_list_of_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".py"):
                    self.file_list.append(name)
    
    def verify_imports(self, name, module):
        # if name in self.file_list:
        for key in self.file_imports[name].keys():
            file_name = key + ".py"
            if file_name in self.file_list:
                self.imports_to_replace.append(key)
    
    def make_import_replacements(self):
        new_app_directory = self.app_name + "/"
        for root, dirs, files in os.walk(new_app_directory):
            for name in files:
                if name.endswith(".py"):
                    file_path = os.path.join(root, name)
                    if not os.path.exists(file_path) or "__init__" in name:
                        continue
                    transformer = Transformer(self.imports_to_replace_dict, self.file_classes)

                    file = open(file_path, "r").read()

                    ast_root = ast.parse(file)
                    transformer.visit(ast_root)

                    self.save_file(ast_root, file_path)
    
    def fix_view_folder_call(self):
        new_app_directory = self.app_name + "/app.py"
        transformer = Transformer()
        file = open(new_app_directory, "r").read()

        ast_root = ast.parse(file)
        transformer.visit(ast_root)

        self.save_file(ast_root, new_app_directory)

    

    def save_file(self, ast_root, file_path):
        try:
            buf = StringIO()
            Unparser(ast_root, buf)

            with open (file_path, 'w') as new_file:
                buf.seek(0)
                shutil.copyfileobj(buf, new_file)
        except Exception as e:
            print("Exceção na leitura de arquivos: " + str(e))

    




