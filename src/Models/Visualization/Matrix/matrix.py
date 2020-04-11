class Matrix:

    def __init__(self, name):
        self.name = name
        self.all_modules = []
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)
    
    def get_all_modules(self):
        modules_to_return = self.all_modules
        modules_to_return.insert(0, "")
        return modules_to_return
    
    def get_cells_for_template(self):
        all_cells = []
        for cell in self.cells:
            all_cells.append(cell.get_representation())
        return all_cells