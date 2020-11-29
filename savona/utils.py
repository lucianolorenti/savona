
class FileFinder:
    def __init__(self, paths=[]):
        self.paths = paths

    def find(self, file):
        for f in self.paths:
            if (f / file).is_file():
                return f/file
        raise FileNotFoundError(file)
