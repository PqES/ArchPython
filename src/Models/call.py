class Call:

    def __init__(self, file_path_from, variable_from, full_name_from , file_path_to, variable_to, full_name_to):
        
        self.file_path_from = file_path_from
        self.full_name_from = full_name_from
        self.variable_from = variable_from

        full_name_from_split = full_name_from.split("::")
        
        self.file_name_from = full_name_from_split[0]
        self.class_from = full_name_from_split[1]
        self.function_from = full_name_from_split[2]


        self.file_path_to = file_path_to
        self.full_name_to = full_name_to
        self.variable_to = variable_to

        full_name_to_split = full_name_to.split("::")

        self.file_name_to = full_name_to_split[0]
        self.class_to = full_name_to_split[1]
        self.function_to = full_name_to_split[2]
    