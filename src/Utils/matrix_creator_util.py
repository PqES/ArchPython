class MatrixCreatorUtil(object):

    @staticmethod
    def create_matrix_file(matrix):
        matrix_file_template = MatrixCreatorUtil.__get_matrix_template()
        matrix_file_modified = MatrixCreatorUtil.__modify_template(matrix, matrix_file_template)
        MatrixCreatorUtil.__write_matrix_file(matrix.name, matrix_file_modified)
    
    @staticmethod
    def __get_matrix_template():
        template = './src/Templates/MatrixTemplate.html'
        vis_file = open(template,'r').read()
        return vis_file

    @staticmethod
    def __modify_template(matrix, matrix_file_template):
        all_modules = matrix.get_all_modules()
        all_cells = matrix.get_cells_for_template()

        final_file = matrix_file_template.replace("REPLACE_ALL_FILES", str(all_modules))
        final_file = final_file.replace("REPLACE_RELATIONSHIPS", str(all_cells))

        return final_file

    @staticmethod
    def __write_matrix_file(matrix_name, matrix_final_file):
        file_name = f"{matrix_name.replace(' ', '_').lower()}.html"
        file_path = f"./results/matrices/{file_name}"
        with open(file_path, 'w+') as output:
            output.write(matrix_final_file)


