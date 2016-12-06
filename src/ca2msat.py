#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, os


# Main
##############################################################################

def main(opts):
    # Este código de ejemplo os escribirá por pantalla el valor de las
    # variables proporcionadas mediante la linea de comandos
    #
    # Podéis ver como se comportan, ejecutando el script con distintas
    # configuraciones. Por ejemplo:
    #
    # ca2msat.py -a a1.txt -f s1.txt -r r1.txt -s WPM3 -alo -amo
    # ca2msat.py -a a2.txt -f s2.txt -r r2.txt -s ./path/to/wpm3 -amo -t13
    #
    print "-a/--auction:", opts.auction
    print "-f/--formula:", opts.formula
    print "-r/--result:", opts.result
    print "-s/--solver:", opts.solver
    print "-alo/--accept-at-least-one:", opts.accept_at_least_one
    print "-amo/--accept-at-most-one:", opts.accept_at_most_one
    print "-t13/--transform-to-1-3-wpm:", opts.transform_to_1_3_wpm

    # **** YOUR CODE HERE ****

    bids, conjunt, agent = readFile(opts.auction)

    print "Bids: " + str(bids)
    print "Soft: " + str(conjunt)
    print "Persona: " + str(agent)

    soft, hard, correlacio = evaluateDependencies(bids, conjunt, agent, opts.accept_at_least_one, opts.accept_at_most_one\
                                      , opts.transform_to_1_3_wpm)
    writeFile(opts.formula, soft, hard, correlacio)
    executeSolver(opts.solver, opts.formula)
    print "----------------------------------------------------------------------------"
    print "Soft" + str(soft)
    print "Hard" + str(hard)



def readFile(fitxer):
    with open(fitxer, 'r') as stream:
        return readStream(stream)


def readStream(stream):
    bids, conjunt, agents = dict(), [], dict()
    n_goods, n_bids, n_dummies = -1, -1, -1
    boolean = True
    reader = (l.strip() for l in stream)
    for line in (l for l in reader if l):
        temporal = line.split()
        if n_goods != -1 and n_bids != -1 and n_dummies != -1 and boolean:
            for x in range(0, n_goods):
                bids["Good "+str(x)] = []
            for x in range(0, n_dummies):
                agents["Agent "+str(x)] = []
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
            pass
            addBids(bids, conjunt, temporal, n_goods, agents)
    return bids, conjunt, agents


def addBids(bids, conjunt, temporal, n_goods, agents):
    n_conjunt = int(len(conjunt) ) + 1#n_conjunt = "X"+str(len(conjunt))
    conjunt.append((int(n_conjunt), int(temporal[1])))
    if int(temporal[-2]) < n_goods:
        agents["Agent "+str(len(agents))] = str(n_conjunt)
    else:
        agents["Agent "+str(int(temporal[-2]) % n_goods)].append(str(n_conjunt))
    for x in range(0,len(temporal)):
        if x < 2 or x == len(temporal)-1:
            pass
        elif int(temporal[x]) < n_goods:
            bids["Good "+str(temporal[x])].append(int(n_conjunt))


def evaluateDependencies(bids, conjunt, agent, ALO, AMO, WPM):
    hard = []
    correlacio = 0
    for x in range(0, len(bids)):
        hard.append(bids.get("Good "+str(x)))
    return conjunt, hard, correlacio


def writeFile(filepath, soft, hard, correlacio):
    with open(filepath, 'w') as f:
        writeDimacs(f, soft, hard, correlacio)


def writeDimacs(f, soft, hard, correlacio):
    infinity = 1
    for x in range(0,len(soft)):
        infinity += soft[x][1]
    num_vars = len(soft) + correlacio
    num_clauses = len(soft) + len(hard)
    print >> f, "p wcnf %d %d %d" % (num_vars, num_clauses, infinity)
    print >> f, "c ===== SOFT CLAUSULES  TotalWeight = %d =====" % (infinity-1)
    for x in range(0, len(soft)):
        print >> f, "%s %s 0" % (soft[x][1], soft[x][0])
    print >> f, "c ===== HARD CLAUSULES ====="
    for x in range(0,len(hard)):
        print >> f, "%d %s 0" % (infinity, str(hard[x]).strip(']').replace(', ', ' -').replace('[', ' -'))


def executeSolver(solver, formula):
    print os.system("bash " + str(solver) + formula)

#Script entry point
###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="", epilog="")

    parser.add_argument('-a', '--auction', type=str, required=True,
                        help="Combinatorial auction file")

    parser.add_argument('-f', '--formula', type=str, required=True,
                        help="Wcnf formula file path")

    parser.add_argument('-r', '--result', type=str, required=True, 
                        help="Result file path")

    parser.add_argument('-s', '--solver', type=str, required=True,
                        help="Path to the WPM3 solver")

    parser.add_argument('-alo', '--accept-at-least-one', action='store_true',
                        help="Accept at least one bid from each agent")

    parser.add_argument('-amo', '--accept-at-most-one', action='store_true',
                        help="Accept at most one bid from each agent")

    parser.add_argument('-t13', '--transform-to-1-3-wpm', action='store_true',
                        help="Transform the final formula to 1,3-WPM")

    main(parser.parse_args())

