import ast

# ----------- TODO ---------------

#PARA A MODEL
    #chamada no DAO (TODO)

#PARA A CONTROLLER
    #import model

# ------------ CONCLUIDOS ----------------

#PARA A ROUTE (Concluído)
    #verificar a assinatura do método (OK)

#PARA O APP.PY (Concluído)
    #Verificar se possui __name__ == "__main__" (OK)

#PARA OS DAO
    #nome de variavel = sql, query, database (ok)
    #import mysql, database (ok)
    #string = "insert into", "select * from", "update from", "delete from" (OK)
    #dao no Nome Da Classe (ok)
    #dao no nome do arquivo (ok)

#PARA A CONTROLLER
    #verificar se CHAMA metodos get e set (OK)
    #verificar strings relacionadas a template (OK)
    #import do flask (OK)

#PARA A MODEL
    #metodos INSTANCIADOS que possuem get e set (OK)
    #tem atributo da classe que chama "index" ou "idx" (OK)




class Visitor(ast.NodeVisitor):

    dao_probability = 0
    model_probability = 0
    controller_probability = 0
    route_probability = 0
    main_probability = 0
    classes = []
    imports = {}

    weights = {
        #para achar Dao
        "class_name" : 0.33,
        "method_name": 0.1, #Nao utilizado
        "string_dao": 0.25,
        "import_from_dao": 0.4,
        "import_from_model": 0.1, #Nao utilizado
        "import_from_controller": 0.1, #Nao utilizado
        "file_name" : 0.33, 
        
        #para achar Rotas
        #Valor alto pq declaração de rotas garante que é um arquivo de rotas
        "route_declaration": 1,

        #Para achar Main
        #Valor alto pq declaração de um main que é um arquivo de main
        "main_defined" : 1,

        #Para achar Models
        "get_set_methods_definition" : 0.3,
        "index_definition" : 0.25,

        #Para achar Controllers
        "get_set_methods_caller" : 0.2,
        "render_functions" : 0.2,
        "import_framework" : 0.4
    }

    def visit_FunctionDef(self, node):
        #Verifica se tem assinatura de route
        if hasattr(node, 'decorator_list'):
            if len(node.decorator_list) > 0:
                child = node.decorator_list[0]
                if "/" in child.args[0].s and child.func.attr == "route":
                    #Isso pode ter o peso máximo pq garante que é uma rota
                    self.route_probability += self.weights['route_declaration']
                    if hasattr(child.func, 'value') and hasattr(child.func.value, 'id'):
                        #Rotas normalmente não são declaradas como classes, então verificamos em qual objeto a rota está instaciada
                        route_id = child.func.value.id
                        if route_id not in self.classes:
                            self.classes.append(route_id)


        #fim verifica se tem assinatura de route

        #Verifica se tem get ou set no nome do método
        if "get" in node.name.lower() or "set" in node.name.lower():
            self.model_probability += self.weights['get_set_methods_definition']
        #FIM Verifica se tem get ou set no nome do método

        #Verifica se tem render no nome do método
        if "render" in node.name.lower():
            self.controller_probability += self.weights['render_functions']
        #Fim verifica se tem render no nome do método

        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        if "dao" in node.name.lower():
            self.dao_probability += self.weights['class_name']
        ast.NodeVisitor.generic_visit(self, node)

    def has_sql(self, text):
        if "insert into" in text.lower():
            return True
        if "select" in text.lower() and "from" in text.lower():
            return True
        if "update" in text.lower() and "from" in text.lower():
            return True
        if "delete" in text.lower() and "from" in text.lower():
            return True

    def find_sql_query(self, node):
        if hasattr(node, "s"):
            if self.has_sql(node.s):
                self.dao_probability += self.weights["string_dao"]
        if hasattr(node, "left"):
            self.find_sql_query(node.left)
        
        if hasattr(node, "right"):
            if hasattr(node.right, "s"):
                if self.has_sql(node.right.s):
                    self.dao_probability += self.weights["string_dao"]                    
            elif hasattr(node.right, "id"):
                # variaveis sendo concatenados na string
                pass

    def visit_Assign(self, node):
        if hasattr(node, "value"):
            self.find_sql_query(node.value)
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Name(self, node):
        if "sql" in node.id.lower() or "query" in node.id.lower() or "database" in node.id.lower():
            self.dao_probability += self.weights['string_dao']
        
        #Verifica se tem render no nome do método
        if "render" in node.id.lower():
            self.controller_probability += self.weights['render_functions']
        #Fim verifica se tem render no nome do método
        
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Compare(self,node):
        #Verifica se é main
        if node.left.id == "__name__" and node.comparators[0].s == "__main__":
            #Pode ter peso máximo. Isso certifica que é o main
            self.main_probability += self.weights['main_defined']
        #Fim Verifica se é main

        ast.NodeVisitor.generic_visit(self, node)
    

    def visit_Call(self, node):
        if hasattr(node, 'attr'):
            if "get" in node.attr or "set" in node.attr:
                self.controller_probability += self.weights['get_set_methods_caller']
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Import(self, node):
        for child in node.names:
            if "sql" in child.name.lower() or "database" in child.name.lower() or "mysql" in child.name.lower():
                self.dao_probability += self.weights['import_from_dao']
                ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Alias(self,node):
        ast.NodeVisitor.generic_visit(self, node)


    
    def visit_ImportFrom(self, node):
        if "database" in node.module.lower() or "sql" in node.module.lower() or "mysql" in node.module.lower() or "mongo" in node.module.lower():
            self.dao_probability += self.weights['import_from_dao']
        if "flask" in node.module.lower() or "django" in node.module.lower():
            self.controller_probability += self.weights['import_framework']
        self.imports[node.module] = []
        for child in node.names:
            self.imports[node.module].append(child.name)

        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Attribute(self, node):
        #Verifica se o nó possui nome relacionado com index
        if "index" in node.attr or "idx" in node.attr or "id" in node.attr:
            self.model_probability += self.weights['index_definition']
        #Fim verifica se o nó possui nome relacionado com index
        ast.NodeVisitor.generic_visit(self, node)
        
    
    def clear_visitor(self):
        self.dao_probability = 0
        self.model_probability = 0
        self.controller_probability = 0
        self.route_probability = 0
        self.main_probability = 0
        self.classes = []
        self.imports = {}
    
    def probabilitiesToString(self):
        out = " > Probabilidades:\n"
        out += ("\t DAO: "  + str(self.dao_probability) + "\n")
        out += ("\t MODEL: "  + str(self.model_probability) + "\n")
        out += ("\t CONTROLLER: "  + str(self.controller_probability) + "\n")
        out += ("\t ROUTE: "  + str(self.route_probability) + "\n")
        out += ("\t MAIN: "  + str(self.main_probability) + "\n")  
        return out


class StructureCrawler:

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, "r").read()
        self.visitor = Visitor()

        self.visitor.clear_visitor()
        Visitor().clear_visitor()

        self.run_ast()
    
    def run_ast(self):
        file_name = self.file_path.split('/')[-1]
        if "dao" in file_name.lower():
            self.visitor.dao_probability += self.visitor.weights['file_name']
        file = ast.parse(self.file)
        self.visitor.visit(file)
    
    def get_file_classes(self):
        return self.visitor.classes
    
    #Função que vai definir o tipo do arquivo (controller, model etc...)
    def get_file_module(self):
        max_value = 0
        file_module = ""
        
        if self.visitor.dao_probability > max_value:
            max_value = self.visitor.dao_probability
            file_module = "dao"

        if self.visitor.model_probability > max_value:
            max_value = self.visitor.model_probability
            file_module = "models"

        if self.visitor.controller_probability > max_value:
            max_value = self.visitor.controller_probability
            file_module = "controllers"

        if self.visitor.route_probability > max_value:
            max_value = self.visitor.route_probability
            file_module = "routes"

        if self.visitor.main_probability > max_value:
            max_value = self.visitor.main_probability
            file_module = "main"
        
        return file_module
    
    def get_file_imports(self):
        return self.visitor.imports






