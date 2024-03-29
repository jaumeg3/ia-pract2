class Reader:
    def __init__(self):
        self.n_vars = 0
        self.hard = []
        self.soft = []
        self.alo = []
        self.amo = []
        self.infinity = 1
        self.agents = dict()
        self.goods = 0

    def read_file(self, file_name):
        """
        This function reads the auction file
        :param file_name: path to the file
        :return: void
        """
        try:
            with open(file_name, 'r') as stream:
                return self._read_stream(stream)
        except:
            print "Error, the file couldn't be read"

    def _read_stream(self, stream):
        """
        This function reads each line in the auction file
        :param stream: stream
        :return: void
        """
        bids = dict()
        n_goods, n_bids, n_dummies = -1, -1, -1
        boolean = True
        read = (l.strip() for l in stream)
        for line in (l for l in read if l):
            temporal = line.split()
            if n_goods != -1 and n_bids != -1 and n_dummies != -1 and boolean:
                self.goods = n_goods
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
        """
        This file process the line and identify the bids
        :param bids: List of bids
        :param temporal: Line to process (list)
        :param n_goods: Number of goods (integer)
        :return: void
        """
        self.n_vars += 1
        self.soft.append((int(temporal[0])+1, int(temporal[1])))
        self.infinity += int(temporal[1])
        if int(temporal[-2]) < n_goods:
            self.agents["Agent " + str(len(self.agents))] = \
                [-(int(temporal[0])+1)]
        else:
            self.agents["Agent " + str(int(temporal[-2])
                        % n_goods)].append(-(int(temporal[0])+1))
        for x in range(0, len(temporal)):
            if x < 2 or x == len(temporal) - 1:
                pass
            elif int(temporal[x]) < n_goods:
                bids["Good " + str(temporal[x])].append(-(int(temporal[0])+1))

    def generate_alo(self):
        """
        This function generate de ALO clauses
        :return: void
        """
        for c in self.agents:
            temporal = self.agents.get(c)
            self.alo.append(map(abs, temporal))

    def generate_amo(self):
        """
        This function generate de AMO clauses
        :return: void
        """
        for x in self.agents:
            temporal = list(self.agents.get(x))
            if len(temporal) > 1:
                combinations = self._combinatory(temporal, 2)
                for c in combinations:
                    self.amo.append(c)
            else:
                self.amo.append(temporal)

    def _combinatory(self, c, n):
        """
        This function returns a list of possible combinations in order to \
        generate AMO clauses
        :param c: List of the clauses to be combinated
        :param n: Number of elements in the combination
        :return: List of possible combinations
        """
        return [s for s in self._powers(c) if len(s) == n]

    def _powers(self, c):
        """
        This function returns a list of possible combinations in order to \
        generate AMO clauses
        :param c: List of the clauses to be combinated
        :return: List of the combinations
        """
        if len(c) == 0:
            return [[]]
        r = self._powers(c[:-1])
        return r + [s + [c[-1]] for s in r]

    def transform_to_1_3_wpm(self, alo=False, amo=False):
        """
        This function returns the formula with a format (1,3) WPM
        :param alo: Flag ALO
        :param amo: Flag AMO
        :return: void
        """
        self.hard = self._transform_to_1_3_wpm(self.hard)
        if alo:
            self.alo = self._transform_to_1_3_wpm(self.alo)
        if amo:
            self.amo = self._transform_to_1_3_wpm(self.amo)

    def _transform_to_1_3_wpm(self, source_list):
        """
        This function reduce the clauses to (1,3) WPM
        :param source_list: List of the clauses that will be reduced
        :return: void
        """
        destination_list = []
        for c in source_list:
            if len(c) > 3:
                destination_list.append(c[:2] + [self._new_var()])
                temporal = 2
                for x in range(0, len(c) - 4):
                    destination_list.append([-self.n_vars] + [c[temporal]]
                                            + [self._new_var()])
                    temporal += 1
                destination_list.append([-self.n_vars] + c[temporal:])
            elif len(c) == 2:
                destination_list.append([c]+[self._new_var()])
                destination_list.append([-self.n_vars])
            else:
                destination_list.append(c)
        return destination_list

    def _new_var(self):
        """
        This function increases the variables of the problem
        :return: return the top var
        """
        self.n_vars += 1
        return self.n_vars
