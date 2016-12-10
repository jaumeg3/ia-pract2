
class Creator:

    def __init__(self, file_path, soft, hard, alo, amo, num_vars, infinity):
        self.file_path = file_path
        self.soft = soft
        self.hard = hard
        self.alo = alo
        self.amo = amo
        self.num_vars = num_vars
        self.infinity = infinity

    def write_file(self):
        with open(self.file_path, 'w') as f:
            self._write_dimacs(f)

    def _write_dimacs(self, f):
        num_clauses = len(self.soft) + len(self.hard) + len(self.alo) \
                        + len(self.amo)
        print >> f, "p wcnf %d %d %d" % (self.num_vars, num_clauses,
                                            self.infinity)
        print >> f, "c ===== SOFT CLAUSULES  TotalWeight = {:d} =====" \
            .format(self.infinity - 1)
        for x in range(0, len(self.soft)):
            print >> f, "%s %s 0" % (self.soft[x][1], self.soft[x][0])
        print >> f, "c =====     HARD CLAUSULES    ====="
        print >> f, "c ----- Compatibility of bids -----"
        self._write_clauses(f, self.hard)
        if len(self.alo) > 0:
            print >> f, "c -----          ALO          -----"
            self._write_clauses(f, self.alo)
        if len(self.amo) > 0:
            print >> f, "c -----          AMO          -----"
            self._write_clauses(f, self.amo)

    def _write_clauses(self, f, clauses):
        for x in range(0, len(clauses)):
            print >> f, "%d %s 0" \
                        % (self.infinity, str(clauses[x]).
                           strip('[]').replace(', ', ' ').replace(']', ''))
