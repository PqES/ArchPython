class Module:

    def __init__(self, name, package, files, allowed, forbidden, required):
        
        self.name = name
        self.package = package
        self.files = files
        self.allowed = allowed
        self.forbidden = forbidden
        self.required = required

