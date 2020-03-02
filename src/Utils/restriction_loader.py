class RestrictionLoader():


    @staticmethod
    def get_restrictions(file_content):
        restrictions = []
        for module in file_content:
            name = module
            