
class Transform:
    def __init__(self, output, file_path):
        self.output = output
        self.file_path = file_path

    def analize_result(self):
        raise NotImplementedError()
