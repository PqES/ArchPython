from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Enums.edge_status_enum import EdgeStatusEnum

class NewReflectionGraphCreator:

    def __init__(self, conformity__info, module_definitions):
        self.graph = Graph("Reflection Model")

        self.__nodes_cache = {}
        self.__module_definitions = module_definitions
        self.__conformity__info = conformity__info
    
    def __create_edge_label(self, edge_status, usage_count):
        if usage_count == 0:
            return ""
        if edge_status['Code'] == EdgeStatusEnum.REQUIRED_NOT_USED.value['Code']:
            return f"X(#{usage_count})"
        elif edge_status['Code'] == EdgeStatusEnum.FORBIDDEN_OR_NOT_EXPLICITY_ALLOWED.value['Code']:
            return f"!(#{usage_count})"
        else:
            return f"#{usage_count}"
    
    def create_graph(self):
        self.create_nodes()
        self.create_edges()

        return self.graph

    def create_nodes(self):
        all_modules = set([module.name for module in self.__module_definitions])

        for module in all_modules:
            new_node = self.graph.add_node(module)
            self.__nodes_cache[module] = new_node
        
    
    def create_edges(self):
        for conformity in self.__conformity__info:

            origin_node = None
            final_node = None
            
            if conformity.module_origin not in self.__nodes_cache.keys() or conformity.module_destination not in self.__nodes_cache.keys():
                continue

            origin_node = self.__nodes_cache[conformity.module_origin] 
            final_node = self.__nodes_cache[conformity.module_destination]
            status = conformity.status_enum.value['GraphEnum']
            label = self.__create_edge_label(status, conformity.usage)
            dashes = status['Dashes']

            new_edge = Edge(origin_node, final_node, status, dashes, label)
            self.graph.add_edge(new_edge)
    

   