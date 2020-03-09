import ast

from io import StringIO



class Transformer(ast.NodeTransformer):

    def __init__(self, imports_to_transform = None, file_classes = None):
        self.imports_to_transform = imports_to_transform
        self.file_classes = file_classes
    
    def visit_Assign(self, node):
        if self.imports_to_transform == None and self.file_classes == None:
            if hasattr(node, 'targets') and len(node.targets) > 0 and hasattr(node.targets[0], "id") and node.targets[0].id == "views_folder":
                new_node = ast.parse('views_folder = os.path.abspath("./views")')
                new_node.lineno = node.lineno
                node = new_node.body[0]
                # new_value.lineno = node.lineno
                # node.value = new_value
        ast.NodeVisitor.generic_visit(self, node)
        return node

        

    def visit_ImportFrom(self, node):
        if self.imports_to_transform == None and self.file_classes == None:
            ast.NodeVisitor.generic_visit(self, node)
            return node
        
        new_node = None
        if node.module in self.imports_to_transform.keys():
            if self.imports_to_transform[node.module] == 'routes':
                new_node = ast.parse(f'from {self.imports_to_transform[node.module]} import *')
                ast.NodeVisitor.generic_visit(self, new_node)
                return new_node

            file = node.module + ".py"
            classes_to_import = self.file_classes[file]
            class_str = ""
            for idx in range(len(classes_to_import)):
                if idx == len(classes_to_import) - 1:
                    class_str += classes_to_import[idx]
                else:
                    class_str += classes_to_import[idx] + ", "

            new_node = ast.parse(f'from {self.imports_to_transform[node.module]} import {class_str}')

        if new_node != None:
            ast.NodeVisitor.generic_visit(self, new_node)
            return new_node
        else:
            ast.NodeVisitor.generic_visit(self, node)
            return node
    

