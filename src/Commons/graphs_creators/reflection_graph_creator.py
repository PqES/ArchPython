from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Enums.edge_status_enum import EdgeStatusEnum

class ReflectionGraphCreator:

    def __init__(self, inferences, problems, module_definitions):
        self.inferences = inferences
        self.problems = problems
        self.module_definitions = module_definitions

        self.graph = Graph("Reflection Graph")

        self.__nodes_cache = {}

        self.edges_modified = set()

    
    def create_graph(self):
        self.create_nodes()
        self.create_edges()
        self.paint_problems()

        return self.graph
    

    def paint_problems(self):

        self.draw_allowed_dependencies() #Black normal
        self.draw_absences() #Dotted red - requerido e não usado
        self.draw_allowed_not_used() #Gray Normal
        self.draw_forbidden_or_not_explicity_forbidden() #Laranja dashed
    
    def draw_allowed_dependencies(self):
        for module in self.module_definitions:
            if module.allowed != None:
                for module_allowed in module.allowed:
                    origin_module = module.name

                    old_edge = self.graph.edge_exists(origin_module, module_allowed)

                    if old_edge != None:
                        origin_node = self.__nodes_cache[origin_module] 
                        final_node = self.__nodes_cache[module_allowed]

                        new_edge = Edge(origin_node, final_node, EdgeStatusEnum.ALLOWED.value)
                        self.graph.replace_edge(old_edge, new_edge)
                        self.edges_modified.add(new_edge)
    
    def draw_forbidden_or_not_explicity_forbidden(self):
        edges_not_painted = set(self.graph.edges) - self.edges_modified
        for old_edge in edges_not_painted:
            new_edge = Edge(old_edge.node_origin, old_edge.node_destination, EdgeStatusEnum.FORBIDDEN_OR_NOT_EXPLICITY_ALLOWED.value)
            self.graph.replace_edge(old_edge, new_edge)

    
    def draw_absences(self):
        for module in self.module_definitions:
            if module.required != None:
                for module_required in module.required:
                    origin_module = module.name

                    old_edge = self.graph.edge_exists(origin_module, module_required)

                    if old_edge == None:
                        origin_node = self.__nodes_cache[origin_module] 
                        final_node = self.__nodes_cache[module_required]

                        new_edge = Edge(origin_node, final_node, EdgeStatusEnum.REQUIRED_NOT_USED.value)
                        self.graph.add_edge(new_edge)
                        self.edges_modified.add(new_edge)
    
    def draw_allowed_not_used(self):
        for module in self.module_definitions:
            if module.allowed != None:
                for module_allowed in module.allowed:
                    origin_module = module.name

                    old_edge = self.graph.edge_exists(origin_module, module_allowed)

                    if old_edge == None:
                        origin_node = self.__nodes_cache[origin_module] 
                        final_node = self.__nodes_cache[module_allowed]

                        new_edge = Edge(origin_node, final_node, EdgeStatusEnum.ALLOWED_NOT_USED.value)
                        self.graph.add_edge(new_edge)
                        self.edges_modified.add(new_edge)

    def create_nodes(self):
        for inference in self.inferences:
            origin_module = inference.origin_module
            inferred_module = inference.inferred_module_name

            if not origin_module in self.__nodes_cache.keys():
                new_node = self.graph.add_node(origin_module)
                self.__nodes_cache[origin_module] = new_node
            
            if not inferred_module in self.__nodes_cache.keys():
                new_node = self.graph.add_node(inferred_module)
                self.__nodes_cache[inferred_module] = new_node
    
    def create_edges(self):
        for inference in self.inferences:

            origin_node = self.__nodes_cache[inference.origin_module] 
            final_node = self.__nodes_cache[inference.inferred_module_name]

            if origin_node.name == final_node.name:
                continue

            new_edge = Edge(origin_node, final_node, EdgeStatusEnum.UNDEFINED.value)
            self.graph.add_edge(new_edge)