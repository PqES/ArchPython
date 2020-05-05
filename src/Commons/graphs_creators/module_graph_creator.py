from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Enums.edge_status_enum import EdgeStatusEnum

class ModuleGraphCreator():

    def __init__(self, module_definitions):
        self.module_definitions = module_definitions
        self.graph = Graph("Module Graph")

        self.__nodes_cache = {}
    
    def create_graph_from_module(self):
        self.create_nodes()
        self.create_edges()

        return self.graph
    
    def create_nodes(self):
        for module in self.module_definitions:
            new_node = self.graph.add_node(module.name)
            self.__nodes_cache[module.name] = new_node
    
    def get_not_forbidden_set(self, module):
        forbidden_modules = set(module.forbidden)
        all_modules = set(self.__nodes_cache.keys())
        all_modules.remove(module.name)

        return list(all_modules.difference(forbidden_modules))
        
    
    def create_edges(self):
        for module in self.module_definitions:
            
            if module.allowed != None:
                for allowed in module.allowed:
                    new_edge = Edge(self.__nodes_cache[module.name], self.__nodes_cache[allowed], EdgeStatusEnum.MODULE_ALLOWED.value)
                    self.graph.add_edge(new_edge)
            
            if module.required != None:
                for required in module.required:
                    new_edge = Edge(self.__nodes_cache[module.name], self.__nodes_cache[required], EdgeStatusEnum.MODULE_REQUIRED.value)
                    self.graph.add_edge(new_edge)
            
            if module.forbidden != None:
                not_forbidden_modules = self.get_not_forbidden_set(module)
                for allowed in not_forbidden_modules:
                    new_edge = Edge(self.__nodes_cache[module.name], self.__nodes_cache[allowed], EdgeStatusEnum.MODULE_ALLOWED.value)
                    self.graph.add_edge(new_edge)

