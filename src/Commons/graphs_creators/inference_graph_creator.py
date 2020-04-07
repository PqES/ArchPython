from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Enums.edge_status_enum import EdgeStatusEnum

class InferenceGraphCreator:

    def __init__(self, inferences):
        self.inferences = inferences
        self.graph = Graph("Inference Graph")

    
    def create_graph_from_inference(self):
        self.create_nodes()
        self.create_edges()
        return self.graph
    
    def create_nodes(self):
        pass
    
    def create_edges(self):
        pass