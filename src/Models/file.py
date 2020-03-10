
class File(object):

    def __init__(self, file_name, file_path, types):
        self.file_name = file_name
        self.file_path = file_path
        self.types = types
    
    def get_as_dict(self):
        return {
            'file' : self.file_name,
            'file_path' : self.file_path,
            'types' : list(self.types)
        }
