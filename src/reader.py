class Reader():
    def __init__(self):
        self.n_vars = 0
        self.hard = []
        self.soft = []
        self.alo = []
        self.amo = []
        self.infinity = 1
        self.agents = dict()

    def read_file(self, file_name):
        with open(file_name, 'r') as stream:
            return self._read_stream(stream)

    def _read_stream(self, stream):
        bids = dict()
        n_goods, n_bids, n_dummies = -1, -1, -1
        boolean = True
        read = (l.strip() for l in stream)
        for line in (l for l in read if l):
            temporal = line.split()
            if n_goods != -1 and n_bids != -1 and n_dummies != -1 and boolean:
                for x in range(0, n_goods):
                    bids["Good " + str(x)] = []
                for x in range(0, n_dummies):
                    self.agents["Agent " + str(x)] = []
                boolean = False
            if temporal[0] == '%' or temporal[0] == "%%" or temporal[0] == '':
                pass
            elif temporal[0] == 'goods':
                n_goods = int(temporal[1])
            elif temporal[0] == 'bids':
                n_bids = int(temporal[1])
            elif temporal[0] == 'dummy':
                n_dummies = int(temporal[1])
            else:
                self._add_bids(bids, temporal, n_goods)
        for x in range(0, len(bids)):
            self.hard.append(bids.get("Good " + str(x)))

    def _add_bids(self, bids, temporal, n_goods):
        self.n_vars += 1
        self.soft.append((int(temporal[0])+1, int(temporal[1])))
        self.infinity += int(temporal[1])
        if int(temporal[-2]) < n_goods:
            self.agents["Agent " + str(len(self.agents))] = int(temporal[0])+1
        else:
            self.agents["Agent " + str(int(temporal[-2])
                        % n_goods)].append(int(temporal[0])+1)
        for x in range(0, len(temporal)):
            if x < 2 or x == len(temporal) - 1:
                pass
            elif int(temporal[x]) < n_goods:
                bids["Good " + str(temporal[x])].append(int(temporal[0])+1)

    def _print_clauses(self):
        print self.hard
        print self.soft
        print self.n_vars
        print self.agents
        print self.alo

    def generate_alo(self):
        for c in range(0, len(self.agents)):
            self.alo.append(self.agents.get("Agent "+str(c)))

    def generate_amo(self):
        for x in range(0, len(self.agents)):
            try:
                temporal = list(self.agents.get("Agent "+str(x)))
                combinations = self._combinatory(temporal, 2)
                for c in combinations:
                    self.amo.append(c)
            except:
                pass

    def _combinatory(self, c, n):
        return [s for s in self._powers(c) if len(s) == n]

    def _powers(self, c):
        if len(c) == 0:
            return [[]]
        r = self._powers(c[:-1])
        return r + [s + [c[-1]] for s in r]

    def transform_to_1_3_wpm(self, alo = False):
        self.hard = self._transform_to_1_3_wpm(self.hard, [])
        if alo:
            self.alo = self._transform_to_1_3_wpm(self.alo, [])

    def _transform_to_1_3_wpm(self, source_list, destination_list):
        for c in source_list:
            print c
            try:
                if len(c) > 3:
                    destination_list.append(c[:2] + [self._new_var()])
                    temporal = 2
                    for x in range(0, len(c) - 4):
                        destination_list.append([-self.n_vars] + [c[temporal]]
                                                + [self._new_var()])
                        temporal += 1
                    destination_list.append([-self.n_vars] + c[temporal:])
                else:
                    destination_list.append(c)
            except:
                pass
        return destination_list

    def _new_var(self):
        self.n_vars += 1
        return self.n_vars
