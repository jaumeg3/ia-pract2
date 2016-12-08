#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from reader import *
from creator import *
from transform import *
from subprocess import PIPE, Popen


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

    reader = Reader()
    reader.read_file(opts.auction)
    if opts.accept_at_least_one:
        reader.generate_alo()
    if opts.accept_at_most_one:
        pass
        reader.generate_amo() # NO FUNCIONA!!!!
    if opts.transform_to_1_3_wpm:
        pass
        reader.transform_to_1_3_wpm()# No implementat
    create = Creator(opts.formula, reader.soft, reader.hard, reader.alo,
                     reader.amo, reader.n_vars, reader.infinity)
    create.write_file()
    execute = Popen([opts.solver, opts.formula], stdin=PIPE, stdout=PIPE,
                    bufsize=1)
    execute.wait()
    output = execute.communicate()
    transform = Transform(output, opts.result)
    transform.analize_result()

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

