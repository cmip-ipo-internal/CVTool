class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class MipTableError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ModuleLoadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GitAPIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        

