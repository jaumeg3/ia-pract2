
class Transform:
    def __init__(self, output, file_path, goods):
        self.output = list(output)[0].split("\n")
        self.file_path = file_path
        self.goods = goods

    def analize_result(self):
        for x in self.output[:-1]:
            print x
            if x.split()[0] == 'v':
                self._write_result(x.split())
            else:
                self._write_result([])

    def _write_result(self, temporal):
        with open(self.file_path, 'w') as f:
            result = []
            for x in temporal[1:]:
                if 0 < int(x) < self.goods:
                    result.append(int(x) - 1)
            if len(result) > 0:
                print >> f, "b %s" % str(result).strip("[]").replace(",", "")
            else:
                print >> f, "b NO SOLUTION"