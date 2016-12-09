#!/bin/bash

let a = 0
for x in `ls prova/`; do
    prova/cats-linux-x64 -d arbitrary -random_goods 10 15 -random_bids 10 15 -n 10 -int_prices
    python src/ca2msat.py -a prova/$x -f prova/x.wcnf -r prova/pet.txt -s src/WPM1-2012 -alo
    python src/ca2msat.py -a prova/$x -f prova/x.wcnf -r prova/pet.txt -s src/WPM1-2012 -amo
    python src/ca2msat.py -a prova/$x -f prova/x.wcnf -r prova/pet.txt -s src/WPM1-2012 -alo -amo
done