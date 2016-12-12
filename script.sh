# !/bin/bash
rm log.txt
rm -r auctions
mkdir auctions

rm -r formules
mkdir formules

rm -r resultats
mkdir resultats

echo "Prova Pract2"
echo "Create Auctions"
mv cats-linux-x64 auctions/
cd auctions/
./cats-linux-x64 -d arbitrary -random_goods 10 15 -random_bids 10 15 -n 10 -int_prices
mv cats-linux-x64 ../
cd ..

echo "Begin Test"
echo 'Normal' >> log.txt
for x in $(ls auctions/)
do
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.wcnf -r resultats/${x}.result -s src/WPM1-2012
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.t13.wcnf -r resultats/${x}.t13.result -s src/WPM1-2012 -t13
	if [ $(diff resultats/${x}.result resultats/${x}.t13.result) ]; then
	    echo 'False' >> log.txt
	else
	    echo 'True' >> log.txt
	fi
done
echo 'ALO' >> log.txt
for x in $(ls auctions/)
do
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.wcnf -r resultats/${x}.result -s src/WPM1-2012 -alo
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.t13.wcnf -r resultats/${x}.t13.result -s src/WPM1-2012 -alo -t13
	if [ $(diff resultats/${x}.result resultats/${x}.t13.result) ]; then
	    echo 'False' >> log.txt
	else
	    echo 'True' >> log.txt
	fi
done
echo 'AMO' >> log.txt
for x in $(ls auctions/)
do
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.wcnf -r resultats/${x}.result -s src/WPM1-2012 -amo
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.t13.wcnf -r resultats/${x}.t13.result -s src/WPM1-2012 -amo -t13
	if [ $(diff resultats/${x}.result resultats/${x}.t13.result) ]; then
	    echo 'False' >> log.txt
	else
	    echo 'True' >> log.txt
	fi
done
echo 'ALO i AMO' >> log.txt
for x in $(ls auctions/)
do
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.wcnf -r resultats/${x}.result -s src/WPM1-2012 -alo -amo
	python src/ca2msat.py -a auctions/${x} -f formules/${x}.t13.wcnf -r resultats/${x}.t13.result -s src/WPM1-2012 -alo -amo -t13
	if [ $(diff resultats/${x}.result resultats/${x}.t13.result) ]; then
	    echo 'False' >> log.txt
	else
	    echo 'True' >> log.txt
	fi
done
echo "END TEST"