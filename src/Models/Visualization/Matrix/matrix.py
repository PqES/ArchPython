class Matrix:

    def __init__(self, name):
        self.name = name
        self.all_modules = []
        self.all_packages = []
        self.cells = []

        self.cells_cache = None

    def add_cell(self, cell):
        self.cells.append(cell)
    
    def get_cell(self, from_module, to_module):
        if self.cells_cache == None:
            self.__construct_cells_cache()
        try:
            key = from_module + to_module
            cell_index = self.cells_cache[key]
            return self.cells[cell_index]
        except:
            return None

        for cell in self.cells:
            if cell.from_module == from_module and cell.to_module == to_module:
                return cell
        return None
    
    def edit_cell_status(self, from_module, to_module, new_status):
        if self.cells_cache == None:
            self.__construct_cells_cache()
        
        key = from_module + to_module
        cell_index = self.cells_cache[key]
        self.cells[cell_index].status_module = new_status

    def edit_cell_content(self, from_module, to_module, new_content):
        if self.cells_cache == None:
            self.__construct_cells_cache()
        
        key = from_module + to_module
        cell_index = self.cells_cache[key]
        self.cells[cell_index].content = new_content
            
    
    def __construct_cells_cache(self):
        self.cells_cache = {}
        for index, cell in enumerate(self.cells):
            key = cell.from_module + cell.to_module
            self.cells_cache[key] = index

            
    
    def get_all_modules(self):
        modules_to_return = self.all_modules
        modules_to_return.insert(0, "")
        return modules_to_return
    
    def get_all_packages(self):
        return self.all_packages
    
    def get_cells_for_template(self):
        all_cells = []
        for cell in self.cells:
            all_cells.append(cell.get_representation())
        return all_cells