from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Enums.edge_status_enum import EdgeStatusEnum
from Enums.problems_enum import ProblemsEnum

class ProblemGraphCreator:

    def __init__(self, inferences, problems):
        self.inferences = inferences
        self.problems = problems

        self.graph = Graph("Problem Graph")

        self.__nodes_cache = {}
        self.__problems_cache = {} #Tupla (de -> para) --> Problema

    
    def create_graph_from_problems(self):
        self.construct_problems_cache()
        self.create_nodes()
        self.create_edges()
        return self.graph
    
    def construct_problems_cache(self):
        for problem in self.problems:
            for restriction_broken in problem.restrictions_broken:
                tuple_key = (problem.origin_module.name, restriction_broken)
                self.__problems_cache[tuple_key] = problem
    
    def create_nodes(self):
        for inference in self.inferences:
            origin_module = inference.origin_module
            inferred_module = inference.inferred_module_name
            if "builtins" in inferred_module:
                inferred_module = inference.variable_type

            if not origin_module in self.__nodes_cache.keys():
                new_node = self.graph.add_node(origin_module)
                self.__nodes_cache[origin_module] = new_node
            
            if not inferred_module in self.__nodes_cache.keys():
                new_node = self.graph.add_node(inferred_module)
                self.__nodes_cache[inferred_module] = new_node
    
    def create_edges(self):
        for inference in self.inferences:
            inferred_module_name = inference.inferred_module_name.replace("builtins.", "")
            tuple_key = (inference.origin_module, inferred_module_name)
            new_edge = None
            
            origin_node = self.__nodes_cache[inference.origin_module]
            destination_node = self.__nodes_cache[inferred_module_name]

            if origin_node.name == destination_node.name:
                continue

            if tuple_key in self.__problems_cache.keys():
                if self.__problems_cache[tuple_key].category == "problem":
                    new_edge = Edge(origin_node, destination_node, EdgeStatusEnum.ERROR_RESTRICTION.value)
                else:
                    new_edge = Edge(origin_node, destination_node, EdgeStatusEnum.WARNING_RESTRICTION.value)
            else:
                new_edge = Edge(origin_node, destination_node, EdgeStatusEnum.ALLOWED.value)
            self.graph.add_edge(new_edge)
        
        for problem in self.problems:
            if problem.problem_type == ProblemsEnum.REQUIRED_RESTRICTION_BROKEN.value:
                for destination in problem.restrictions_broken:
                    if problem.origin_module.name == destination:
                        continue
                    new_edge = Edge(self.__nodes_cache[problem.origin_module.name], self.__nodes_cache[destination], EdgeStatusEnum.ERROR_RESTRICTION.value)
                    self.graph.add_edge(new_edge)