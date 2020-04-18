from Models.Visualization.Graph.node import Node

class Graph:

    def __init__(self, graph_name):
        self.graph_name = graph_name
        self.nodes = []
        self.edges = []

        self.__nodes_name_cache = []
        self.__current_node_id = 0
    
    def add_node(self, node_name):
        #TODO: checar se já existe um nó com o mesmo id no grafo
        new_node = Node(self.__current_node_id, node_name)
        if node_name in self.__nodes_name_cache:
            #TODO: Tirar essa string daqui
            raise Exception("Nó já adicionado")
        self.nodes.append(new_node)
        self.__nodes_name_cache.append(node_name)
        self.__current_node_id += 1
        return new_node
    
    def edge_exists(self, node_origin, node_destination):
        for edge in self.edges:
            if edge.node_origin.name == node_origin and edge.node_destination.name == node_destination:
                return edge
        return None
    
    def replace_edge(self, old_edge, new_edge):
        for index, edge in enumerate(self.edges):
            if edge.node_origin.name == old_edge.node_origin.name and edge.node_destination.name == old_edge.node_destination.name:
                self.edges[index] = new_edge
                return


    def add_edge(self, edge):
        #TODO: checar se os nós já existem no grafo
        if edge.node_origin.name in self.__nodes_name_cache and edge.node_destination.name in self.__nodes_name_cache:
            if self.edge_exists(edge.node_origin.name, edge.node_destination.name) == None:
                self.edges.append(edge)
        else: 
            #TODO: Tirar essa string daqui
            raise Exception("Tentando adicionar uma aresta com nós que não existem")
    
    def get_nodes_in_vis_model(self):
        nodes = []
        for node in self.nodes:
            nodes.append({"id": node.idx, "label": node.name})
        return nodes
    
    def get_edges_in_vis_model(self):
        edges = []
        for edge in self.edges:
            if not edge.dashes:
                edges.append({
                    "from": edge.node_origin.idx, 
                    "to": edge.node_destination.idx, 
                    "arrows" : "to",
                    "color": edge.get_color()
                })
            else:
                edges.append({
                    "from": edge.node_origin.idx, 
                    "to": edge.node_destination.idx, 
                    "arrows" : "to",
                    "color": edge.get_color(),
                    "dashes": edge.dashes
                })
        return edges
