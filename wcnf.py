#!/usr/bin/env python
# -*- coding: utf -*-

import itertools
import sys
import StringIO as sio


class WCNFException(Exception):
    """Invalid MaxSAT operation."""


class WCNFFormula(object):

    def __init__(self):
        self.num_vars = 0
        self.hard = []  # Item format: [literals]
        self.soft = []  # Item format: (weight, [literals])
        self._sum_soft_weights = 0

    @property
    def num_clauses(self):
        return len(self.hard) + len(self.soft)

    @property
    def top_weight(self):
        return self._sum_soft_weights + 1

    def clean(self):
        self.__init__()

    def add_clauses(self, clauses, weight=0):
        """Adds the given set of clauses, having each one the specified weight.

        :param clauses: Iterable filled with sets of literals.
        :type clauses: list[list[int]]
        :param weight: Weight applied to all the clauses, as in add_clause().
        :type weight: int
        """
        for c in clauses:
            self.add_clause(c)

    def add_clause(self, literals, weight):
        """Adds the given literals as a new clause with the specified weight.

        :param literals: Clause literals
        :type literals: list[int]
        :param weight: Clause weight, less than 1 means infinity.
        :type weight: int
        """
        self._check_literals(literals)
        self._add_clause(literals, weight)

    def add_exactly_one(self, literals, weight):
        """Adds the necessary combination of clauses to ensure that exactly
        one of the given literals evaluates to true.

        :param literals: Literals to include in the exactly one set of clauses.
        :type literals: list[int]
        :param weight: Clauses weight, less than 1 means infinity.
        :type weight: int
        """
        self._check_literals(literals)
        self._add_at_least_one(literals, weight)
        self._add_at_most_one(literals, weight)

    def add_at_least_one(self, literals, weight):
        """Adds the necessary combination of clauses to ensure that at least
        one of the given literals evaluates to true.

        :param literals: Literals to include in the at most one set of clauses.
        :type literals: list[int]
        :param weight: Clause weight, less than 1 means infinity.
        :type weight: int
        """
        self._check_literals(literals)
        self._add_at_least_one(literals, weight)

    def add_at_most_one(self, literals, weight):
        """Adds the necessary combination of clauses to ensure that at most
        one of the given literals evaluates to true.

        :param literals: Literals to include in the at most one set of clauses.
        :type literals: list[int]
        :param weight: Clauses weight, less than 1 means infinity.
        :type weight: int
        """
        self._check_literals(literals)
        self._add_at_most_one(literals, weight)

    def new_var(self):
        """Returns the next free variable of this formula.

        :return: The next free variable (>1).
        :rtype: int
        """
        self.num_vars += 1
        return self.num_vars

    def write_dimacs(self, stream=sys.stdout):
        """Writes the formula in DIMACS format into the specified stream.

        :param stream: A writable stream object.
        """
        tw = self.top_weight
        print >> stream, "p wcnf %d %d %d" % (self.num_vars, self.num_clauses,
                                              tw)
        print >> stream, "c ===== Hard Clauses ====="
        for c in self.hard:
            print >> stream, "%d %s 0" % (tw, " ".join(str(l) for l in c))

        print >> stream, "c ===== Soft Clauses (Sum weights: {0}) ====="\
                         .format(self._sum_soft_weights)
        for w, c in self.soft:
            print >> stream, "%d %s 0" % (w, " ".join(str(l) for l in c))

    def write_dimacs_file(self, file_path):
        """Writes the formula in DIMACS format into the specified file.

        :param file_path: Path to a writable file.
        :type file_path: str
        """
        with open(file_path, 'w') as f:
            self.write_dimacs(f)

    def to_1_3_wpm(self):
        """Transforms this formula to its 1,3 WPM equivalent.

        :return: A new instance whose clauses are the 1,3 WPM
                 equivalent of this.
        """
        msat = WCNFFormula()
        # **** YOUR CODE HERE ****

        return msat

    def _add_clause(self, literals, weight):
        if weight < 1:
            self.hard.append(literals)
        else:
            self.soft.append((weight, literals))
            self._sum_soft_weights += weight

    def _add_at_least_one(self, literals, weight):
        # **** YOUR CODE HERE ****
        raise NotImplementedError()

    def _add_at_most_one(self, literals, weight):
        # **** YOUR CODE HERE ****
        raise NotImplementedError()

    def _check_literals(self, literals):
        for var in itertools.imap(abs, literals):
            if var == 0:
                raise WCNFException("Clause cannot contain variable 0")    
            elif self.num_vars < var:
                raise WCNFException("Clause contains variable {0}, not defined"
                                    " by new_var()".format(var))

    def __str__(self):
        ss = sio.StringIO()
        self.write_dimacs(stream=ss)
        output = ss.getvalue()
        ss.close()
        return output

