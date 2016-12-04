#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


# Main
##############################################################################

global auction
auction = 0

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

    readFile(opts.auction)

def readFile(fitxer):
    with open(fitxer, 'r') as stream:
        readStream(stream)

def readStream(stream):
    matrix = []
    n_goods, n_bids, n_dummies = -1, -1, -1
    boolean = True
    reader = (l.strip() for l in stream)
    for line in (l for l in reader if l):
        temporal = line.split()
        if n_goods != -1 and n_bids != -1 and boolean:
            matrix = [range(n_goods+1) for i in range(n_bids)]
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
            addMatrix(matrix, temporal)
    print matrix
    print n_goods
    print n_bids
    print n_dummies

def addMatrix(matrix, valors):
    global auction
    matrix[auction][0] = int(valors[1])
    for i in range(1,len(valors)-2):
        if int(valors[i]) > 15: pass
        else:
            matrix[auction][int(valors[i])] = "True"
    auction += 1

# Script entry point
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

