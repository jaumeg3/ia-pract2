
class Creator(file):

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
            self.write_dimacs(f)

    def write_dimacs(self, f):
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
        for x in range(0, len(self.hard)):
            print >> f, "%d %s 0" \
                        % (self.infinity, str(self.hard[x]).
                           strip(']').replace(', ', ' -').replace('[', '-'))

        print >> f, "c -----          ALO          -----"
        for x in range(0, len(self.alo)):
            print >> f, "%d %s 0" % (
                self.infinity, str(self.alo[x]).strip('[]').replace(', ', ' '))