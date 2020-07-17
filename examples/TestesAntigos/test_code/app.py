import sys
from move_views import MoveViews
from move_py_files import MovePyFiles

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Número incorreto de parametros")
        sys.exit(0)

    project_path = sys.argv[1]
    new_project_name = sys.argv[2]
    move_views = MoveViews(new_project_name, project_path)
    move_py_files = MovePyFiles(new_project_name, project_path)
    move_views.get_files_directories()
    pass


