import jedi
import sys
from read_py_files import ReadPyFiles

if __name__ == "__main__":
    project_root_folder = "/home/eduardol/UFLA/tcc/arquivos-arthur/dataset/sistema0"

    read_py_files = ReadPyFiles(project_root_folder)
    read_py_files.find_pys()
    files = read_py_files.get_files_dictionary()


    for key in files:
        file_dict = files[key]

        # script_names = jedi.Script(path=file_dict['path']).get_names(all_scopes=True, definitions=True, references=True)
        script_names = jedi.Script(path=file_dict['path']).get_names()


        for definition in script_names:
            inferences = definition.infer()
            for inference in inferences:
                files[key]['types'].add(inference.name)

            # inference = definition.infer()[0].name
            # files[key]['types'].append(inference)
        

    a = 2



