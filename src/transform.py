
class Transform:
    def __init__(self, output, file_path, goods):
        self.output = list(output)[0].split("\n")
        self.file_path = file_path
        self.goods = goods

    def analyze_result(self):
        """
        This function analyze the result of the execution
        :return: void
        """
        for x in self.output[:-1]:
            self._write_result(x.split()) if x.split()[0] == 'v' else \
                self._write_result([])

    def _write_result(self, temporal):
        """
        This function write the result in the file
        :param temporal: result of the execution
        :return: void
        """
        try:
            with open(self.file_path, 'w') as f:
                result = []
                for x in temporal[1:]:
                    result.append(int(x) - 1) if 0 < int(x) < self.goods else 0
                if len(result) > 0:
                    print >> f, "b %s" % str(result).strip("[]").\
                        replace(",", "")
                else:
                    print >> f, "b NO SOLUTION"
        except:
            print "Error, the file couldn't be created"
