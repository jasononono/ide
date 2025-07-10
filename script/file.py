from script.utility import Object

class File(Object):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.file = ""

class FileBar:
    def __init__(self):
        pass