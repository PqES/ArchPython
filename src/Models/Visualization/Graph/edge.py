class Edge:

    def __init__(self, node_origin, node_destination, status):
        self.node_origin = node_origin
        self.node_destination = node_destination
        
        #Representa se é uma aresta permitida ou não
        self.status = status
    
    def get_color(self):
        return self.status["Color"]
