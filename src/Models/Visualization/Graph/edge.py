class Edge:

    def __init__(self, node_origin, node_destination, status, dashes = False, label = ""):
        self.node_origin = node_origin
        self.node_destination = node_destination
        
        #Representa se é uma aresta permitida ou não
        self.status = status

        self.dashes = dashes

        self.label = label
    
    def get_color(self):
        return self.status["Color"]
    
    def get_width(self):
        return self.status["Width"]
