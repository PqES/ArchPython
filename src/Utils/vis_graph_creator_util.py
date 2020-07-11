import os
import errno

class VisGraphCreatorUtil(object):

    @staticmethod
    def create_vis_graph(graph, project_name, is_main=False):
        vis_file_template = VisGraphCreatorUtil.__get_vis_template()
        vis_file_modified = VisGraphCreatorUtil.__modify_template(graph, vis_file_template)
        VisGraphCreatorUtil.__write_vis_file(graph.graph_name, vis_file_modified, project_name, is_main)
        

    @staticmethod
    def __get_vis_template():
        template = './src/Templates/VisTemplate.html'
        vis_file = open(template,'r').read()
        return vis_file
    
    @staticmethod
    def __modify_template(graph, vis_file_template):
        nodes = graph.get_nodes_in_vis_model()
        edges = graph.get_edges_in_vis_model()
        final_vis_file = vis_file_template.replace("REPLACE_GRAPH_NODES", str(nodes))
        final_vis_file = final_vis_file.replace("REPLACE_GRAPH_EDGES", str(edges))
        final_vis_file = final_vis_file.replace("True", "true")
        final_vis_file = final_vis_file.replace("False", "false")

        return final_vis_file

    @staticmethod
    def __write_vis_file(graph_name, vis_final_file, project_name, is_main=False):
        category_folder = "main" if is_main else "extra"
        file_name = f"{graph_name.replace(' ', '_').lower()}.html"
        file_path = f"./results/{project_name}/{category_folder}/{file_name}"

        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        with open(file_path, 'w+') as output:
            output.write(vis_final_file)
