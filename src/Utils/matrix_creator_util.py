import os
import errno

class MatrixCreatorUtil(object):

    @staticmethod
    def create_matrix_file(matrix, project_name):
        matrix_file_template = MatrixCreatorUtil.__get_matrix_template()
        matrix_file_modified = MatrixCreatorUtil.__modify_template(matrix, matrix_file_template)
        MatrixCreatorUtil.__write_matrix_file(matrix.name, matrix_file_modified, project_name)
    
    @staticmethod
    def __get_matrix_template():
        template = './src/Templates/MatrixTemplate.html'
        vis_file = open(template,'r').read()
        return vis_file

    @staticmethod
    def __modify_template(matrix, matrix_file_template):
        all_modules = matrix.get_all_modules()
        all_cells = matrix.get_cells_for_template()
        all_packages = matrix.get_all_packages()

        final_file = matrix_file_template.replace("REPLACE_ALL_FILES", str(all_modules))
        final_file = final_file.replace("REPLACE_RELATIONSHIPS", str(all_cells))
        final_file = final_file.replace("REPLACE_ALL_PACKAGES", str(all_packages))

        return final_file

    @staticmethod
    def __write_matrix_file(matrix_name, matrix_final_file, project_name):
        file_name = f"{matrix_name.replace(' ', '_').lower()}.html"
        file_path = f"./results/{project_name}/main/{file_name}"

        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        with open(file_path, 'w+') as output:
            output.write(matrix_final_file)


