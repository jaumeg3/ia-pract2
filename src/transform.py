
class Transform:
    def __init__(self, output, file_path):
        self.output = list(output)[0].split("\n")
        self.file_path = file_path

    def analize_result(self):
        for x in self.output[:-1]:
            print x
            if x.split()[0] == 'v':
                self._write_result(x.split())

    def _write_result(self, temporal):
        with open(self.file_path, 'w') as f:
            result = []
            for x in temporal[1:]:
                if int(x) > 0:
                    result.append(int(x))
            if len(result) > 0:
                print >> f, "b %s" % str(result).strip("[]").replace(",","")
            else:
                print >> f, "b NO SOLUTION"