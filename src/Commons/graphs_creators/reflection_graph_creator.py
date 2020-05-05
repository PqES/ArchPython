from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Enums.edge_status_enum import EdgeStatusEnum

class ReflectionGraphCreator:

    def __init__(self, inferences, module_definitions):
        self.inferences = inferences
        self.module_definitions = module_definitions

        self.graph = Graph("Reflection Graph")

        self.__nodes_cache = {}

        self.__file_inferences_dict = {}

        self.edges_modified = set()

        self.__modules_usage = {}
    
    def __create_edge_label(self, node_origin, node_destination, edge_status, usage_count = None):
        if edge_status == EdgeStatusEnum.REQUIRED_NOT_USED:
            return f"X(#{usage_count})"
        number_of_dependencies = self.__modules_usage[(node_origin, node_destination)]
        if edge_status == EdgeStatusEnum.REQUIRED_NOT_USED:
            return f"X(#{number_of_dependencies})"
        elif edge_status == EdgeStatusEnum.FORBIDDEN_OR_NOT_EXPLICITY_ALLOWED:
            return f"!(#{number_of_dependencies})"
        else:
            return f"#{number_of_dependencies}"

    
    def create_graph(self):
        self.__calculate_modules_usage()
        self.__create_file_inference_dict()
        self.create_nodes()
        self.create_edges()
        self.paint_problems()

        return self.graph
    
    def __create_file_inference_dict(self):
        file_inference_dict = {}
        for inference in self.inferences:
            file_path = inference.file_path
            if file_path in file_inference_dict.keys():
                file_inference_dict[file_path].append(inference)
            else:
                file_inference_dict[file_path] = [] 
                file_inference_dict[file_path].append(inference)
        self.__file_inferences_dict = file_inference_dict

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

                        edge_label = self.__create_edge_label(origin_node.name, final_node.name, EdgeStatusEnum.ALLOWED)

                        new_edge = Edge(origin_node, final_node, EdgeStatusEnum.ALLOWED.value, label=edge_label)
                        self.graph.replace_edge(old_edge, new_edge)
                        self.edges_modified.add(new_edge)

            if module.required != None:
                for module_required in module.required:
                    origin_module = module.name

                    old_edge = self.graph.edge_exists(origin_module, module_required)

                    if old_edge != None:
                        origin_node = self.__nodes_cache[origin_module] 
                        final_node = self.__nodes_cache[module_required]

                        edge_label = self.__create_edge_label(origin_node.name, final_node.name, EdgeStatusEnum.ALLOWED)

                        new_edge = Edge(origin_node, final_node, EdgeStatusEnum.ALLOWED.value, label=edge_label)
                        self.graph.replace_edge(old_edge, new_edge)
                        self.edges_modified.add(new_edge)
            
            if module.forbidden != None:
                modules_to_paint = set(self.__nodes_cache.keys()).difference(set(module.forbidden))
                for module_allowed in modules_to_paint:
                    origin_module = module.name
                    old_edge = self.graph.edge_exists(origin_module, module_allowed)

                    if old_edge != None:
                        origin_node = self.__nodes_cache[origin_module] 
                        final_node = self.__nodes_cache[module_allowed]

                        edge_label = self.__create_edge_label(origin_node.name, final_node.name, EdgeStatusEnum.ALLOWED)

                        new_edge = Edge(origin_node, final_node, EdgeStatusEnum.ALLOWED.value, label=edge_label)
                        self.graph.replace_edge(old_edge, new_edge)
                        self.edges_modified.add(new_edge)

    
    def draw_forbidden_or_not_explicity_forbidden(self):
        edges_not_painted = set(self.graph.edges) - self.edges_modified
        for old_edge in edges_not_painted:

            edge_label = self.__create_edge_label(old_edge.node_origin.name, old_edge.node_destination.name, EdgeStatusEnum.FORBIDDEN_OR_NOT_EXPLICITY_ALLOWED)

            new_edge = Edge(old_edge.node_origin, old_edge.node_destination, EdgeStatusEnum.FORBIDDEN_OR_NOT_EXPLICITY_ALLOWED.value, "true", label=edge_label)
            self.graph.replace_edge(old_edge, new_edge)

    #Required but not used
    def draw_absences(self):
        for module in self.module_definitions:
            if module.required != None:
                # verificar ressposta do terra dps
                for module_required in module.required:

                    file_dont_use_a_module = False
                    use_count = 0

                    for file in module.files:
                        if not self.__file_access_module(file, module_required):
                            file_dont_use_a_module = True
                        else:
                            use_count += 1
                    
                    if file_dont_use_a_module:
                        old_edge = self.graph.edge_exists(module.name, module_required)

                        if old_edge != None:

                            origin_module = module.name
                            
                            origin_node = self.__nodes_cache[origin_module] 
                            final_node = self.__nodes_cache[module_required]

                            edge_label = self.__create_edge_label(origin_node.name, final_node.name, EdgeStatusEnum.REQUIRED_NOT_USED, use_count)

                            new_edge = Edge(origin_node, final_node, EdgeStatusEnum.REQUIRED_NOT_USED.value, "true", edge_label)
                            self.graph.replace_edge(old_edge, new_edge)
                            self.edges_modified.add(new_edge)

                    #Para cada file dentro de module
                    #Verificar se file acessa module_required
                    #Eu preciso verificar se TODOS os files de module acessam os modules_required

                    # old_edge = self.graph.edge_exists(origin_module, module_required)

                    # if old_edge == None:
                    #     origin_node = self.__nodes_cache[origin_module] 
                    #     final_node = self.__nodes_cache[module_required]

                        
    
    def __file_access_module(self, file, module):
        if "__init__" in file:
            return True
        inferences = self.__file_inferences_dict[file]
        for inference in inferences:
            if inference.inferred_module_name == module:
                return True
        return False
    
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

            if inference.is_external_package and not inferred_module in self.__nodes_cache.keys():
                new_node = self.graph.add_node(inferred_module, True)
                self.__nodes_cache[inferred_module] = new_node

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
    
    def __calculate_modules_usage(self):
        for inference in self.inferences:
            key = (inference.origin_module, inference.inferred_module_name)
            if key in self.__modules_usage.keys():
                self.__modules_usage[key] += 1
            else:
                self.__modules_usage[key] = 1