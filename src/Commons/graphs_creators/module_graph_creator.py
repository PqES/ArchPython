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
    
    def create_edges(self):
        for module in self.module_definitions:
            
            if module.allowed != None:
                for allowed in module.allowed:
                    new_edge = Edge(self.__nodes_cache[module.name], self.__nodes_cache[allowed], EdgeStatusEnum.ALLOWED.value)
                    self.graph.add_edge(new_edge)
            
            if module.required != None:
                for required in module.required:
                    new_edge = Edge(self.__nodes_cache[module.name], self.__nodes_cache[required], EdgeStatusEnum.REQUIRED.value)
                    self.graph.add_edge(new_edge)
            
            if module.forbidden != None:
                for forbidden in module.forbidden:
                    new_edge = Edge(self.__nodes_cache[module.name], self.__nodes_cache[forbidden], EdgeStatusEnum.FORBIDDEN.value)
                    self.graph.add_edge(new_edge)

